from objects.Motor import *
from objects.BoardComponents import *
from objects.Board import Board

import abc

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
    def __init__(self, z_motor: Stepper, right_pump_assemply: PumpAssembly, left_pump_assembly: PumpAssembly,
                 right_gribber_type = 'cup', left_gripper_type = 'universal'):
        self.z_motor = z_motor
        self.right_pump_assembly = right_pump_assemply
        self.left_pump_assembly = left_pump_assembly
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
        
    def move_to(self, location):
        pass
    
    def pick_up(self, object_to_pick):
        self.move_to(object_to_pick)
        
        if isinstance(object_to_pick, list) and isinstance(object_to_pick[0], Container): # Lazy eval
            valid_container = self.valid_remove_container(object_to_pick)
            height = valid_container.stack_height # Tested it, it does a copy.
            item = valid_container.pop()
            self.mount.pick_up(item, height)
        elif isinstance(object_to_pick, list) and not isinstance(object_to_pick[0], Container):
            raise RuntimeError("Must be a list of containers")
        else:
            self.mount.pick_up(object, object.height)
    
    def place(self, xy, object_to_place, where_to_place):
        self.move_to(xy)
        if isinstance(where_to_place, list) and isinstance(where_to_place[0], Container): # Lazy eval
            valid_container = self.valid_place_container(object_to_place, where_to_place)
            valid_container.push(object_to_place)
            self.mount.place(object_to_place, valid_container.height) # + object.height) we want to place right above the stack so adding it first should be ideal
        elif isinstance(object_to_place, list) and not isinstance(object_to_place[0], Container):
            raise RuntimeError("Must be a list of containers")
        else:
            self.mount.place(object_to_place, where_to_place) # man this is definity cheating and will lead to so many bugs but I love it, its hard to do things in python without the languge being strongly typed
               
    def valid_place_container(self, object, containers):
        for container in containers:
            if object.height + container.height <= container.max_height:
                return container
           
    def valid_remove_container(self, containers):
        for container in reversed(containers):
            if len(container) != 0:
                return container
        
        raise RuntimeError("No object to remove")
        
