from catan_objects.TableComponents import *
from catan_objects.Gantry import Gantry
#from integration_test.integration_setup import Setup
from integration_test.Expo_setup import Setup # When running Expo Code

class Table():
    def __init__(self, gantry: Gantry, camera: CameraRig, lift: Lift, cover: SingleDegreeComponent):
        self.gantry = gantry
        self.camera = camera
        self.lift = lift
        self.cover = cover
        
    def run(self):
        # drop lift
        #self.lift.set_low_position()
        # close cover
        # self.cover.set_high_position()
        
        # take picture
        # self.camera.take_picture()
        
        # Determine where Robber is
        self.find_desert()
        
        # Add numbers and robber to stack
        self.reveal(Number(10))
        self.reveal(Robber())

        # take & place robber off
        self.remove_robber()
        # take & place pieces off
        self.remove_pieces()
        # take & place numbers off
        self.remove_numbers()
        # take & place hexes off
        self.remove_hexes()
        # take & place hexes on
        self.place_hexes()
        # take & place numbers on
        self.place_numbers()
        # take & place robber on
        self.place_robber()
        # open cover
        # raise lift
    
    def find_desert(self):
        A_pos = [345,105]
        catan_board_camera = Setup(A_pos)

        self.camera.find_desert(catan_board_camera, self.gantry.catan_board, (40,50))
    
    def reveal(self, to_reveal):
        objs = self.camera.analyze_board(to_reveal)
        self.gantry.catan_board.add_to_board_lazy(objs)
    
    def remove_robber(self):
        robber_hexes = self.camera.analyze_board([Robber()])
        self.gantry.mount.z_motor.move_to(5)
        
        for hexagon in robber_hexes:
            self.gantry.pick_up(hexagon)
            self.gantry.place(self.gantry.robber)
            self.gantry.mount.z_motor.move_to(10)
            
    def remove_pieces_by_color(self, color):
        pieces = self.camera.analyze_board([Road(color), Settlement(color), City(color)])
        for piece in pieces:
            self.gantry.pick_up(piece)
            if color == 'red':
                self.gantry.place(self.gantry.red_bin)
            elif color == 'blue':
                self.gantry.place(self.gantry.blue_bin)
            elif color == 'white':
                self.gantry.place(self.gantry.white_bin)
            elif color == 'orange':
                self.gantry.place(self.gantry.orange_bin)
            
    def remove_pieces(self):
        colors = ['red']
        for color in colors:
            self.remove_pieces_by_color(color)
            # Can check image and update
            
    def remove_numbers(self):
        hexes = self.gantry.catan_board.remove_tiles()
        for hexagon in hexes:
            self.gantry.pick_up(hexagon)
            self.gantry.place(self.gantry.number_stacks)
            
    def remove_hexes(self):
        hexes = self.gantry.catan_board.remove_tiles()
        for hexagon in hexes:
            self.gantry.pick_up(hexagon)
            self.gantry.place(self.gantry.tile_stacks)
            
    def place_hexes(self):
        hexes = self.gantry.catan_board.place_resources()
        for hexagon in hexes:
            self.gantry.pick_up(self.gantry.tile_stacks)
            self.gantry.place(hexagon)
            
    def place_numbers(self):
        numbers = self.gantry.catan_board.place_numbers()
        for number in numbers:
            self.gantry.pick_up(self.gantry.number_stacks)
            self.gantry.place(number)
            
    def place_robber(self):
        self.gantry.mount.z_motor.move_to(-5)
        
        self.gantry.pick_up(self.gantry.robber)
        self.gantry.place(self.gantry.catan_board.get_desert_hex())