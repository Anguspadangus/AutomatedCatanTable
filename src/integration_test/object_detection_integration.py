from catan_objects.TableComponents import *
from catan_objects.BoardComponents import *
from integration_test.integration_setup import Setup
from catan_objects.Motor import *
from catan_objects.Gantry import *
from catan_objects.Table import *

import cv2
import copy
import time

pump_1 = PumpAssembly(Gate_Valve(GPIO_SETUP(6), GPIO_CONTROL_GATE, 6), DCMotor(HAT_SETUP("motor1", 0x62)), DCMotor(HAT_SETUP("motor2", 0x62)))
pump_2 = PumpAssembly(Gate_Valve(GPIO_SETUP(19), GPIO_CONTROL_GATE, 19), DCMotor(HAT_SETUP("motor3", 0x62)), DCMotor(HAT_SETUP("motor4", 0x62)))
mount = Mount(Stepper(200, 40, HAT_SETUP('stepper1', 0x61), HAT_CONTROL, 0.01), pump_2, pump_1)
catan_board = Setup((395,39))
gantry = Gantry(LinkedMotor(Stepper(200, 40, HAT_SETUP('stepper1')),
                Stepper(200, 40, HAT_SETUP('stepper2')), LINKED_HAT_CONTROL),
                mount, catan_board, [[0,0], [2,113]], [[30,195], [24,247]], [395,115],
                [250,-52], [-150,-75], [-150,-75], [-150,-75])
cover = SingleDegreeComponent(Stepper(200, 8, HAT_SETUP('stepper2', 0x61), HAT_CONTROL, 0.002), -670, 0)
cam = CameraRig(CameraModuleCatan(), Lights(), [395,39])
table = Table(gantry, cam, None, cover)


table.cover.set_high_position()
table.camera.take_picture()

table.cover.set_low_position()

table.find_desert()
table.reveal([Number(10)])
table.remove_numbers()
table.remove_hexes()

table.place_hexes()
table.place_numbers()



#numbers = cam.find_numbers(cam.image, (40, 45))
#cam.analyze_board([Road('blue')])