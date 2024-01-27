from objects.Motor import *

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
        
class CameraRig():
    def __init__(self, camera : DCMotor, light: DCMotor):
        self.camera = camera
        self.light = light
        
    def take_picture(self):
        # turn light on
        # take picture
        # turn off light
        # return picture
        pass