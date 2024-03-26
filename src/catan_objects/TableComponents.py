from catan_objects.Motor import *
from catan_objects.BoardComponents import *
from unit_tests.StandardBoard import StandardSetup
from catan_objects.CatanBoard import CatanBoard

import numpy as np
import cv2
import copy

# Such as the lift and the cover
class SingleDegreeComponent():
    def __init__(self, motor : Stepper, maximum_value, minimum_value = 0):
        self.motor = motor
        self.maximum_value = maximum_value
        self.minimum_value = minimum_value
    
    def set_high_position(self):
        self.motor.move_to(self.maximum_value)
        
    def set_low_position(self):
        self.motor.move_to(self.minimum_value)

class Lift(SingleDegreeComponent):
    def __init__(self, motor: Stepper, maximum_value, minimum_value, solenoid_1: DCMotor, solenoid_2: DCMotor):
        super().__init__(motor, maximum_value, minimum_value)
        # self.lift = lift #if we make this a list we can have as many lead screws as we need
        self.solenoid_1 = solenoid_1
        self.solenoid_2 = solenoid_2 # Ask owen if we can wire these in series

    def set_high_position(self):
        self.motor.move_to(self.maximum_value)
        self.solenoid_1.stop()
        self.solenoid_2.stop()
        
    def set_low_position(self):
        self.solenoid_1.start(1)
        self.solenoid_2.start(1)
        self.motor.move_to(self.minimum_value)
