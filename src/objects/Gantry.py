from objects.Motor import *
from objects.BoardComponents import *
from objects.Board import Board

class PumpAssembly():
    def __init__(self, valve: DCMotor, intake: DCMotor, outtake: DCMotor = None):
        self.valve = valve
        self.intake = intake
        self.outake = outtake
        
    def suction(self, throttle = 1.0, sleep = 0.0):
        self.valve.low()
        self.intake.start(throttle)
        time.sleep(sleep)
    
    def release(self):
        if self.intake.motor.throttle != 0:
            self.intake.stop()
        elif self.outake.motor.throttle != 0:
            self.outake.stop()
    
    def blow(self, throttle = 1.0, sleep = 0.0):
        self.valve.high()
        self.outake.start(throttle)   
        time.sleep(sleep)
        
class Mount():
    def __init__(self, z_motor: Stepper, right_pump_assemply: PumpAssembly, left_pump_assembly: PumpAssembly, max_height = 40, offset = 28,
                 right_suction_type = 'cup', left_suction_type = 'universal'):
        self.z_motor = z_motor
        self.right_pump_assembly = right_pump_assemply
        self.left_pump_assembly = left_pump_assembly
        self.offset = offset
        self.right_suction_type = right_suction_type
        self.left_suction_type = left_suction_type
        self.current_suckable = None
        self.maxium_height = max_height
        
    def return_to_even(self):
        return_value = 0.0
        if isinstance(self.current_suckable, Robber):
            return_value += self.maxium_height + 10.
        elif isinstance(self.current_suckable, Tile):
            return_value += self.maxium_height + 3.
        elif isinstance(self.current_suckable, Piece):
            return_value += self.maxium_height + 5.
        
        if self.current_suckable != None:    
            return_value = -1 * self.convert_z(self.current_suckable, return_value)
        
        self.z_motor.move_to(return_value)
    
    def convert_z(self, suckable, z):
        if suckable.suction_type == self.right_suction_type:
            return self.maxium_height - z
        elif suckable.suction_type == self.left_suction_type:
            return -self.maxium_height + z
        
    def add_offset(self, suckable):
        if suckable.suction_type == self.right_suction_type:
            return [suckable.position[0], suckable.position[1] + self.offset]
        elif suckable.suction_type == self.left_suction_type:
            return [suckable.position[0], suckable.position[1] - self.offset]
        
    def pick_up(self, suckable, z):
        self.current_suckable = suckable
        
        z = self.convert_z(suckable, z)
        # This will have to change if we change what side it is on
        if suckable.suction_type == self.right_suction_type:
            self.right_pump_assembly.suction()
            self.z_motor.move_to(z)
            time.sleep(0.1)
            self.return_to_even()
        elif suckable.suction_type == self.left_suction_type:
            self.left_pump_assembly.blow(0.75, 1.5)
            self.z_motor.move_to(z)
            self.left_pump_assembly.release()
            self.left_pump_assembly.suction(1.0, 3)
            self.return_to_even()
            
            
    def place(self, suckable, z):
        self.current_suckable = None
        
        z = self.convert_z(suckable, z)
        if suckable.suction_type == self.right_suction_type:
            self.z_motor.move_to(z)
            self.right_pump_assembly.release()
            self.right_pump_assembly.blow(1.0, 0.4)
            self.right_pump_assembly.release()
            self.return_to_even()
        elif suckable.suction_type == self.left_suction_type:
            self.z_motor.move_to(z)
            self.left_pump_assembly.release()
            self.left_pump_assembly.blow(1.0, 2)
            self.left_pump_assembly.release()
            self.return_to_even()
            
    
class Gantry():
    def __init__(self, linked_motor: LinkedMotor, mount: Mount, catan_board: Board, 
                 tile_stack_positions, number_stack_positions, robber_position,
                 red_position, blue_position, orange_position, white_position):
        
        self.x_and_y_motor = linked_motor
        self.mount = mount
        self.catan_board = catan_board
        self.tile_stacks = [TileStack(xy) for xy in tile_stack_positions]
        self.number_stacks = [TileStack(xy) for xy in number_stack_positions]
        self.robber = [TileStack(robber_position, 33)] # When we place the robber we put it here
        
        self.red_bin = Bin(red_position)
        self.blue_bin = Bin(blue_position)
        self.orange_bin = Bin(orange_position)
        self.white_bin = Bin(white_position)
        
    def move_to(self, object):
        # we will always move to an object in space, i think?
        xy = self.mount.add_offset(object)
        self.x_and_y_motor.move_to(xy)
        
    def move_to_xy(self, xy):
        self.x_and_y_motor.move_to(xy)
        
    def move_to_home(self):
        self.move_to_xy([0.,0.])
    
    def pick_up(self, object_to_pick):
        if isinstance(object_to_pick, list) and isinstance(object_to_pick[0], Container): # Lazy eval
            valid_container = self.valid_remove_container(object_to_pick)
            height = valid_container.stack_height # Tested it, it does a copy.
            item = valid_container.pop()
            
            self.move_to(item)
            self.mount.pick_up(item, height)
        elif isinstance(object_to_pick, Container):
            height = object_to_pick.stack_height
            item = object_to_pick.pop()
            
            self.move_to(item)
            self.mount.pick_up(item, height)
        else:
            self.move_to(object_to_pick)
            self.mount.pick_up(object_to_pick, object_to_pick.height)
    
    def place(self, where_to_place):
        if isinstance(where_to_place, list) and isinstance(where_to_place[0], Container): # Lazy eval
            valid_container = self.valid_place_container(self.mount.current_suckable, where_to_place)
            # Can check if there is no valid containers, but I want to error out anyway    
            valid_container.push(self.mount.current_suckable)
            self.move_to(self.mount.current_suckable)
            self.mount.place(self.mount.current_suckable, valid_container.stack_height) # + object.height) we want to place right above the stack so adding it first should be ideal
        elif isinstance(where_to_place, Container):
            where_to_place.push(self.mount.current_suckable)
            self.move_to(self.mount.current_suckable)
            self.mount.place(self.mount.current_suckable, where_to_place.stack_height)
        else:
            self.move_to(where_to_place)
            self.mount.place(self.mount.current_suckable, where_to_place.height) # man this is definity cheating and will lead to so many bugs but I love it, its hard to do things in python without the languge being strongly typed
               
    def valid_place_container(self, object, containers):
        for container in containers:
            if object.height + container.stack_height <= container.max_height:
                return container
           
    def valid_remove_container(self, containers):
        for container in reversed(containers):
            if len(container) != 0:
                return container
        
        raise RuntimeError("No object to remove")
        
