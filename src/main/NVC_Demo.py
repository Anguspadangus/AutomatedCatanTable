from main.NVC_setup import Setup
from catan_objects.BoardComponents import *
from catan_objects.Gantry import *

pump_1 = PumpAssembly(Gate_Valve(GPIO_SETUP(6), GPIO_CONTROL_GATE, 6), DCMotor(HAT_SETUP("motor2", 0x62)), DCMotor(HAT_SETUP("motor1", 0x62)))
pump_2 = PumpAssembly(Gate_Valve(GPIO_SETUP(19), GPIO_CONTROL_GATE, 19), DCMotor(HAT_SETUP("motor4", 0x62)), DCMotor(HAT_SETUP("motor3", 0x62)))
# Since you only have one pump, need to switch
mount = Mount(Stepper(200, 40, HAT_SETUP('stepper1', 0x61), HAT_CONTROL), pump_2, pump_1)
catan_board = Setup((350,50))
gantry = Gantry(LinkedMotor(Stepper(200, 40, HAT_SETUP('stepper1')),
                Stepper(200, 40, HAT_SETUP('stepper2')), LINKED_HAT_CONTROL),
                mount, catan_board, [[0,100]], [[10,10]], [10,20],
                [10, 30], [10, 40], [10, 50], [10,60])

# Setup over A
#gantry.move_to_xy([-350, -50])

city = City('red', [300, 50])
number = Number(xy=[350, 50])

gantry.catan_board.empty_spaces[0].push(number)

# pick and place city
gantry.pick_up(city)
gantry.place(gantry.red_bin)

# pick and place number
gantry.pick_up(gantry.catan_board.empty_spaces[0])
gantry.place(gantry.number_stacks)

# pick and place hex
gantry.pick_up(gantry.catan_board.empty_spaces[0])
gantry.place(gantry.tile_stacks)

# return hex
gantry.pick_up(gantry.tile_stacks)
gantry.place(gantry.catan_board.empty_spaces[0])

# return number
gantry.pick_up(gantry.number_stacks)
gantry.place(gantry.catan_board.empty_spaces[0])

gantry.move_to_home()
