from integration_test.integration_setup import Setup
from catan_objects.BoardComponents import *
from catan_objects.Gantry import *
import time

pump_1 = PumpAssembly(Gate_Valve(GPIO_SETUP(6), GPIO_CONTROL_GATE, 6), DCMotor(HAT_SETUP("motor1", 0x62)), DCMotor(HAT_SETUP("motor2", 0x62)))
pump_2 = PumpAssembly(Gate_Valve(GPIO_SETUP(19), GPIO_CONTROL_GATE, 19), DCMotor(HAT_SETUP("motor3", 0x62)), DCMotor(HAT_SETUP("motor4", 0x62)))
# Since you only have one pump, need to switch
mount = Mount(Stepper(200, 40, HAT_SETUP('stepper1', 0x61), HAT_CONTROL), pump_1, pump_2)
catan_board = Setup((395,38))
gantry = Gantry(LinkedMotor(Stepper(200, 40, HAT_SETUP('stepper1')),
                Stepper(200, 40, HAT_SETUP('stepper2')), LINKED_HAT_CONTROL),
                mount, catan_board, [[0,0], [2,113]], [[30,195]], [205,-52],
                [250,-52], [-150,-75], [-150,-75], [-150,-75])

#gantry.move_to_xy([395,40])
#gantry.move_to_xy([0,-gantry.mount.offset])
#gantry.mount.right_pump_assembly.suck_motor.throttle = 0
city = City('red', (345,42))
gantry.pick_up(city)
gantry.place(gantry.red_bin)
"""
n1 = Number(10, gantry.catan_board.empty_spaces[0].position)

gantry.catan_board.empty_spaces[0].push(n1)

for hexagon in gantry.catan_board.empty_spaces:
    gantry.pick_up(hexagon)
    gantry.place(gantry.number_stacks)
    time.sleep(2)
    
#gantry.move_to_home()

#gantry.number_stacks[0].push(n1)
#gantry.move_to_xy([gantry.number_stacks[0].position[0], gantry.number_stacks[0].position[1]+25])
#ime.sleep(4)
#gantry.number_stacks[0].push(n2)


for hexagon in reversed(gantry.catan_board.empty_spaces):
    gantry.pick_up(gantry.number_stacks)
    gantry.place(hexagon)

"""
gantry.move_to_home()
