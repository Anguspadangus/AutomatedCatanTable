from objects.TableComponents import SingleDegreeComponent, CameraRig
from objects.Gantry import Gantry
from objects.Board import Board

class Table():
    def __init__(self, gantry: Gantry, camera: CameraRig, lift: SingleDegreeComponent, cover: SingleDegreeComponent, catan_board: Board):
        self.gantry = gantry
        self.camera = camera
        self.lift = lift
        self.cover = cover
        self.catan_board = catan_board
        
    def run(self):
        # drop lift
        # close cover
        # take picture
        # take & place robber off
        # take & place pieces off
        # take & place numbers off
        # take & place hexes off
        # take & place hexes on
        # take & place numbers on
        # take & place robber on
        
        pass