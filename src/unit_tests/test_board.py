from unit_tests.StandardBoard import StandardSetup
from catan_objects.CatanBoard import CatanBoard
from catan_objects.BoardComponents import *
from unit_tests.motor_test_methods import *
import unittest

import os
import copy
import numpy as np
import random
import json

class CVTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        catan_board = StandardSetup()
        hex_radius  = 45 - 35 #mm
        cls.number_positions = [Number(1,[random.uniform(space.position[0]-hex_radius, space.position[0]+hex_radius), random.uniform(space.position[1]-hex_radius, space.position[1]+hex_radius)])
                            for space in catan_board.empty_spaces]
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def tearDown(self):
        # In running python the static var is created and not destroyed between tests
        Motor.s_hats.clear()
    
    def set_desert_position(self, tile_name):
        fake_board = StandardSetup()
        for tile in fake_board.empty_spaces:
            if tile.name == tile_name:
                desert_position = tile.position
        
        with open('src\Algorithms\desertPosition.json', 'w') as f:
            json.dump({"pos" : desert_position}, f)   
    
    def test_init(self):
        catan_board = StandardSetup()
        self.assertTrue(all(len(space.stack) > 0 for space in catan_board.empty_spaces))
        
    def test_add_numbers(self):
        catan_board = StandardSetup()
        numbers = [Number(10, random.randint(0, 100)) for i in range(18)]
        catan_board.add_numbers(numbers)
        self.assertTrue(all((len(space.stack) > 1 or space.stack[0].is_desert) for space in catan_board.empty_spaces))
        
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
        
    def test_add_to_board_numbers(self):
        self.set_desert_position("F")
        catan_board = StandardSetup()
        catan_board.add_to_board(self.number_positions)
        self.assertTrue(all((len(space.stack) == 2 or space.stack[0].is_desert) for space in catan_board.empty_spaces))
        
    def test_add_to_board_robber(self):
        self.set_desert_position("F")
        catan_board = StandardSetup()
        catan_board.add_to_board(self.number_positions)
        
        robber_hex = random.randint(0,4)
        random_y = random.uniform(-10, 10)
        random_x = random.uniform(-10, 10)
        robber = Robber([catan_board.empty_spaces[robber_hex].position[0] + random_x,
                         catan_board.empty_spaces[robber_hex].position[1] + random_y])
        catan_board.add_to_board([robber])
        self.assertEqual(len(catan_board.empty_spaces[robber_hex].stack), 3)
        
    def test_place_resources(self):
        self.set_desert_position("F")
        catan_board = StandardSetup()
        place_order = catan_board.place_resources()
        
        self.assertEqual(len(place_order), len(catan_board.empty_spaces))
        self.assertEqual(len(place_order), 19)
        self.assertNotEqual(place_order, catan_board.empty_spaces)
        self.assertEqual(sorted(place_order, key=lambda tile: tile.name), sorted(catan_board.empty_spaces, key=lambda tile: tile.name))
        
    def test_place_numbers(self):
        self.set_desert_position("F")
        catan_board = StandardSetup()
        place_order = catan_board.place_numbers()
        board_empty_spaces = [space for space in catan_board.empty_spaces if space.position != catan_board.desert_position]
        
        self.assertEqual(len(place_order), len(board_empty_spaces))
        self.assertEqual(len(place_order), 18)
        self.assertNotEqual(place_order, board_empty_spaces)
        self.assertEqual(sorted(place_order, key=lambda tile: tile.name), sorted(board_empty_spaces, key=lambda tile: tile.name))
        
if __name__ == '__main__':
    unittest.main()