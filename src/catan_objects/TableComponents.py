from catan_objects.Motor import *
from catan_objects.BoardComponents import *
from catan_objects.CatanBoard import CatanBoard

import numpy as np
import cv2
import copy

CENTER_OF_CAMERAS_CATAN_BOARD = (346,262)
# CENTER_OF_CAMERAS_CATAN_BOARD = (343,267)

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
        self.solenoid_1 = solenoid_1
        self.solenoid_2 = solenoid_2 # Ask owen if we can wire these in series

    def set_high_position(self):
        self.motor.move_to(self.maximum_value)
        
    def set_low_position(self):
        # move up to take away pressure on solenoids
        self.motor.move_to(self.maximum_value + 2)
        self.solenoid_1.start(1)
        self.solenoid_2.start(1)
        # Then move it alittle to allow us to stop sending current to the solenoid
        self.motor.move_to(self.minimum_value - 50)
        self.solenoid_1.stop(1)
        self.solenoid_2.stop(1)
        # Finish
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
    def __init__(self, camera : CameraModuleCatan, light: Lights, position = [0,0]):
        self.camera = camera
        self.light = light
        self.pose = position
        self.K = np.array([[324.76825238, 0. ,373.66404696], [0., 326.72841161, 247.07466765], [0., 0., 1., ]])
        self.D = np.array([[-0.31685422,  0.11733933, -0.00043777,  0.00120568, -0.02182481]])
        self.H = np.array([[ 1.26468616e-02,  9.99554797e-01,  1.93688909e+02], [-1.00500787e+00, -2.03228976e-02,  2.70416347e+02],[ 7.01118413e-05, -2.21403641e-05,  1.00000000e+00]])
        self.image = None
        self.relative_catan_board = None
        
    def take_picture(self):
        # turn light on
        self.light.start()
        # take picture
        self.camera.take_picture()
        # turn off light
        self.light.stop()
        # Load and undistort picture
        self.load_image('Catable_Image.jpg')
        #self.load_image('Catable_Image.jpg')
        self.undistort_picture()
        
    def undistort_picture(self):
        # Can use Knew to change scale so it fits
        h, w = self.image.shape[:2]
        new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(self.K, self.D, (w,h), 0, (w,h))
        self.image = cv2.undistort(self.image, cameraMatrix=self.K, distCoeffs=self.D, newCameraMatrix=new_camera_matrix)

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
    
    def rotate_empty_spaces(self, center, angle = 90):
        angle_radians = math.radians(angle)
        
        for space in self.relative_catan_board.empty_spaces:
            pos = space.position
            qx = center[0] + math.cos(angle_radians) * (pos[0] - center[0]) - math.sin(angle_radians) * (pos[1] - center[1])
            qy = center[1] + math.sin(angle_radians) * (pos[0] - center[0]) + math.cos(angle_radians) * (pos[1] - center[1])
            space.position = [qx, qy]
    
    def find_desert(self, catan_board_keep, catan_board_to_update, box = (40,50)):
        self.relative_catan_board = catan_board_keep
        self.rotate_empty_spaces([CENTER_OF_CAMERAS_CATAN_BOARD[0], CENTER_OF_CAMERAS_CATAN_BOARD[1]], -90)
        
        hex_images = self.crop_to_hexes(self.image, box, True)
        pixel_counts = []
        desert_hsv = [(139, 69, 147), (169 , 114, 210)]
        for image in hex_images:
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv_image, desert_hsv[0], desert_hsv[1])
            pixel_counts.append(cv2.countNonZero(mask))
            
        index = pixel_counts.index(max(pixel_counts))
        self.relative_catan_board.empty_spaces[index].stack[0].is_desert = True
        
        catan_board_to_update.empty_spaces[index].stack[0].is_desert = True

    def threshold_between_values(self, image, thresh_min, thresh_max):
        # Finding two thresholds and then finding the common part
        _, threshold = cv2.threshold(image, thresh_min, 255, cv2.THRESH_BINARY)
        _, threshold2 = cv2.threshold(image, thresh_max, 255, cv2.THRESH_BINARY_INV)
        return cv2.bitwise_and(threshold, threshold2)

    def threshold_in_range(self, image, threshold_range):
        return self.threshold_between_values(image, threshold_range[0], threshold_range[1])

    def find_background(self, image):
        h, s, v = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2HSV))
        blue = [100, 115]
        background = self.threshold_in_range(h, blue)
        background = cv2.morphologyEx(background, cv2.MORPH_DILATE, np.ones((7, 7), np.uint8))
        contours, hierarchy = cv2.findContours(background, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
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

    def crop_to_hexes(self, image, box, want_desert = False):
        if want_desert:
            centers = [space.position for space in self.relative_catan_board.empty_spaces]
        else:
            centers = [space.position for space in self.relative_catan_board.empty_spaces if not space.stack[0].is_desert]
        
        cropped_images = []

        for center in centers:
            pos = (int(center[0]), int(center[1]))
            # image = cv2.circle(image, pos, 10, (255,0,0), -1)
            image2 = image[pos[1] - box[1]: pos[1] + box[1], pos[0] - box[0]: pos[0] + box[0]]
            cropped_images.append(image2)
            #cv2.circle(image, pos, 10, (255,255,255), 3)
            
            #cv2.namedWindow('output', cv2.WINDOW_NORMAL)
            #cv2.imshow('output', image2)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
        
        # Test to validate centers (scalar, offset)
        #cv2.namedWindow('output', cv2.WINDOW_NORMAL)
        #cv2.imshow('output', image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
            
        return cropped_images

    def find_numbers(self, image, box = (40, 50)):
        cropped_images = self.crop_to_hexes(self.image, box)
        centers = [space.position for space in self.relative_catan_board.empty_spaces if not space.stack[0].is_desert]        
        positions = []
        
        number_hsv = [(83, 51, 155), (174 , 103, 255)]
        
        for i, im in enumerate(cropped_images):
            #cv2.namedWindow('output', cv2.WINDOW_NORMAL)
            #cv2.imshow('output', im)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            
            hsv_image = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv_image, number_hsv[0], number_hsv[1])
            result = cv2.bitwise_and(im, im, mask=mask)
            gray_image = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
            
            # Apply GaussianBlur to reduce noise and improve circle detection
            blurred_image = cv2.GaussianBlur(gray_image, (7, 7), 1)
            # cv2.namedWindow('output', cv2.WINDOW_NORMAL)
            # cv2.imshow('output', blurred_image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            
            # Use Hough Circle Transform to detect circles
            circles = cv2.HoughCircles(
                blurred_image,
                cv2.HOUGH_GRADIENT,
                dp=1.70,      # Inverse ratio of the accumulator resolution to the image resolution.
                minDist=80,  # Minimum distance between the centers of detected circles.
                param1=120, # Upper threshold for the internal Canny edge detector.
                param2=26,  # Threshold for center detection.
                minRadius=9, # Minimum radius of the detected circles.
                maxRadius=17 # Maximum radius of the detected circles.
            )
            
            # Draw the circles on the original image
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for j in circles[0, :]:
                    # cv2.circle(blurred_image, (int(j[0]), int(j[1])), 11, (255,255,255), 1) 
                    pos = [int(-box[0]+j[0]+centers[i][0]), int(-box[1]+j[1]+centers[i][1])]
                    #cv2.circle(image, pos, j[2], (255,255,255), 1)        
                    pos = self.convert_to_world_single(pos)
                    positions.append(Number(10, pos))
            else:
                # basically we're going to guess
                pos = [int(centers[i][0]),int(centers[i][1])]
                #cv2.circle(image, pos, 10, (255,0,0), 3)    
                pos = self.convert_to_world_single(pos)
                positions.append(Number(10, pos)) 
                    
        #cv2.namedWindow('output', cv2.WINDOW_NORMAL)
        #cv2.imshow('output', image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        return positions

    def find_piece(self, piece : Piece, image):
        # print(type(piece))
        pieces = []
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_image, piece.color[0], piece.color[1])
        result = cv2.bitwise_and(image, image, mask=mask)
        result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        
        #cv2.namedWindow('output', cv2.WINDOW_NORMAL)
        #cv2.imshow('output', result)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        
        contours, _ = cv2.findContours(result, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        contour_areas = [cv2.contourArea(contour) for contour in contours]
        # Find indices of largest contours
        indices_of_contours_in_range = [i for i, area in enumerate(contour_areas) if piece.area[0] <= area <= piece.area[1]]

        # Extract the largest contours
        largest_contours = [contours[i] for i in indices_of_contours_in_range]
        output = self.image.copy()
        for contour in largest_contours:
            approx = cv2.approxPolyDP(contour, 0.05 * cv2.arcLength(contour, True), True)
            if len(approx) >= piece.edges[0] and len(approx) <= piece.edges[1]:
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
                # cv2.circle(self.image, (cx, cy), 5, (255, 255, 255), -1)
                #cv2.drawContours(output, [approx], -1, (0, 255, 0), 3)
                #text = "num_pts={} area ={}".format(len(approx), cv2.contourArea(contour))
                #cv2.putText(output, text, (cx, cy - 15), cv2.FONT_HERSHEY_SIMPLEX,
                #    0.4, (0, 255, 0), 1)
            
        #cv2.namedWindow('output', cv2.WINDOW_NORMAL)
        #cv2.imshow('output', output)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
                
        return pieces

    def find_pieces(self, pieces, image):
        piece_list = []
        for p in pieces:
            piece_list.extend(self.find_piece(p, image))
            
        return piece_list

    # need a complete board.
    def mask_board(self):
        contour = self.find_background(self.image)
        mask = cv2.inRange(self.image, (0,0,0), (0,0,0))
        cv2.drawContours(mask, [contour],-1, (255,255,255), thickness=cv2.FILLED)
        # cv2.namedWindow('output', cv2.WINDOW_NORMAL)
        # cv2.imshow('output', mask)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        mask = cv2.bitwise_and(self.image, self.image, mask=mask)
        
        return mask

    def construct_hexagon(self, center, sideLength):
        hexagon_vertices = []
        for i in range(6):
            x = int(center[0] + sideLength * np.cos(i * np.pi / 3))
            y = int(center[1] + sideLength * np.sin(i * np.pi / 3))
            hexagon_vertices.append((x, y))
            
        return hexagon_vertices

    def hexagon_mask(self, find_background = True, small_hexes = True):
        if find_background:
            result_image = self.mask_board()
        else:
            side_length = 225

            # Calculate the coordinates of the hexagon vertices
            hexagon_vertices = self.construct_hexagon([CENTER_OF_CAMERAS_CATAN_BOARD[0], CENTER_OF_CAMERAS_CATAN_BOARD[1]], side_length)

            # Create a black image (initially all zeros) to serve as the mask
            mask = np.zeros_like(self.image[:, :, 0])

            # Fill the mask with a white hexagon
            cv2.fillConvexPoly(mask, np.array(hexagon_vertices), 255)
            result_image = cv2.bitwise_and(self.image, self.image, mask=mask)
        if small_hexes == True:
            # now apply to every single hex
            centers = [space.position for space in self.relative_catan_board.empty_spaces]
            
            for center in centers:
                result_image = cv2.circle(result_image, (int(center[0]), int(center[1])), 27, (0,0,0), -1)
            
        return result_image
    
    def show_image(self):    
        cv2.namedWindow('output', cv2.WINDOW_NORMAL)
        cv2.imshow('output', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def display_on_image(self, cords):
        for cord in cords:
            pos = [int(cord.position[0]), int(cord.position[1])]
            image = cv2.circle(self.image, pos, 20, (255, 0, 0), 10)
            
        cv2.namedWindow('output', cv2.WINDOW_NORMAL)
        cv2.imshow('output', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def analyze_board(self, pieces = []):
        # If there is a robber, we will only go for all of them? May need to change this
        if isinstance(pieces[0], Robber):
            treated_image = self.mask_board()
            locs = self.find_pieces(pieces, treated_image)
        
        elif isinstance(pieces[0], Number):
            #self.show_image()
            locs = self.find_numbers(self.image)
        
        else:
            # If not a number or a robber we can mask
            treated_image = self.hexagon_mask(True, True)
            locs = self.find_pieces(pieces, treated_image)
        
        return locs