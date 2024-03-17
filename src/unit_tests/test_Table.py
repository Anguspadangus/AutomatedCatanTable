from catan_objects.Table import Table
from unit_tests.StandardBoard import StandardSetup
from catan_objects.BoardComponents import *
from catan_objects.Gantry import *
from catan_objects.TableComponents import *
from unit_tests.motor_test_methods import *

import unittest
import os
import copy

class CVTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    def set_desert_position(self, tile_name):
        fake_board = StandardSetup()
        for tile in fake_board.empty_spaces:
            if tile.name == tile_name:
                desert_position = tile.position
        
        with open('src\Algorithms\desertPosition.json', 'w') as f:
            json.dump({"pos" : desert_position}, f)   
    
    def setUp(self):
        camera = CameraRig(DCMotor(HAT_SETUP("motor1")), DCMotor(HAT_SETUP("motor2")))
        camera.H = np.array([[ 1.0, 0.0, 0.0], [ 0.0, 1.0, 0.0], [ 0.0, 0.0, 1.0]])
        camera.load_image("src\\unit_tests\\images\\robber1.jpeg")
        
        pump_1 = PumpAssembly(Gate_Valve(GPIO_SETUP(6), GPIO_CONTROL_GATE, 6), DCMotor(HAT_SETUP("motor4")), DCMotor(HAT_SETUP("motor1", 0x62)))
        pump_2 = PumpAssembly(Gate_Valve(GPIO_SETUP(6), GPIO_CONTROL_GATE, 6), DCMotor(HAT_SETUP("motor3", 0x62)), DCMotor(HAT_SETUP("motor4", 0x62)))
        mount = Mount(Stepper(200, 8, HAT_SETUP('stepper1', 0x64), HAT_CONTROL), pump_1, pump_2)
        
        self.set_desert_position("F")
        catan_board = StandardSetup()
        
        gantry = Gantry(LinkedMotor(Stepper(200, 8, HAT_SETUP('stepper2', 0x64), None),
                        Stepper(200, 8, HAT_SETUP('stepper1', 0x66), None), LINKED_HAT_CONTROL),
                        mount, catan_board, [[10,0], [20,0], [30,0]], [[10,10], [20,10], [30,10]], [10,20],
                        [10, 30], [10, 40], [10, 50], [10,60])
        solenoid_1 = SingleDegreeComponent(DCMotor(HAT_SETUP("motor1", 0x68)), 1, 0)
        solenoid_2 = SingleDegreeComponent(DCMotor(HAT_SETUP("motor2", 0x68)), 1, 0)
        lift = Lift(Stepper(200, 8, GPIO_SETUP(20, 32), GPIO_CONTROL, 20, 32), 100, 0, solenoid_1, solenoid_2)
        cover = SingleDegreeComponent(Stepper(200, 8, HAT_SETUP('stepper2', 0x66), HAT_CONTROL), 300, 0)
        self.table = Table(gantry, camera, lift, cover)
    
    def tearDown(self):
        # In running python the static var is created and not destroyed between tests
        Motor.s_hats.clear()
        
    def test_init(self):
        # Check to make sure setup is performed
        pass
        
    def test_remove_and_place_robber(self):
        self.table.reveal([Robber()])
        
        self.assertTrue([tile for tile in self.table.gantry.catan_board.empty_spaces if isinstance(tile.stack[-1], Robber)])
        self.assertFalse(self.table.gantry.robber.stack)
        self.table.remove_robber()
        self.assertFalse([tile for tile in self.table.gantry.catan_board.empty_spaces if isinstance(tile.stack[-1], Robber)])
        self.assertTrue(self.table.gantry.robber.stack)
        
        self.table.place_robber()
        self.assertTrue([tile for tile in self.table.gantry.catan_board.empty_spaces if isinstance(tile.stack[-1], Robber)])
        self.assertFalse(self.table.gantry.robber.stack)
        
    def test_remove_and_place_numbers(self):
        self.table.reveal([Number(10)])
        
        self.assertEqual(len([tile for tile in self.table.gantry.catan_board.empty_spaces if isinstance(tile.stack[-1], Number)]),
                         len(self.table.gantry.catan_board.empty_spaces) - 1)
        
        self.table.remove_numbers()
        self.assertEqual(len([tile for tile in self.table.gantry.catan_board.empty_spaces if isinstance(tile.stack[-1], Number)]),0)
        
        total_numbers_in_stack = 0
        for stack in self.table.gantry.number_stacks:
            total_numbers_in_stack += len(stack)
            
        self.assertTrue(total_numbers_in_stack, len(self.table.gantry.catan_board.empty_spaces) - 1)
        
        self.table.place_numbers()
        self.assertEqual(len([tile for tile in self.table.gantry.catan_board.empty_spaces if isinstance(tile.stack[-1], Number)]),
                         len(self.table.gantry.catan_board.empty_spaces) - 1)
        
    def test_remove_and_place_resources(self):
        self.table.remove_hexes()
        self.assertFalse([tile for tile in self.table.gantry.catan_board.empty_spaces if len(tile.stack) != 0])
        self.table.place_hexes()
        self.assertEqual(len([tile for tile in self.table.gantry.catan_board.empty_spaces if isinstance(tile.stack[-1], Hex)]),
                         len(self.table.gantry.catan_board.empty_spaces))
        
        
if __name__ == '__main__':
    unittest.main()