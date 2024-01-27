from objects.TableComponents import SingleDegreeComponent, CameraRig
from objects.Gantry import Gantry
from objects.BoardComponents import *

class Table():
    def __init__(self, gantry: Gantry, camera: CameraRig, lift: SingleDegreeComponent, cover: SingleDegreeComponent):
        self.gantry = gantry
        self.camera = camera
        self.lift = lift
        self.cover = cover
        self.hex_stack = []
        self.number_stack = []
        
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