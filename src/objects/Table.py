from objects.TableComponents import *
from objects.Gantry import Gantry

class Table():
    def __init__(self, gantry: Gantry, camera: CameraRig, lift: Lift, cover: SingleDegreeComponent):
        self.gantry = gantry
        self.camera = camera
        self.lift = lift
        self.cover = cover
        
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
        # open cover
        # raise lift
        
        pass