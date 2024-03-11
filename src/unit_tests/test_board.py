from unit_tests.StandardBoard import StandardSetup
from catan_objects.BoardComponents import *
from unit_tests.motor_test_methods import *

import unittest
import os
import copy
import numpy as np
import random

class CVTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        catan_board = StandardSetup()
        hex_radius  = 3.5 / 2 * 25.4 #mm
        number_positions = [[random.uniform(space.position[0]-hex_radius, space.position[0]+hex_radius), random.uniform(space.position[1]-hex_radius, space.position[1]+hex_radius)]
                            for space in catan_board.empty_spaces]
        
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def tearDown(self):
        # In running python the static var is created and not destroyed between tests
        Motor.s_hats.clear()
        
    def test_init(self):
        catan_board = StandardSetup()
        self.assertTrue(all(len(space.stack) > 0 for space in catan_board.empty_spaces))
        
    def test_add_numbers(self):
        catan_board = StandardSetup()
        numbers = [Number(10, random.randint(0, 100)) for i in range(18)]
        catan_board.add_numbers(numbers)
        self.assertTrue(all((len(space.stack) > 1 or space.stack[0].isDesert) for space in catan_board.empty_spaces))
        
    def test_remove_numbers(self):
        catan_board = StandardSetup()
        numbers = [Number(10, random.randint(0, 100)) for i in range(18)]
        catan_board.add_numbers(numbers)
        removal_order = catan_board.remove_tiles()
        
        self.assertTrue(len(removal_order), 18)
        
        for empty_hex in removal_order:
            empty_hex.pop()
            
        self.assertTrue(all((len(space.stack) == 1) for space in removal_order))
        self.assertTrue(all((len(space.stack) == 1) for space in catan_board.empty_spaces))
        
    def test_remove_hexes(self):
        catan_board = StandardSetup()
        numbers = [Number(10, random.randint(0, 100)) for i in range(18)]
        catan_board.add_numbers(numbers)
        for i in range(2):
            removal_order = catan_board.remove_tiles()
            for empty_hex in removal_order:
                empty_hex.pop()
                
        self.assertTrue(len(removal_order), 19)
            
        self.assertTrue(all((len(space.stack) == 0) for space in removal_order))
        self.assertTrue(all((len(space.stack) == 0) for space in catan_board.empty_spaces))
        
if __name__ == '__main__':
    unittest.main()