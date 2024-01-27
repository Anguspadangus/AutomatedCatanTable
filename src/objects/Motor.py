from abc import abstractmethod, ABC
import json
import time

# TEST CLASSES
class MotorKit():
    def __init__(self, address):
        self.address = address
        self.stepper1 = "A"
        self.stepper2 = "B"
        self.motor_M1 = "M1"
        
class stepper():
    def __init__(self):
        self.FORWARD = "F"
        self.BAKCWARD = "B"
        
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
        if i <= 5:
            motor.onestep(direction=direction, style=stepper.MICROSTEP)
            time.sleep(0.0001)
        else:
            motor.onestep(direction=direction, style=stepper.SINGLE)
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
    def __init__(self, steps_per_rotation, transalor, setup_function, control_function, *args):
        super().__init__(setup_function)
        self.distance_per_step = transalor / steps_per_rotation # mm/step
        self.current_cartisan = 0.0
        self.control_function = control_function
        self.control_args = args
        
    def move_to(self, value):
        steps = self.position_to_steps(value)
        
        self.control_function(steps, *self.control_args)
        
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
        self.motor = super().__init__(setup_function)
    
    def start(self, throttle):
        self.motor.throttle = throttle
        pass
    
    def stop(self):
        self.motor.throttle = 0
        pass
    
    # If there is a need to save and load these motors, we'll do it
    def save(self, name):
        pass
    
    def load(self, name):
        pass