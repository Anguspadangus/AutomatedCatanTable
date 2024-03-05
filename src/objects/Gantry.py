from objects.Motor import *
from objects.BoardComponents import *
from objects.Board import Board

import abc
import time

class PumpAssembly():
    def __init__(self, valve: DCMotor, intake: DCMotor, outtake: DCMotor = None):
        self.valve = valve
        self.intake = intake
        self.outake = outtake
        
    def suction():
        pass
    
    def release():
        pass
    
    def blow():
        pass    
        
class Mount():
    def __init__(self, z_motor: Stepper, right_pump_assemply: PumpAssembly, left_pump_assembly: PumpAssembly, offset = 30,
                 right_gribber_type = 'cup', left_gripper_type = 'universal'):
        self.z_motor = z_motor
        self.right_pump_assembly = right_pump_assemply
        self.left_pump_assembly = left_pump_assembly
        self.offset = offset
        self.right_gribber_type = right_gribber_type
        self.left_gripper_type = left_gripper_type
        self.mount_dimensions = [0]
        
    def return_to_even(self):
        pass
    
    def convert_z(self, suckable, z):
        if suckable.gripper_type == self.right_gribber_type:
            return z
        elif suckable.gripper_type == self.left_gribber_type:
            return -z
        
    def add_offset(self, suckable):
        if suckable.gripper_type == self.right_gribber_type:
            return [object.position[0], object.position[1] + self.offset]
        elif suckable.gripper_type == self.left_gribber_type:
            return [object.position[0], object.position[1] - self.offset]
        
    def pick_up(self, suckable, z):
        z = self.convert_z(suckable, z)
        if suckable.gripper_type == self.right_gribber_type:
            self.z_motor.move_to(z)
            self.right_pump_assembly.suction()
            self.return_to_even()
        if suckable.gripper_type == self.left_gribber_type:
            self.z_motor.move_to(z)
            self.right_pump_assembly.blow()
            self.right_pump_assembly.suction()
            self.return_to_even()
            
    def place(self, suckable, z):
        z = self.convert_z(suckable, z)
        if suckable.gripper_type == self.right_gribber_type:
            self.z_motor.move_to(z)
            self.right_pump_assembly.blow()
            self.right_pump_assembly.release()
            self.return_to_even()
        if suckable.gripper_type == self.left_gribber_type:
            self.z_motor.move_to(z)
            self.left_pump_assembly.blow()
            self.left_pump_assembly.release()
            self.return_to_even()
        
class Container():
    def __init__(self, position):
        self.position = position
        self.stack = []
        self.stack_height = 0
    
    def __len__(self):
        return len(self.stack)    
    
    @abc.abstractmethod
    def push(self, object):
        pass
    
    @abc.abstractmethod
    def pop(self):
        pass

 # Stack of tiles to be manipulated with 
class TileStack(Container):
    def __init__(self, position, max_height = 30):
        super().__init__(position)
        self.max_height = max_height
        
    def push(self, tile):
        if self.stack_height + tile.height <= self.max_height:
            self.stack.append(tile)
            self.stack_height += tile.height
            return True
        
        return False
    
    def pop(self):
        if self.stack:
            tile = self.stack.pop()
            self.stack_height -= tile.height
            return tile
        
        return None   

class Bin(Container):
    def __init__(self, position):
        super().__init__(position)
    
    def push(self, obj):
        return True
    
    def pop(self):
        return None
    
class Gantry():
    def __init__(self, x_motor: Motor, y_motor: Motor, mount: Mount, catan_board: Board, 
                 tile_stack_positions, number_stack_positions, robber_position,
                 red_position, blue_position, orange_position, white_position):
        
        self.x_motor = x_motor
        self.y_motor = y_motor
        self.mount = mount
        self.catan_board = catan_board
        self.tile_stacks = [TileStack(xy) for xy in tile_stack_positions]
        self.number_stacks = [TileStack(xy) for xy in number_stack_positions]
        self.robber = [TileStack(robber_position, 33)] # When we place the robber we put it here
        
        self.red_bin = [Container(red_position)]
        self.blue_bin = [Container(blue_position)]
        self.orange_bin = [Container(orange_position)]
        self.white_bin = [Container(white_position)]
        
        self.current_suckable = None
        
    def move_to(self, object):
        # we will always move to an object in space, i think?
        xy = self.mount.add_offset(object)
        self.x_motor.move_to(xy[0])
        self.y_motor.move_to(xy[1])
    
    def pick_up(self, object_to_pick):
        if isinstance(object_to_pick, list) and isinstance(object_to_pick[0], Container): # Lazy eval
            valid_container = self.valid_remove_container(object_to_pick)
            height = valid_container.stack_height # Tested it, it does a copy.
            item = valid_container.pop()
            
            self.move_to(item)
            self.mount.pick_up(item, height)
            self.current_suckable = item
        elif isinstance(object_to_pick, list) and not isinstance(object_to_pick[0], Container):
            raise RuntimeError("Must be a list of containers")
        else:
            self.move_to(item)
            self.mount.pick_up(object_to_pick, object.height)
            self.current_suckable = object_to_pick
    
    def place(self, where_to_place):
        if isinstance(where_to_place, list) and isinstance(where_to_place[0], Container): # Lazy eval
            valid_container = self.valid_place_container(self.current_suckable, where_to_place)
            valid_container.push(self.current_suckable)
            self.mount.place(self.current_suckable, valid_container.height) # + object.height) we want to place right above the stack so adding it first should be ideal
        elif isinstance(where_to_place, list) and not isinstance(where_to_place[0], Container):
            raise RuntimeError("Must be a list of containers")
        else:
            self.mount.place(self.current_suckable, where_to_place) # man this is definity cheating and will lead to so many bugs but I love it, its hard to do things in python without the languge being strongly typed
        
        self.current_suckable = None
               
    def valid_place_container(self, object, containers):
        for container in containers:
            if object.height + container.height <= container.max_height:
                return container
           
    def valid_remove_container(self, containers):
        for container in reversed(containers):
            if len(container) != 0:
                return container
        
        raise RuntimeError("No object to remove")
        
