from objects.TableComponents import *
from objects.Gantry import Gantry

class Table():
    def __init__(self, gantry: Gantry, camera: CameraRig, lift: SingleDegreeComponent, cover: SingleDegreeComponent):
        self.gantry = gantry
        self.camera = camera
        self.lift = lift
        self.cover = cover
        
    def run(self):
        # drop lift
        # close cover
        # take picture
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
        
        pass
    
    def remove_robber(self):
        robber = self.camera.analyze_board(self.gantry.board, [Robber()])
        for piece in robber:
            self.gantry.pick_up(piece)
            self.gantry.place(self.gantry.robber)
                
    def remove_pieces_by_color(self, color):
        pieces = self.camera.analyze_board(self.gantry.board, [Road(color), Settlememt(color), City(color)])
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
        colors = ['red', 'blue', 'white', 'orange']
        for color in colors:
            self.remove_pieces_by_color(color)
            # Can check image and update
            
    def remove_numbers(self):
        number = self.camera.analyze_board(self.gantry.board, [Number()])
        for piece in number:
            self.gantry.pick_up(piece)
            self.gantry.place(self.gantry.number_stacks)
            
    def remove_hexes(self):
        hexes = self.gantry.board.remove_resources()
        for hex in hexes:
            self.gantry.pick_up(hex)
            self.gantry.place(self.gantry.tile_stacks)
            
    def place_hexes(self):
        hexes = self.gantry.board.place_resources()
        for hex in hexes:
            self.gantry.pick_up(self.gantry.tile_stacks)
            self.gantry.place(hex)
            
    def place_numbers(self):
        numbers = self.gantry.board.place_numbers()
        for number in numbers:
            self.gantry.pick_up(self.gantry.number_stacks)
            self.gantry.place(number)
            
    def place_robber(self):
        self.gantry.pick_up(self.gantry.robber)
        self.gantry.place(self.gantry.board.desert_position)