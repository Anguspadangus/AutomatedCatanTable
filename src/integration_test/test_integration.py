from integration_test.integration_setup import Setup
from catan_objects.BoardComponents import *
from catan_objects.Gantry import *

pump_1 = PumpAssembly(Gate_Valve(GPIO_SETUP(6), GPIO_CONTROL_GATE, 6), DCMotor(HAT_SETUP("motor2", 0x62)), DCMotor(HAT_SETUP("motor1", 0x62)))
pump_2 = PumpAssembly(Gate_Valve(GPIO_SETUP(19), GPIO_CONTROL_GATE, 19), DCMotor(HAT_SETUP("motor4", 0x62)), DCMotor(HAT_SETUP("motor3", 0x62)))
# Since you only have one pump, need to switch
mount = Mount(Stepper(200, 40, HAT_SETUP('stepper1', 0x61), HAT_CONTROL), pump_2, pump_1)
catan_board = Setup((350,50))
gantry = Gantry(LinkedMotor(Stepper(200, 40, HAT_SETUP('stepper1')),
                Stepper(200, 40, HAT_SETUP('stepper2')), LINKED_HAT_CONTROL),
                mount, catan_board, [[0,100], [0,200], [0,300]], [[10,10], [20,10], [30,10]], [10,20],
                [10, 30], [10, 40], [10, 50], [10,60])

#gantry.move_to_xy([-350, -50])
#gantry.move_to_xy([0,-gantry.mount.offset])
#gantry.mount.right_pump_assembly.suck_motor.throttle = 0

"""
hexagon = Hex('s',1)
tile_stack = TileStack([0,0])
gantry.pick_up(hexagon)
gantry.place(tile_stack)
gantry.move_to_home()
"""

for hexagon in gantry.catan_board.empty_spaces:
    gantry.pick_up(hexagon)
    gantry.place(gantry.tile_stacks)
    
for hexagon in reversed(gantry.catan_board.empty_spaces):
    gantry.pick_up(gantry.tile_stacks)
    gantry.place(hexagon)

gantry.move_to_home()