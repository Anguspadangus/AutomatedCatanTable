from catan_objects.TableComponents import CameraRig
from catan_objects.BoardComponents import *
from integration_test.integration_setup import Setup
import cv2
import copy
import math


cam = CameraRig(None, None, [0,0])
cam.load_image('src\\integration_test\\images\\image_training\\pieces3.jpg')
cam.undistort_picture()
A_pos = [345,105]
catan_board_cam = Setup(A_pos)
catan_board_real = Setup([0,0])

cam.find_desert(catan_board_cam, catan_board_real, (40,50))
# numbers = cam.find_numbers(cam.image, (40, 45))
cam.analyze_board([Road('blue')])