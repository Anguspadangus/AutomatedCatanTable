from objects.BoardComponents import *
from objects.Board import Board
import math

"""
Defines the standard setup of a catan game, useful for tests and the final product.    
"""

def Setup(A_pos):
    # The size of each resource hex and number tile
    long_hex_Radius = 45 # mm
    short_hex_radius = long_hex_Radius / 2 * math.sqrt(3) # mm

    # The neighbors of each empty hex
    A_neighbors = ['0', 'B', 'E','C', '0', '0']
    B_neighbors = ['0', 'D', 'G','E', 'A', '0']
    C_neighbors = ['A', 'E', 'H','F', '0', '0']
    D_neighbors = ['0', '0', 'I','G', 'B', '0']
    E_neighbors = ['B', 'G', 'J','H', 'C', 'A']
    F_neighbors = ['C', 'H', 'K','0', '0', '0']
    G_neighbors = ['D', 'I', 'L','J', 'E', 'B']
    H_neighbors = ['E', 'J', 'M','K', 'F', 'C']
    I_neighbors = ['0', '0', 'N','L', 'G', 'D']
    J_neighbors = ['G', 'L', 'O','M', 'H', 'E']
    K_neighbors = ['H', 'M', 'P','0', '0', '0']
    L_neighbors = ['I', 'N', 'Q','O', 'J', 'G']
    M_neighbors = ['J', 'O', 'R','P', 'K', 'H']
    N_neighbors = ['0', '0', '0','Q', 'L', 'I']
    O_neighbors = ['L', 'Q', 'S','R', 'M', 'J']
    P_neighbors = ['M', 'R', '0','0', '0', 'K']
    Q_neighbors = ['N', '0', '0','S', 'O', 'L']
    R_neighbors = ['O', 'S', '0','0', 'P', 'M']
    S_neighbors = ['Q', '0', '0','0', 'R', 'O']

    # The position of each possible catan board, determined by the hexes radius
    B_pos = (A_pos[0] + short_hex_radius + long_hex_Radius, A_pos[0] + short_hex_radius)
    C_pos = (A_pos[0] - short_hex_radius + long_hex_Radius, A_pos[0] + short_hex_radius)
    D_pos = (B_pos[0] + short_hex_radius + long_hex_Radius, B_pos[0] + short_hex_radius)
    E_pos = (A_pos[0], 2 * short_hex_radius + A_pos[1])
    F_pos = (C_pos[0] - short_hex_radius + long_hex_Radius, C_pos[0] + short_hex_radius)
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
        [['A', A_pos, A_neighbors], Hex('A', long_hex_Radius)],
        [['B', B_pos, B_neighbors], Hex('B', long_hex_Radius)],
        [['C', C_pos, C_neighbors], Hex('C', long_hex_Radius)],
        [['D', D_pos, D_neighbors], Hex('D', long_hex_Radius)],
        [['E', E_pos, E_neighbors], Hex('E', long_hex_Radius)],
        [['F', F_pos, F_neighbors], Hex('F', long_hex_Radius)],
        [['G', G_pos, G_neighbors], Hex('G', long_hex_Radius)],
        [['H', H_pos, H_neighbors], Hex('H', long_hex_Radius)],
        [['I', I_pos, I_neighbors], Hex('I', long_hex_Radius)],
        [['J', J_pos, J_neighbors], Hex('J', long_hex_Radius)],
        [['K', K_pos, K_neighbors], Hex('K', long_hex_Radius)],
        [['L', L_pos, L_neighbors], Hex('L', long_hex_Radius)],
        [['M', M_pos, M_neighbors], Hex('M', long_hex_Radius)],
        [['N', N_pos, N_neighbors], Hex('N', long_hex_Radius)],
        [['O', O_pos, O_neighbors], Hex('O', long_hex_Radius)],
        [['P', P_pos, P_neighbors], Hex('P', long_hex_Radius)],
        [['Q', Q_pos, Q_neighbors], Hex('Q', long_hex_Radius)],
        [['R', R_pos, R_neighbors], Hex('R', long_hex_Radius)],
        [['S', S_pos, S_neighbors], Hex('S', long_hex_Radius)]
    ]

    return Board(configuration)

if __name__ == '__main__':
    Setup()