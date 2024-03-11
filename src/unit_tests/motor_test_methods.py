from catan_objects.Motor import Motor

"""
These are test methods for adafruit motor kit, when we are ready for integration tests we won't use these methods
"""

class MotorKit():
    def __init__(self, address):
        self.address = address
        self.stepper1 = stepper("A")
        self.stepper2 = stepper("B")
        self.motor_M1 = Basic_DC_Motor("M1")
        self.motor_M2 = Basic_DC_Motor("M2")
        self.motor_M3 = Basic_DC_Motor("M3")
        self.motor_M4 = Basic_DC_Motor("M4")
        
class Basic_DC_Motor():
    def __init__(self, type) -> None:
        self.type = type
        self.throttle = 0
        
class stepper():
    FORWARD = "F"
    BAKCWARD = "B"
    MICROSTEP = 0
    SINGLE = 1
    DOUBLE = 2
    
    def __init__(self, type):
        self.type = type
    
    def onestep(self, direction, style):
        pass
        
class GPIO():
    BCM = 0
    OUT = 0
    LOW = 0
    HIGH = 0
        
    def __init__(self):
        pass
        
    def setmode(self, *args):
        pass
    def setup(self, *args):
        pass
    def output(self, *args):
        pass
    
def gpio_cleanup():
    pass
# TEST CLASSES

def GPIO_CONTROL(steps, MOTOR_DIRECTION_PIN, MOTOR_STEP_PIN):
    if steps < 0:
        GPIO.output(MOTOR_DIRECTION_PIN, GPIO.LOW)   # Set to LOW for counterclockwise
    else:
        GPIO.output(MOTOR_DIRECTION_PIN, GPIO.HIGH)  # Set to HIGH for clockwise
    
    steps = abs(int(steps))

def GPIO_DESTRUCTOR():
    # call on __del__()
    gpio_cleanup()

def HAT_SETUP(type, address = '0x60'):
    if address not in Motor.s_hats:
        Motor.s_hats[address] = MotorKit(address)
        
    try:
        motor = getattr(Motor.s_hats[address], type)
    except AttributeError:
        motor = None
        
    return motor

def HAT_CONTROL(motor, steps):
    if steps > 0:
        direction = stepper.FORWARD
    else:
        direction = stepper.BAKCWARD
        
    steps = abs(int(steps))
    
def LINKED_HAT_CONTROL(motor_1, motor_2, steps_1, steps_2):
    if steps_1 > 0:
        direction_1 = stepper.FORWARD
    else:
        direction_1 = stepper.BAKCWARD
        
    if steps_2 > 0:
        direction_2 = stepper.FORWARD
    else:
        direction_2 = stepper.BAKCWARD
        
    steps_1 = abs(int(steps_1))
    steps_2 = abs(int(steps_2))
