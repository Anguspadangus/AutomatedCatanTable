from integration_test.integration_setup import Setup
from catan_objects.BoardComponents import *
from catan_objects.Gantry import *
import time

pump_1 = PumpAssembly(DCMotor(HAT_SETUP("motor1", 0x68)), DCMotor(HAT_SETUP("motor1", 0x62)), DCMotor(HAT_SETUP("motor2", 0x62)))
pump_2 = PumpAssembly(DCMotor(HAT_SETUP("motor2", 0x68)), DCMotor(HAT_SETUP("motor3", 0x62)), DCMotor(HAT_SETUP("motor4", 0x62)))
mount = Mount(Stepper(200, 40, HAT_SETUP('stepper1', 0x61), HAT_CONTROL, 0.01), pump_2, pump_1)
catan_board = Setup((389,37))
gantry = Gantry(LinkedMotor(Stepper(200, 40, HAT_SETUP('stepper1')),
                Stepper(200, 40, HAT_SETUP('stepper2')), LINKED_HAT_CONTROL),
                mount, catan_board, [[0,0], [2,113]], [[30,195], [24,247]], [395,115],
                [250,-52], [550,-52], [250,448], [550,448])

#gantry.move_to_xy([395,40])
#gantry.move_to_xy([0,-gantry.mount.offset])
#gantry.mount.right_pump_assembly.suck_motor.throttle = 0
"""
city = Robber((395,39))
gantry.mount.z_motor.move_to(5)
gantry.pick_up(city)
gantry.place(gantry.robber)
gantry.mount.z_motor.move_to(10)
"""
"""
n1 = Number(10, gantry.catan_board.empty_spaces[0].position)

gantry.catan_board.empty_spaces[0].push(n1)
"""

for hexagon in gantry.catan_board.empty_spaces:
    gantry.pick_up(hexagon)
    gantry.place(gantry.tile_stacks)
    time.sleep(2)
    
#gantry.move_to_home()

#gantry.number_stacks[0].push(n1)
#gantry.move_to_xy([gantry.number_stacks[0].position[0], gantry.number_stacks[0].position[1]+25])
#ime.sleep(4)
#gantry.number_stacks[0].push(n2)


for hexagon in reversed(gantry.catan_board.empty_spaces):
    gantry.pick_up(gantry.tile_stacks)
    gantry.place(hexagon)

gantry.move_to_home()
#gantry.mount.z_motor.move_to(0)