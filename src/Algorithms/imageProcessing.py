import cv2
import numpy as np
from objects.BoardComponents import *
from objects.StandardBoard import StandardSetup
from objects.Board import Board

def threshold_between_values(image, thresh_min, thresh_max):
    # Finding two thresholds and then finding the common part
    _, threshold = cv2.threshold(image, thresh_min, 255, cv2.THRESH_BINARY)
    _, threshold2 = cv2.threshold(image, thresh_max, 255, cv2.THRESH_BINARY_INV)
    return cv2.bitwise_and(threshold, threshold2)


def threshold_in_range(image, threshold_range):
    return threshold_between_values(image, threshold_range[0], threshold_range[1])


def find_background(image):
    h, s, v = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2HSV))
    blue = [0.5 * 180, 0.65 * 180]
    background = threshold_in_range(h, blue)
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

    # Największym konturem jest prawie zawsze cała plansza.
    # Drugim co do wielkości jest plansza z wyciętą wodą, która by nas bardziej interesowała.
    # Jednak na niektórych zdjęciach oba te kontury się zlewają w jeden, więc nie możemy zawsze brać tego mniejszego.
    # If the second biggest contour is inside the biggest one take the inside one
    if hierarchy[0][second_max_area_index][3] == max_area_index:
        best_contour = contours[second_max_area_index]
    else:
        best_contour = contours[max_area_index]
    return best_contour

def convert_image_to_space(image):
    # https://nilesh0109.medium.com/camera-image-perspective-transformation-to-different-plane-using-opencv-5e389dd56527
    pass

def undistort_image(image):
    # DIM=XXX
    # K=np.array(YYY)
    # D=np.array(ZZZ)
    # h,w = image.shape[:2]
    # map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    # undistorted_img = cv2.remap(image, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return image

def load_image(filepath = 'src\\test\\images\\robber1.jpeg'):
    image = cv2.imread(filepath)
    return image

def crop_to_hexes(image, board : Board):
    centers = [space.shape.xy for space in board.empty_spaces if space.shape.xy != board.desert_position]
    offset = (900, 1100)
    scaler = (200, 200)
    box = (250, 250)
    
    cropped_images = []
    
    color = (0,255,0)
    radius = 50
    for center in centers:
        pos = (int(center[0]*scaler[0]+offset[0]), int(center[1]*scaler[1]+offset[1]))
        # image = cv2.circle(image, pos, radius, color, -1)
        image2 = image[pos[1] - box[1]: pos[1] + box[1], pos[0] - box[0]: pos[0] + box[0]]
        cropped_images.append(image2)
        
    return cropped_images

def find_numbers(image, board : Board):
    cropped_images = crop_to_hexes(image, board)
    centers = [space.shape.xy for space in board.empty_spaces if space.shape.xy != board.desert_position]
    offset = (900, 1100)
    scaler = (200, 200)
    box = (250, 250)
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
                pos = [offset[0]-box[0]+j[0]+int(centers[i][0]*scaler[0]), offset[1]-box[1]+j[1]+int(centers[i][1]*scaler[1])]
                positions.append([Number(10), pos])
            
    return positions

def find_piece(piece : Piece, image):
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

        pieces.append([piece, [cx,cy]])
        # Print or use centroid coordinates as needed
        # print(f"Center of mass: ({cx}, {cy})")

        # Optionally, draw a circle at the center of mass
        # image = cv2.circle(image, (cx, cy), 20, (255, 0, 0), 10)
            
    return pieces

def find_pieces(pieces, image):
    piece_list = []
    for p in pieces:
        piece_list.extend(find_piece(p, image))
        
    return piece_list

# need a complete board.
def mask_board(image):
    contour = find_background(image)
    mask = np.zeros_like(image)
    cv2.drawContours(mask, contour,-1, (255), thickness=cv2.FILLED)
    
    return mask

def construct_hexagon(center, sideLength):
    hexagon_vertices = []
    for i in range(6):
        x = int(center[0] + sideLength * np.cos(i * np.pi / 3))
        y = int(center[1] + sideLength * np.sin(i * np.pi / 3))
        hexagon_vertices.append((x, y))
        
    return hexagon_vertices

def hexagon_mask(image, board):
    # Define the size of the hexagon
    side_length = 1700

    # Calculate the coordinates of the hexagon vertices
    hexagon_center = (int(image.shape[1]/2), int(image.shape[0]/2)+100)  # Example center coordinates
    hexagon_vertices = construct_hexagon(hexagon_center, side_length)

    # Create a black image (initially all zeros) to serve as the mask
    mask = np.zeros_like(image[:, :, 0])

    # Fill the mask with a white hexagon
    cv2.fillConvexPoly(mask, np.array(hexagon_vertices), 255)

    # Apply the mask to the original image
    result_image = cv2.bitwise_and(image, image, mask=mask)
    
    # now apply to every single hex
    centers = [space.shape.xy for space in board.empty_spaces if space.shape.xy != board.desert_position]
    offset = (900, 1100)
    scaler = (200, 200)
    
    for center in centers:
        pos = (int(center[0]*scaler[0]+offset[0]), int(center[1]*scaler[1]+offset[1]))
        result_image = cv2.circle(result_image, (pos[0], pos[1]), 150, (0,0,0), -1)
        
    return result_image

def display_on_image(cords, image):
    for cord in cords:
        image = cv2.circle(image, cord[1], 20, (255, 0, 0), 10)
        
    cv2.namedWindow('output', cv2.WINDOW_NORMAL)
    cv2.imshow('output', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def analyze_board(board, image, pieces = []):
    image = undistort_image(image)
    treated_image = hexagon_mask(image, board)
    robber = None
    for i, obj in enumerate(pieces):
        if isinstance(obj, Robber):
            robber = pieces.pop(i)
    locs = find_pieces(pieces, treated_image)
    if robber is not None:
        locs.extend(find_pieces([robber], image))
        
    locs.extend(find_numbers(image, board))
    
    return locs


if __name__ == "__main__":
    b = StandardSetup()
    b.desert_position = b.empty_spaces[5].shape.xy # for testing
    image = load_image()
    pieces = [Road('red'), Settlememt('red'), City('red'),
            Road('blue'), Settlememt('blue'), City('blue'),
            Road('white'), Settlememt('white'), City('white'),
            Road('orange'), Settlememt('orange'), City('orange'), Robber()]
    locs = analyze_board(b, image, pieces)
    display_on_image(locs, image)
