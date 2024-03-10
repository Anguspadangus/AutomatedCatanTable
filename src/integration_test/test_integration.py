from integration_test.integration_setup import Setup
from objects.BoardComponents import *
from objects.Gantry import *

pump_1 = PumpAssembly(Gate_Valve(GPIO_SETUP(6), GPIO_CONTROL_GATE, 6), DCMotor(HAT_SETUP("motor_M3", "0x61")), DCMotor(HAT_SETUP("motor_M4", "0x61")))
# Since you only have one pump, need to switch
mount = Mount(Stepper(200, 8, HAT_SETUP('stepper1', "0x61"), HAT_CONTROL), pump_1, None)
board = Setup((0,0))
gantry = Gantry(LinkedMotor(Stepper(200, 8, HAT_SETUP('stepper1')),
                Stepper(200, 8, HAT_SETUP('stepper2')), LINKED_HAT_CONTROL),
                mount, board, [[10,0], [20,0], [30,0]], [[10,10], [20,10], [30,10]], [10,20],
                [10, 30], [10, 40], [10, 50], [10,60])





