from objects.Motor import Motor
from objects.BoardComponents import *

class Mount():
    def __init__(self):
        pass

class Gantry():
    def __init__(self, x_motor: Motor, y_motor: Motor, mount: Mount):
        self.x_motor_1 = x_motor
        self.y_motor = y_motor
        self.mount = mount
        
    def move_to(self, location):
        # https://github.com/adafruit/Adafruit_Motor_Shield_V2_Library/blob/master/examples/Accel_MultiStepper/Accel_MultiStepper.ino
        pass
    
    def pick_up(self, object):
        self.move_to(object)
        
        pass
        
