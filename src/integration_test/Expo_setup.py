from catan_objects.BoardComponents import *
from catan_objects.CatanBoard import CatanBoard
import math

"""
Defines the standard setup of a catan game, useful for tests and the final product.    
"""

def Setup(A_pos):
    # The size of each resource hex and number tile
    long_hex_Radius = 45.5 # mm
    short_hex_radius = long_hex_Radius / 2 * math.sqrt(3) * 1.01 # mm

    # The neighbors of each empty hex
    E_neighbors = ['0', 'G', 'J','H', '0', '0']
    G_neighbors = ['0', '0', 'L','J', 'E', '0']
    H_neighbors = ['E', 'J', 'M','0', '0', '0']
    J_neighbors = ['G', 'L', 'O','M', 'H', 'E']
    L_neighbors = ['0', '0', '0','O', 'J', 'G']
    M_neighbors = ['J', 'O', '0','0', '0', 'H']
    O_neighbors = ['L', '0', '0','0', 'M', 'J']


    # The position of each possible catan board, determined by the hexes radius
    # The position of each possible catan board, determined by the hexes radius
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
    P_pos = (K_pos[0], 2 * short_hex_radius + K_pos[1])
    Q_pos = (L_pos[0], 2 * short_hex_radius + L_pos[1])
    R_pos = (M_pos[0], 2 * short_hex_radius + M_pos[1])
    S_pos = (O_pos[0], 2 * short_hex_radius + O_pos[1])
    
    configuration = [
        [['E', E_pos, E_neighbors, long_hex_Radius], Hex('E', long_hex_Radius)],
        [['G', G_pos, G_neighbors, long_hex_Radius], Hex('G', long_hex_Radius)],
        [['H', H_pos, H_neighbors, long_hex_Radius], Hex('H', long_hex_Radius)],
        [['J', J_pos, J_neighbors, long_hex_Radius], Hex('J', long_hex_Radius)],
        [['L', L_pos, L_neighbors, long_hex_Radius], Hex('L', long_hex_Radius)],
        [['M', M_pos, M_neighbors, long_hex_Radius], Hex('M', long_hex_Radius)],
        [['O', O_pos, O_neighbors, long_hex_Radius], Hex('O', long_hex_Radius)]
        ]
    
    return CatanBoard(configuration)

if __name__ == '__main__':
    Setup()