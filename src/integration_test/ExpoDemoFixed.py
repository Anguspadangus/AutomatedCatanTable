from catan_objects.TableComponents import *
from catan_objects.BoardComponents import *
from integration_test.Expo_setup import Setup
from catan_objects.Motor import *
from catan_objects.Gantry import *
from catan_objects.Table import *

import time

# UPDATE THESE
pump_1 = PumpAssembly(Gate_Valve(GPIO_SETUP(6), GPIO_CONTROL_GATE, 6), DCMotor(HAT_SETUP("motor1", 0x62)), DCMotor(HAT_SETUP("motor2", 0x62)))
pump_2 = PumpAssembly(Gate_Valve(GPIO_SETUP(19), GPIO_CONTROL_GATE, 19), DCMotor(HAT_SETUP("motor3", 0x62)), DCMotor(HAT_SETUP("motor4", 0x62)))
mount = Mount(Stepper(200, 40, HAT_SETUP('stepper1', 0x61), HAT_CONTROL, 0.01), pump_2, pump_1)
catan_board = Setup((395,39))
gantry = Gantry(LinkedMotor(Stepper(200, 40, HAT_SETUP('stepper1')),
                Stepper(200, 40, HAT_SETUP('stepper2')), LINKED_HAT_CONTROL),
                mount, catan_board, [[0,0], [2,113]], [[30,195]], [395,115],
                [250,-52], [-150,-75], [-150,-75], [-150,-75])

cover = SingleDegreeComponent(Stepper(200, 8, HAT_SETUP('stepper1', 0x63), 0.002, HAT_CONTROL), -769, 0,)

cam = CameraRig(CameraModuleCatan(), Lights(), [0,0])
table = Table(gantry, cam, None, cover)

table.cover.set_high_position()
cam.take_picture()
table.find_desert()

for hexagon in table.gantry.catan_board.empty_spaces:
    if not hexagon.stack[0].is_desert:
        hexagon.push(Number(10, hexagon.position))

long_hex_Radius = 45.5 # mm
short_hex_radius = long_hex_Radius / 2 * math.sqrt(3) * 1.01 # mm
A_pos = (395,39)
B_pos = (A_pos[0] + 1.5 * long_hex_Radius, A_pos[1] + short_hex_radius)
C_pos = (A_pos[0] - (1.5 * long_hex_Radius), A_pos[1] + short_hex_radius)
D_pos = (B_pos[0] + 1.5 * long_hex_Radius, B_pos[1] + short_hex_radius)
E_pos = (A_pos[0], 2 * short_hex_radius + A_pos[1])
F_pos = (C_pos[0] - (1.5 * long_hex_Radius), C_pos[1] + short_hex_radius)
G_pos = (B_pos[0], 2 * short_hex_radius + B_pos[1])
H_pos = (C_pos[0], 2 * short_hex_radius + C_pos[1])
I_pos = (D_pos[0], 2 * short_hex_radius + D_pos[1])
J_pos = (E_pos[0], 2 * short_hex_radius + E_pos[1])
K_pos = (F_pos[0], 2 * short_hex_radius + F_pos[1])
L_pos = (G_pos[0], 2 * short_hex_radius + G_pos[1])
M_pos = (H_pos[0], 2 * short_hex_radius + H_pos[1])
N_pos = (I_pos[0], 2 * short_hex_radius + I_pos[1])
O_pos = (J_pos[0], 2 * short_hex_radius + J_pos[1])

pieces = [Road('white', [M_pos[0] - long_hex_Radius, M_pos[1]]),
            Settlement('blue', [H_pos[0] - 0.5 * long_hex_Radius, H_pos[1] - short_hex_radius]),
            City('red', [A_pos[0] + long_hex_Radius, J_pos[1]])]

robber = Robber(table.gantry.catan_board.empty_spaces[1].position)

# Pick up Robber
table.remove_robber()

# Pick up city, settlement, Road
for p in pieces:
    table.gantry.pick_up(p)
    if p.color == Piece.__color_dictionary['red']:
        table.gantry.place(table.gantry.red_bin)
    if p.color == Piece.__color_dictionary['white']:
        table.gantry.place(table.gantry.white_bin)
    if p.color == Piece.__color_dictionary['blue']:
        table.gantry.place(table.gantry.blue_bin)

# Pick up Numbers
table.remove_numbers()

# Pick up Hexes
table.remove_hexes()

# Place Hexes
table.place_hexes()

# Place Numbers
table.place_hexes()

table.gantry.move_to_home()