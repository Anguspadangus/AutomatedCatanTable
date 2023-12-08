from objects.tile import *
from objects.Board import Board
import math

"""
Defines the standard setup of a catan game, useful for tests and the final product.    
"""

def StandardSetup():
    # The size of each resource hex and number tile
    hexRadius = 3.5 / 2 # inches
    circleRadius = 0.492126 # inches

    # The neighbors of each empty hex
    A_neighbors = ['E', 'B', '0','0', '0', 'D']
    B_neighbors = ['F', 'C', '0','0', 'A', 'E']
    C_neighbors = ['G', '0', '0','0', 'B', 'G']
    D_neighbors = ['I', 'E', 'A','0', '0', 'H']
    E_neighbors = ['J', 'F', 'B','A', 'D', 'I']
    F_neighbors = ['K', 'G', 'C','B', 'E', 'J']
    G_neighbors = ['L', '0', '0','C', 'F', 'K']
    H_neighbors = ['M', 'I', 'D','0', '0', '0']
    I_neighbors = ['N', 'J', 'E','D', 'H', 'M']
    J_neighbors = ['O', 'K', 'F','E', 'I', 'N']
    K_neighbors = ['P', 'L', 'G','F', 'J', 'O']
    L_neighbors = ['0', '0', '0','G', 'K', 'P']
    M_neighbors = ['Q', 'N', 'I','H', '0', '0']
    N_neighbors = ['R', 'O', 'J','I', 'M', 'Q']
    O_neighbors = ['S', 'P', 'K','J', 'N', 'R']
    P_neighbors = ['0', '0', 'L','K', 'O', 'S']
    Q_neighbors = ['0', 'R', 'N','M', '0', '0']
    R_neighbors = ['0', 'S', 'O','N', 'Q', '0']
    S_neighbors = ['0', '0', 'P','O', 'R', '0']

    # The position of each possible catan board, determined by the hexes radius
    A_pos = (0,0)
    B_pos = (math.sqrt(3) * hexRadius + A_pos[0], A_pos[1])
    C_pos = (math.sqrt(3) * hexRadius + B_pos[0], B_pos[1])
    D_pos = (-math.sqrt(3)/2 * hexRadius + A_pos[0], 3/2 * hexRadius + A_pos[1])
    E_pos = (math.sqrt(3) * hexRadius + D_pos[0], D_pos[1])
    F_pos = (math.sqrt(3) * hexRadius + E_pos[0], E_pos[1])
    G_pos = (math.sqrt(3) * hexRadius + F_pos[0], F_pos[1])
    H_pos = (-math.sqrt(3)/2 * hexRadius + D_pos[0], 3/2 * hexRadius + D_pos[1])
    I_pos = (math.sqrt(3) * hexRadius + H_pos[0], H_pos[1])
    J_pos = (math.sqrt(3) * hexRadius + I_pos[0], I_pos[1])
    K_pos = (math.sqrt(3) * hexRadius + J_pos[0], J_pos[1])
    L_pos = (math.sqrt(3) * hexRadius + K_pos[0], K_pos[1])
    M_pos = (math.sqrt(3)/2 * hexRadius + H_pos[0], 3/2 * hexRadius + H_pos[1])
    N_pos = (math.sqrt(3) * hexRadius + M_pos[0], M_pos[1])
    O_pos = (math.sqrt(3) * hexRadius + N_pos[0], N_pos[1])
    P_pos = (math.sqrt(3) * hexRadius + O_pos[0], O_pos[1])
    Q_pos = (math.sqrt(3)/2 * hexRadius + M_pos[0], 3/2 * hexRadius + M_pos[1])
    R_pos = (math.sqrt(3) * hexRadius + Q_pos[0], Q_pos[1])
    S_pos = (math.sqrt(3) * hexRadius + R_pos[0], R_pos[1])

    # Configuration of the board
    # [[name, position, neighbors], Hex(radius, resource), Number(value, radius)]
    # The position of each Hex gets updated by the empty hex it is in the same row as
    configuration = [
        [['A', A_pos, A_neighbors], Hex('A', hexRadius), Number(circleRadius)],
        [['B', B_pos, B_neighbors], Hex('B',hexRadius), Number(circleRadius)],
        [['C', C_pos, C_neighbors], Hex('C', hexRadius), Number(circleRadius)],
        [['D', D_pos, D_neighbors], Hex('D', hexRadius), Number(circleRadius)],
        [['E', E_pos, E_neighbors], Hex('E', hexRadius), Number(circleRadius)],
        [['F', F_pos, F_neighbors], Hex('F', hexRadius), Number(circleRadius)],
        [['G', G_pos, G_neighbors], Hex('G', hexRadius), Number(circleRadius)],
        [['H', H_pos, H_neighbors], Hex('H', hexRadius), Number(circleRadius)],
        [['I', I_pos, I_neighbors], Hex('I', hexRadius), Number(circleRadius)],
        [['J', J_pos, J_neighbors], Hex('J', hexRadius), Number(circleRadius)],
        [['K', K_pos, K_neighbors], Hex('K', hexRadius), Number(circleRadius)],
        [['L', L_pos, L_neighbors], Hex('L', hexRadius), Number(circleRadius)],
        [['M', M_pos, M_neighbors], Hex('M', hexRadius), Number(circleRadius)],
        [['N', N_pos, N_neighbors], Hex('N', hexRadius), Number(circleRadius)],
        [['O', O_pos, O_neighbors], Hex('O', hexRadius), Number(circleRadius)],
        [['P', P_pos, P_neighbors], Hex('P', hexRadius), Number(circleRadius)],
        [['Q', Q_pos, Q_neighbors], Hex('Q', hexRadius), Number(circleRadius)],
        [['R', R_pos, R_neighbors], Hex('R', hexRadius), Number(circleRadius)],
        [['S', S_pos, S_neighbors], Hex('S', hexRadius), Number(circleRadius)]
    ]

    return Board(configuration, hexRadius)