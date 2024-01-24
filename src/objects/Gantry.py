from objects.Motor import *
from objects.BoardComponents import *

class PumpAssembly():
    def __init__(self, valve: DCMotor, intake: DCMotor, outtake: DCMotor = None):
        self.valve = valve
        self.intake = intake
        self.intake = outtake
        
    def suction():
        pass
    
    def release():
        pass
    
    def blow():
        pass    
        
class Mount():
    def __init__(self, z_motor: Stepper, right_pump_assemply: PumpAssembly, left_pump_assembly: PumpAssembly,
                 right_gribber_type = 'cup', left_gripper_type = 'universal', max_position = 100):
        self.z_motor = z_motor
        self.right_pump_assembly = right_pump_assemply
        self.left_pump_assembly = left_pump_assembly
        self.right_gribber_type = right_gribber_type
        self.left_gripper_type = left_gripper_type
        self.max_position = max_position
        self.mount_dimensions = [0]
        
    def return_to_even(self):
        pass
    
    def pick_up(self, suckable, tile_stack):
        if suckable.gripper_type == self.right_gribber_type:
            self.z_motor.move_to(self.max_position - (suckable.height + tile_stack.height))
            self.right_pump_assembly.suction()
            self.return_to_even()
        if suckable.gripper_type == self.left_gribber_type:
            self.z_motor.move_to(-self.max_position + (suckable.height + tile_stack.height))
            self.left_pump_assembly.suction()
            self.return_to_even()
    
    def place(self, suckable, tile_stack):
        if suckable.gripper_type == self.right_gribber_type:
            self.z_motor.move_to(self.max_position - (suckable.height + tile_stack.height))
            self.right_pump_assembly.release()
            self.return_to_even()
        if suckable.gripper_type == self.left_gribber_type:
            self.z_motor.move_to(-self.max_position + (suckable.height + tile_stack.height))
            self.left_pump_assembly.release()
            self.left_pump_assembly.blow()
            self.left_pump_assembly.release()
            self.return_to_even()
        
        

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
        