"""
K and D are found using cv2.camera_calibration, see fisheyeCalibration Scripts
H is used with cv2.findHomography where uv is pixel coords and xy is real world coords 
uv = np.array([[548,103], [337,143],[239,368],[515,279]])
xy = np.array([[0,0], [-500, -100], [-700,-600], [-100, -400]])

h, status = cv2.findHomography(xy, uv)
see https://colab.research.google.com/drive/1rSl_eMrMY3c0pPDfQxWlSY97dhvtqyMP#scrollTo=VxaYMfC-n9wo
"""
class CameraRig():
    def __init__(self, camera : CameraModule, light: Lights, position = [0,0]):
        self.camera = camera
        self.light = light
        self.pose = position
        self.K = np.array([[113.49354735654141, 0.0, 371.5786534104595], [0.0, 116.6060998517777, 205.3861581256824], [0.0, 0.0, 1.0]])
        self.D = np.array([[0.12694667308062602], [0.6454345033192549], [-0.5465056949757663], [0.25172851391836865]])
        self.H = np.array([[ 3.98379589e-01, 8.28098023e-02, 5.48000000e+02], [-6.12605764e-03,-3.84345357e-01, 1.03000000e+02], [-6.28872633e-05, 2.09711523e-04, 1.00000000e+00]])
        self.image = None
        
    def take_picture(self):
        # turn light on
        self.light.start()
        # take picture
        self.camera.take_picture()
        # turn off light
        self.light.stop()
        # Load and undistort picture
        self.load_image('/home/pi/Desktop/cam/Catable_Image.jpg')
        self.undistort_picture()
        
    def undistort_picture(self):
        # Can use Knew to change scale so it fits
        self.image = cv2.fisheye.undistortImage(self.image, self.K, D=self.D)

    def convert_to_world(self, positions_camera_space):
        positions_world_space = []
        for position in positions_camera_space:
            positions_world_space.append(self.convert_to_world_single(position))
            
        return positions_world_space
            
    def convert_to_world_single(self, position_camera_space):
        if not isinstance(position_camera_space, np.ndarray):
            position_camera_space = np.array(position_camera_space)
            
        position_camera_space = np.append(position_camera_space, 1.0)
        world_space = np.matmul(np.linalg.inv(self.H), position_camera_space)

        w_x = world_space[0] / world_space[2]
        w_y = world_space[1] / world_space[2]
        
        # Adding position, the rotation and position probably need to be defined as a matrix that we multiply
        w_x = w_x + self.pose[0]
        w_y = w_y + self.pose[1]
        
        return [w_x,w_y]

    def threshold_between_values(self, image, thresh_min, thresh_max):
        # Finding two thresholds and then finding the common part
        _, threshold = cv2.threshold(image, thresh_min, 255, cv2.THRESH_BINARY)
        _, threshold2 = cv2.threshold(image, thresh_max, 255, cv2.THRESH_BINARY_INV)
        return cv2.bitwise_and(threshold, threshold2)

    def threshold_in_range(self, image, threshold_range):
        return self.threshold_between_values(image, threshold_range[0], threshold_range[1])

    def find_background(self, image):
        h, s, v = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2HSV))
        blue = [0.5 * 180, 0.65 * 180]
        background = self.threshold_in_range(h, blue)
        background = cv2.morphologyEx(background, cv2.MORPH_DILATE, np.ones((7, 7), np.uint8))
        contours, hierarchy = cv2.findContours(background, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        # Find two biggest contours
        max_area_index = 0
        second_max_area_index = 0
        max_area = 0
        second_max_area = 0
        for i, cont in enumerate(contours):
            tmp_area = cv2.contourArea(cont)
            if tmp_area > max_area:
                second_max_area = max_area
                second_max_area_index = max_area_index
                max_area = tmp_area
                max_area_index = i
            elif tmp_area > second_max_area:
                second_max_area = tmp_area
                second_max_area_index = i

        if hierarchy[0][second_max_area_index][3] == max_area_index:
            best_contour = contours[second_max_area_index]
        else:
            best_contour = contours[max_area_index]
        return best_contour

    def load_image(self, filepath = 'src\\unit_tests\\images\\robber1.jpeg'):
        image = cv2.imread(filepath)
        self.image = image

    def crop_to_hexes(self, image, catan_board : CatanBoard, box):
        centers = [space.position for space in catan_board.empty_spaces if space.position != catan_board.desert_position]
        
        cropped_images = []

        for center in centers:
            # pos = (int(center[0]*scaler[0]+offset[0]), int(center[1]*scaler[1]+offset[1]))
            pos = center
            # image = cv2.circle(image, pos, radius, color, -1)
            image2 = image[pos[1] - box[1]: pos[1] + box[1], pos[0] - box[0]: pos[0] + box[0]]
            cropped_images.append(image2)
            # cv2.circle(image, pos, 20, (255,255,255), 3)
            
            # cv2.namedWindow('output', cv2.WINDOW_NORMAL)
            # cv2.imshow('output', image2)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
        
        # Test to validate centers (scalar, offset)
        # cv2.namedWindow('output', cv2.WINDOW_NORMAL)
        # cv2.imshow('output', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
            
        return cropped_images

    def find_numbers(self, image, catan_board : CatanBoard, box = (270, 270)):
        cropped_images = self.crop_to_hexes(image, catan_board, box)
        centers = [space.position for space in catan_board.empty_spaces if space.position != catan_board.desert_position]        
        positions = []
        
        for i, im in enumerate(cropped_images):
            gray_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

            # Apply GaussianBlur to reduce noise and improve circle detection
            blurred_image = cv2.GaussianBlur(gray_image, (9, 9), 2)

            # Use Hough Circle Transform to detect circles
            circles = cv2.HoughCircles(
                blurred_image,
                cv2.HOUGH_GRADIENT,
                dp=1,      # Inverse ratio of the accumulator resolution to the image resolution.
                minDist=50,  # Minimum distance between the centers of detected circles.
                param1=100, # Upper threshold for the internal Canny edge detector.
                param2=30,  # Threshold for center detection.
                minRadius=80, # Minimum radius of the detected circles.
                maxRadius=100 # Maximum radius of the detected circles.
            )
            
            # Draw the circles on the original image
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for j in circles[0, :]:
                    pos = [-box[0]+j[0]+centers[i][0], -box[1]+j[1]+centers[i][1]]
                    # cv2.circle(image, pos, 11, (255,255,255), 5)        
                    pos = self.convert_to_world_single(pos)
                    positions.append(Number(10, pos))
                    
        # cv2.namedWindow('output', cv2.WINDOW_NORMAL)
        # cv2.imshow('output', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return positions

    def find_piece(self, piece : Piece, image):
        # print(type(piece))
        pieces = []
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_image, piece.color[0], piece.color[1])
        result = cv2.bitwise_and(image, image, mask=mask)
        result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        
        contours, _ = cv2.findContours(result, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        contour_areas = [cv2.contourArea(contour) for contour in contours]
        # Find indices of largest contours
        indices_of_contours_in_range = [i for i, area in enumerate(contour_areas) if piece.area[0] <= area <= piece.area[1]]

        # Extract the largest contours
        largest_contours = [contours[i] for i in indices_of_contours_in_range]
        
        for contour in largest_contours:
            # Calculate moments
            M = cv2.moments(contour)

            # Calculate centroid
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            copied_piece = copy.deepcopy(piece)
            position = self.convert_to_world_single([cx,cy])
            copied_piece.position = position
            pieces.append(copied_piece)

            # Print or use centroid coordinates as needed
            # print(f"Center of mass: ({cx}, {cy})")

            # Optionally, draw a circle at the center of mass
            # image = cv2.circle(image, (cx, cy), 20, (255, 0, 0), 10)
                
        return pieces

    def find_pieces(self, pieces, image):
        piece_list = []
        for p in pieces:
            piece_list.extend(self.find_piece(p, image))
            
        return piece_list

    # need a complete board.
    def mask_board(self, image):
        contour = self.find_background(image)
        mask = np.zeros_like(image)
        cv2.drawContours(mask, contour,-1, (255), thickness=cv2.FILLED)
        
        return mask

    def construct_hexagon(self, center, sideLength):
        hexagon_vertices = []
        for i in range(6):
            x = int(center[0] + sideLength * np.cos(i * np.pi / 3))
            y = int(center[1] + sideLength * np.sin(i * np.pi / 3))
            hexagon_vertices.append((x, y))
            
        return hexagon_vertices

    def hexagon_mask(self, catan_board):
        # Define the size of the hexagon
        side_length = 1700

        # Calculate the coordinates of the hexagon vertices
        hexagon_center = (int(self.image.shape[1]/2), int(self.image.shape[0]/2)+100)  # Example center coordinates
        hexagon_vertices = self.construct_hexagon(hexagon_center, side_length)

        # Create a black image (initially all zeros) to serve as the mask
        mask = np.zeros_like(self.image[:, :, 0])

        # Fill the mask with a white hexagon
        cv2.fillConvexPoly(mask, np.array(hexagon_vertices), 255)

        # Apply the mask to the original image
        result_image = cv2.bitwise_and(self.image, self.image, mask=mask)
        
        # now apply to every single hex
        centers = [space.position for space in catan_board.empty_spaces if space.position != catan_board.desert_position]
        offset = (900, 1100)
        scaler = (200, 200)
        
        for center in centers:
            pos = (int(center[0]*scaler[0]+offset[0]), int(center[1]*scaler[1]+offset[1]))
            result_image = cv2.circle(result_image, (pos[0], pos[1]), 150, (0,0,0), -1)
            
        return result_image

    def display_on_image(self, cords):
        for cord in cords:
            pos = [int(cord.position[0]), int(cord.position[1])]
            image = cv2.circle(self.image, pos, 20, (255, 0, 0), 10)
            
        cv2.namedWindow('output', cv2.WINDOW_NORMAL)
        cv2.imshow('output', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def analyze_board(self, catan_board, pieces = []):
        # If there is a robber, we will only go for all of them? May need to change this
        if isinstance(pieces[0], Robber):
            locs = self.find_pieces(pieces, self.image)
        
        elif isinstance(pieces[0], Number):
            locs = self.find_numbers(self.image, catan_board)
        
        else:
            # If not a number or a robber we can mask
            treated_image = self.hexagon_mask(catan_board)
            locs = self.find_pieces(pieces, treated_image)
        
        return locs