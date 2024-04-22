import cv2
import numpy as np

from catan_objects.TableComponents import CameraRig
from catan_objects.BoardComponents import *
from integration_test.integration_setup import Setup

# cam = CameraRig(None, None, [0,0])
# # cam.load_image('src\\integration_test\\images\\image_training\\robber1_1_filter.jpg') # to get the mask
# cam.load_image('src\\integration_test\\images\\image_training\\numbers1.jpg') 
# cam.undistort_picture()
# A_pos = [345,105]
# catan_board_cam = Setup(A_pos)
# catan_board_real = Setup([0,0])
# cam.find_desert(catan_board_cam, catan_board_real, (40,50))

# image = cam.hexagon_mask(False, True)

image = cv2.imread('Catable_Image.jpg')

def nothing(x):
    pass

# Create a window
cv2.namedWindow('image')

# Create trackbars for color change
# Hue is from 0-179 for Opencv
cv2.createTrackbar('HMin', 'image', 0, 179, nothing)
cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
cv2.createTrackbar('VMax', 'image', 0, 255, nothing)

# hsv_ = [(0,0,0), (179,255,255)]
hsv_ = [(83, 51, 155), (174 , 103, 255)]

# Set default value for Max HSV trackbars
cv2.setTrackbarPos('HMin', 'image', hsv_[0][0])
cv2.setTrackbarPos('SMin', 'image', hsv_[0][1])
cv2.setTrackbarPos('VMin', 'image', hsv_[0][2])
cv2.setTrackbarPos('HMax', 'image', hsv_[1][0])
cv2.setTrackbarPos('SMax', 'image', hsv_[1][1])
cv2.setTrackbarPos('VMax', 'image', hsv_[1][2])

# Initialize HSV min/max values
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

while(1):
    # Get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin', 'image')
    sMin = cv2.getTrackbarPos('SMin', 'image')
    vMin = cv2.getTrackbarPos('VMin', 'image')
    hMax = cv2.getTrackbarPos('HMax', 'image')
    sMax = cv2.getTrackbarPos('SMax', 'image')
    vMax = cv2.getTrackbarPos('VMax', 'image')

    # Set minimum and maximum HSV values to display
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # Convert to HSV format and color threshold
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(image, image, mask=mask)

    # Print if there is a change in HSV value
    if((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
        print("(%d, %d, %d), (%d , %d, %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
        phMin = hMin
        psMin = sMin
        pvMin = vMin
        phMax = hMax
        psMax = sMax
        pvMax = vMax

    # Display result image
    cv2.imshow('image', result)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()