from catan_objects.BoardComponents import *
from catan_objects.CatanBoard import CatanBoard
import math

"""
Defines the standard setup of a catan game, useful for tests and the final product.    
"""

def StandardSetup():
    # The size of each resource hex and number tile
    hexRadius = 350 # mm

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

    scaler = (1, 1)
    offset = (900, 1100)
    
    # The position of each possible catan board, determined by the hexes radius
    A_pos = (0, 0)
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

    positions = [A_pos, B_pos, C_pos, D_pos, E_pos, F_pos, G_pos, H_pos, I_pos, J_pos, K_pos, L_pos, M_pos, N_pos, O_pos, P_pos, Q_pos, R_pos, S_pos]
    for i in range(len(positions)):
        positions[i] = (int(positions[i][0]*scaler[0]+offset[0]), int(positions[i][1]*scaler[1]+offset[1]))
    
    configuration = [
        [['A', positions[0], A_neighbors, hexRadius], Hex('A', hexRadius)],
        [['B', positions[1], B_neighbors, hexRadius], Hex('B', hexRadius)],
        [['C', positions[2], C_neighbors, hexRadius], Hex('C', hexRadius)],
        [['D', positions[3], D_neighbors, hexRadius], Hex('D', hexRadius)],
        [['E', positions[4], E_neighbors, hexRadius], Hex('E', hexRadius)],
        [['F', positions[5], F_neighbors, hexRadius], Hex('F', hexRadius)],
        [['G', positions[6], G_neighbors, hexRadius], Hex('G', hexRadius)],
        [['H', positions[7], H_neighbors, hexRadius], Hex('H', hexRadius)],
        [['I', positions[8], I_neighbors, hexRadius], Hex('I', hexRadius)],
        [['J', positions[9], J_neighbors, hexRadius], Hex('J', hexRadius)],
        [['K', positions[10], K_neighbors, hexRadius], Hex('K', hexRadius)],
        [['L', positions[11], L_neighbors, hexRadius], Hex('L', hexRadius)],
        [['M', positions[12], M_neighbors, hexRadius], Hex('M', hexRadius)],
        [['N', positions[13], N_neighbors, hexRadius], Hex('N', hexRadius)],
        [['O', positions[14], O_neighbors, hexRadius], Hex('O', hexRadius)],
        [['P', positions[15], P_neighbors, hexRadius], Hex('P', hexRadius)],
        [['Q', positions[16], Q_neighbors, hexRadius], Hex('Q', hexRadius)],
        [['R', positions[17], R_neighbors, hexRadius], Hex('R', hexRadius)],
        [['S', positions[18], S_neighbors, hexRadius], Hex('S', hexRadius)]
    ]

    return CatanBoard(configuration)

if __name__ == '__main__':
    StandardSetup()