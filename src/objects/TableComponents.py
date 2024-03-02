from objects.Motor import *

import numpy as np
import cv2

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
    def __init__(self, motor, maximum_value, minimum_value, solenoid_1: SingleDegreeComponent, solenoid_2: SingleDegreeComponent):
        super().__init__(motor, maximum_value, minimum_value)
        # self.lift = lift #if we make this a list we can have as many lead screws as we need
        self.solenoid_1 = solenoid_1
        self.solenoid_2 = solenoid_2 # Ask owen if we can wire these in series

    def set_high_position(self):
        self.motor.move_to(self.maximum_value)
        self.solenoid_1.set_low_position()
        self.solenoid_2.set_low_position()
        
    def set_low_position(self):
        self.solenoid_1.set_high_position()
        self.solenoid_2.set_high_position()
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
    def __init__(self, camera : DCMotor, light: DCMotor, position = [0,0]):
        self.camera = camera
        self.light = light
        self.pose = position
        self.K = np.array([[113.49354735654141, 0.0, 371.5786534104595], [0.0, 116.6060998517777, 205.3861581256824], [0.0, 0.0, 1.0]])
        self.D = np.array([[0.12694667308062602], [0.6454345033192549], [-0.5465056949757663], [0.25172851391836865]])
        self.H = np.array([[ 3.98379589e-01, 8.28098023e-02, 5.48000000e+02], [-6.12605764e-03,-3.84345357e-01, 1.03000000e+02], [-6.28872633e-05, 2.09711523e-04, 1.00000000e+00]])
        self.picture = None
        
    def take_picture(self):
        # TODO owen
        # turn light on
        # take picture
        # turn off light
        # self.picture = undistort_picture(picture)
        pass
    
    def undistort_picture(self, picture):
        # Can use Knew to change scale so it fits
        self.picture = cv2.fisheye.undistortImage(picture, self.K, D=self.D)
    
    def convert_to_world(self, position_camera_space):
        position_camera_space = cv2.convertPointsToHomogeneous(position_camera_space)
        world_space = np.matmul(np.linalg.inv(self.H), position_camera_space)

        w_x = world_space[0] / world_space[2]
        w_y = world_space[1] / world_space[2]

        # TODO: Rotation component
        
        # Adding position, the rotation and position probably need to be defined as a matrix that we multiply
        w_x = w_x + self.pose[0]
        w_y = w_y + self.pose[1]
        
        return [w_x,w_y]