from objects.Motor import *

M = Stepper(200, 8, HAT_SETUP('stepper1'), HAT_CONTROL)
M2 = Stepper(200, 8, HAT_SETUP('stepper2'), HAT_CONTROL)
LM = LinkedMotor(M, M2, LINKED_HAT_CONTROL)
LM.move_to([20, 10])
# M3 = Stepper(200, 8, HAT_SETUP('stepper1', '0x72'), HAT_CONTROL)

# DC = DCMotor(HAT_SETUP("motor_M1"))

# G1 = Stepper(200, 8, GPIO_SETUP(20, 32), GPIO_CONTROL, 20, 32)
# G1.move_to(20)