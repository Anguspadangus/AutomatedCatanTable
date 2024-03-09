from abc import abstractmethod, ABC
import json
import time

# TEST CLASSES
class MotorKit():
    def __init__(self, address):
        self.address = address
        self.stepper1 = stepper("A")
        self.stepper2 = stepper("B")
        self.motor_M1 = Basic_DC_Motor("M1")
        self.motor_M2 = Basic_DC_Motor("M2")
        self.motor_M3 = Basic_DC_Motor("M3")
        
class Basic_DC_Motor():
    def __init__(self, type) -> None:
        self.type = type
        self.throttle = 0
        
class stepper():
    FORWARD = "F"
    BAKCWARD = "B"
    MICROSTEP = 0
    SINGLE = 1
    
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

def GPIO_SETUP(MOTOR_DIRECTION_PIN, MOTOR_STEP_PIN):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOTOR_DIRECTION_PIN, GPIO.OUT)  # Direction
    GPIO.setup(MOTOR_STEP_PIN, GPIO.OUT)       # Step

def GPIO_CONTROL(steps, MOTOR_DIRECTION_PIN, MOTOR_STEP_PIN):
    if steps < 0:
        GPIO.output(MOTOR_DIRECTION_PIN, GPIO.LOW)   # Set to LOW for counterclockwise
    else:
        GPIO.output(MOTOR_DIRECTION_PIN, GPIO.HIGH)  # Set to HIGH for clockwise
    
    steps = abs(int(steps))
    
    for i in range(steps):
        GPIO.output(MOTOR_STEP_PIN, GPIO.HIGH)
        time.sleep(0.0005)
        GPIO.output(MOTOR_STEP_PIN, GPIO.LOW)
        time.sleep(0.0005)

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
    
    for i in range(steps):
        # Switch to microstepping for the last 5 steps
        if i >= steps - 5:
            motor.onestep(direction=direction, style=stepper.MICROSTEP)
            time.sleep(0.0001)
        else:
            motor.onestep(direction=direction, style=stepper.SINGLE)
            time.sleep(0.0001)

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
    
    for i in range(max(steps_1, steps_2)):
        if i <= steps_1:
            if i >= steps_1 - 5:
                motor_1.onestep(direction=direction_1, style=stepper.MICROSTEP)
                time.sleep(0.0001)
            else:
                motor_1.onestep(direction=direction_1, style=stepper.SINGLE)
                time.sleep(0.0001)
                
        if i <= steps_2:
            if i >= steps_2 - 5:
                motor_2.onestep(direction=direction_2, style=stepper.MICROSTEP)
                time.sleep(0.0001)
            else:
                motor_2.onestep(direction=direction_2, style=stepper.SINGLE)
                time.sleep(0.0001)

class Motor(ABC):
    
    s_hats = {}
    
    def __init__(self, setup):
        self.motor = setup
        
    @abstractmethod
    def save(self, name):
        pass
    
    @abstractmethod
    def load(self, name):
        pass

class Stepper(Motor):
    # The translator is the attachment to the motor, example a timing pully has 20 teeth per rotation
    # each spaced 2 mm. So the translator is 20 teeth/rotation * 2 mm/tooth = 40 mm/rotation
    def __init__(self, steps_per_rotation, translator, setup_function, control_function, *args):
        super().__init__(setup_function)
        self.distance_per_step = translator / steps_per_rotation # mm/step
        self.current_cartisan = 0.0
        self.control_function = control_function
        self.control_args = args
        
    def move_to(self, value):
        steps = self.position_to_steps(value)
        
        self.control_function(self.motor, steps, *self.control_args)
        
        self._set_current_cartisan(value)
           
    def position_to_steps(self, coordinate):
        return (coordinate - self.current_cartisan) / self.distance_per_step # steps
    
    def save(self, name):
        with open('src\Algorithms\desertPosition.json', 'w') as f:
            json.dump({f"{name}" :self.current_cartisan}, f) 
            
    def load(self, name):
        f = open('src\Algorithms\desertPosition.json')
        data = json.load(f)
        f.close()
        self.current_cartisan = data[f"{name}"]
    
    def _set_current_cartisan(self, value):
        self.current_cartisan = value
        
class DCMotor(Motor):
    def __init__(self, setup_function):
       super().__init__(setup_function)
    
    def start(self, throttle):
        self.motor.throttle = throttle
    
    def stop(self):
        self.motor.throttle = 0
    
    # If there is a need to save and load these motors, we'll do it
    def save(self, name):
        pass
    
    def load(self, name):
        pass
    
class LinkedMotor(Motor):
    def __init__(self, motor_1, motor_2, linking_function):
        self.motor_1 = motor_1
        self.motor_2 = motor_2
        self.control_function = linking_function
        
    def move_to(self, value : list):
        steps_1 = self.motor_1.position_to_steps(value[0])
        steps_2 = self.motor_1.position_to_steps(value[1])
        
        self.control_function(self.motor_1, self.motor_2, steps_1, steps_2)
        
        self.motor_1._set_current_cartisan(value[0])
        self.motor_2._set_current_cartisan(value[1])
        
    def save(self, name_1, name_2):
        self.motor_1.save(name_1)
        self.motor_2.save(name_2)
        
    def load(self, name_1, name_2):
        self.motor_1.load(name_1)
        self.motor_2.load(name_2)