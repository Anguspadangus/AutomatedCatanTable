import cv2
import numpy as np
from objects.TableComponents import CameraRig
from objects.Motor import *

global_x, global_y = None, None

def on_mouse_click(event, x, y, flags, param):
    global global_x, global_y
    if event == cv2.EVENT_LBUTTONDOWN:
        global_x = x
        global_y = y
        print(f'x: {x}\ny: {y}')
        cv2.destroyAllWindows()

cam = CameraRig(DCMotor(HAT_SETUP("motor_M1")), DCMotor(HAT_SETUP("motor_M2")), [150.,200.,476.25])
picture = cv2.imread('src\\calibration_methods\\calibration_images\\RealTest.jpg')
cam.undistort_picture(picture)
# cam.picture = picture

cv2.namedWindow(winname = "Title of Popup Window") 
cv2.setMouseCallback("Title of Popup Window", on_mouse_click) 

while True: 
    cv2.imshow("Title of Popup Window", cam.picture) 
      
    if cv2.waitKey(0): 
        break

coords = cam.convert_to_world_2(np.array([global_x, global_y]), 476.25)
print(coords)

# K = np.array([[500., 0.0, 320.],
#               [0.0, 525., 220.],
#               [0.0, 0.0, 1.0]])

# # zero distortion coefficients work well for this image
# D = np.array([0.0, 0.0, 0.0, 0.0])

# # use Knew to scale the output
# Knew = K.copy()
# Knew[(0,1), (0,1)] = 0.85 * Knew[(0,1), (0,1)]


# img = cv2.imread('src\\test\\test_calibration_cropped.jpg')
# img_undistorted = cv2.fisheye.undistortImage(img, K, D=D, Knew=Knew)
# # cv2.imwrite('src\\test\\fisheye_sample_undistorted.jpg', img_undistorted)
# cv2.imshow('undistorted', img_undistorted)
# cv2.waitKey()

# cam.convert_to_world(pixels, 0)

# K = np.array([[  689.21,     0.  ,  1295.56],
#               [    0.  ,   690.48,   942.17],
#               [    0.  ,     0.  ,     1.  ]])

# # zero distortion coefficients work well for this image
# D = np.array([0., 0., 0., 0.])

# # use Knew to scale the output
# Knew = K.copy()
# Knew[(0,1), (0,1)] = 0.4 * Knew[(0,1), (0,1)]


# img = cv2.imread('src\\test\\fisheye_sample.jpg')
# img_undistorted = cv2.fisheye.undistortImage(img, K, D=D, Knew=Knew)
# cv2.imwrite('src\\test\\fisheye_sample_undistorted.jpg', img_undistorted)
# cv2.imshow('undistorted', img_undistorted)
# cv2.waitKey()