from catan_objects.Motor import *
from catan_objects.BoardComponents import *
from catan_objects.CatanBoard import CatanBoard

class PumpAssembly():
    def __init__(self, valve: DCMotor, suck_motor: DCMotor, blow_motor: DCMotor = None):
        self.valve = valve
        self.suck_motor = suck_motor
        self.blow_motor = blow_motor
        
    def suction(self, throttle = 1.0, sleep = 0.0):
        self.valve.start(1)
        self.suck_motor.start(throttle)
        time.sleep(sleep)
    
    def release(self):
        if self.suck_motor.motor.throttle != 0:
            self.suck_motor.stop()
        elif self.blow_motor.motor.throttle != 0:
            self.blow_motor.stop()
    
    def blow(self, throttle = 1.0, sleep = 0.0):
        self.valve.stop()
        self.blow_motor.start(throttle)   
        time.sleep(sleep)
        
class Mount():
    def __init__(self, z_motor: Stepper, right_pump_assemply: PumpAssembly, left_pump_assembly: PumpAssembly, max_height = 47, offset = 28,
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
            return_value += 35.
        elif isinstance(self.current_suckable, Tile):
            return_value += 35.
        elif isinstance(self.current_suckable, Piece):
            return_value += 30.
        
        if self.current_suckable != None:    
            return_value = self.convert_z(self.current_suckable, return_value)
        print(f"return value {return_value}")
        self.z_motor.move_to(return_value)
    
    def convert_z(self, suckable, z):
        if suckable.suction_type == self.right_suction_type:
            new_z = self.maxium_height - z
        elif suckable.suction_type == self.left_suction_type:
            new_z = -self.maxium_height + z
            
        if new_z > 45.5 or new_z < -45.5:
            raise Exception(f"Can't go to {new_z}")
        
        return new_z
        
    def add_offset(self, suckable):
        if suckable.suction_type == self.right_suction_type:
            return [suckable.position[0], suckable.position[1] + self.offset]
        elif suckable.suction_type == self.left_suction_type:
            return [suckable.position[0] - 5, suckable.position[1] - self.offset + 10] # THISS MUST REMAIN UG
        
    def pick_up(self, suckable, z):
        self.current_suckable = suckable
        
        z = self.convert_z(suckable, z)
        print(z)
        # This will have to change if we change what side it is on
        if suckable.suction_type == self.right_suction_type:
            self.right_pump_assembly.suction(sleep=0.5)
            self.z_motor.move_to(z)
            time.sleep(0.5)
            self.return_to_even()
        elif suckable.suction_type == self.left_suction_type:
            self.left_pump_assembly.blow(0.75)
            self.z_motor.move_to(z)
            self.left_pump_assembly.release()
            self.left_pump_assembly.suction(1.0, 3)
            self.return_to_even()
            
            
    def place(self, suckable, z):
        self.current_suckable = None
        
        z = self.convert_z(suckable, z)
        print(f"dropoff: {z}")
        if suckable.suction_type == self.right_suction_type:
            self.z_motor.move_to(z)
            self.right_pump_assembly.release()
            self.right_pump_assembly.blow(1.0, 0.4)
            self.right_pump_assembly.release()
            self.return_to_even()
        elif suckable.suction_type == self.left_suction_type:
            self.z_motor.move_to(z)
            self.left_pump_assembly.release()
            self.left_pump_assembly.blow(1.0, 1.5)
            self.left_pump_assembly.release()
            self.return_to_even()
            
    
class Gantry():
    def __init__(self, linked_motor: LinkedMotor, mount: Mount, catan_board: CatanBoard, 
                 tile_stack_positions, number_stack_positions, robber_position,
                 red_position, blue_position, orange_position, white_position):
        
        self.x_and_y_motor = linked_motor
        self.mount = mount
        self.catan_board = catan_board
        self.tile_stacks = [TileStack(xy) for xy in tile_stack_positions]
        self.number_stacks = [TileStack(xy) for xy in number_stack_positions]
        self.robber = Bin(robber_position, 25) # When we place the robber we put it here
        
        self.red_bin = Bin(red_position)
        self.blue_bin = Bin(blue_position)
        self.orange_bin = Bin(orange_position)
        self.white_bin = Bin(white_position)
        
    def move_to(self, object):
        # we will always move to an object in space, i think?
        print(f"move without offset {object.position}")
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
            self.mount.place(self.mount.current_suckable, valid_container.dropoff_height) # + object.height) we want to place right above the stack so adding it first should be ideal
        elif isinstance(where_to_place, Container):
            where_to_place.push(self.mount.current_suckable)
            self.move_to(self.mount.current_suckable)
            self.mount.place(self.mount.current_suckable, where_to_place.dropoff_height)
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
        
