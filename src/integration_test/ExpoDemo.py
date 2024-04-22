from catan_objects.TableComponents import *
from catan_objects.BoardComponents import *
from integration_test.Expo_setup import Setup
from catan_objects.Motor import *
from catan_objects.Gantry import *
from catan_objects.Table import *

import time

pump_1 = PumpAssembly(DCMotor(HAT_SETUP("motor1", 0x68)), DCMotor(HAT_SETUP("motor1", 0x62)), DCMotor(HAT_SETUP("motor2", 0x62)))
pump_2 = PumpAssembly(DCMotor(HAT_SETUP("motor2", 0x68)), DCMotor(HAT_SETUP("motor3", 0x62)), DCMotor(HAT_SETUP("motor4", 0x62)))
mount = Mount(Stepper(200, 40, HAT_SETUP('stepper1', 0x61), HAT_CONTROL, 0.01), pump_2, pump_1)
catan_board = Setup((389,37))
gantry = Gantry(LinkedMotor(Stepper(200, 40, HAT_SETUP('stepper1')),
                Stepper(200, 40, HAT_SETUP('stepper2')), LINKED_HAT_CONTROL),
                mount, catan_board, [[0,0], [2,113]], [[30,195], [24,247]], [395,115],
                [250,-52], [550,-52], [250,448], [550,448])

cover = SingleDegreeComponent(Stepper(200, 8, HAT_SETUP('stepper2', 0x61), HAT_CONTROL, 0.002), -670, -670)
cam = CameraRig(CameraModuleCatan(), Lights(), [395,39])
table = Table(gantry, cam, None, cover)
table.cover.set_low_position()
"""
#table.cover.set_high_position()
cam.take_picture()

# Pick up Robber
table.find_desert()

#table.remove_robber()

# Pick up White, city, settlement, Road
table.remove_pieces()

# Pick up Numbers
#table.reveal([Number(10)])
#table.remove_numbers()

# Pick up Hexes
table.remove_hexes()

# Place Hexes
table.place_hexes()

# Place Numbers
#table.place_numbers()

# Place Robber
#table.place_robber()

table.gantry.move_to_home()
"""