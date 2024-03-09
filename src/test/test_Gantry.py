from objects.StandardBoard import StandardSetup
from objects.BoardComponents import *
from objects.Gantry import *
from objects.TableComponents import CameraRig
from test.motor_test_methods import *

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
    
    def setUp(self):
        pass
    
    def tearDown(self):
        # In running python the static var is created and not destroyed between tests
        Motor.s_hats.clear()
    
    def test_init(self):
        camera = CameraRig(DCMotor(HAT_SETUP("motor_M1")), DCMotor(HAT_SETUP("motor_M2")))
        pump_1 = PumpAssembly(DCMotor(HAT_SETUP("motor_M3")), DCMotor(HAT_SETUP("motor_M4")), DCMotor(HAT_SETUP("motor_M1", "0x62")))
        pump_2 = PumpAssembly(DCMotor(HAT_SETUP("motor_M2", "0x62")), DCMotor(HAT_SETUP("motor_M3", "0x62")), DCMotor(HAT_SETUP("motor_M4", "0x62")))
        mount = Mount(Stepper(200, 8, HAT_SETUP('stepper1', "0x64"), HAT_CONTROL), pump_1, pump_2)
        board = StandardSetup()
        gantry = Gantry(Stepper(200, 8, HAT_SETUP('stepper2', "0x64"), HAT_CONTROL),
                        Stepper(200, 8, HAT_SETUP('stepper1', '0x66'), HAT_CONTROL),
                        mount, board, [[10,0], [20,0], [30,0]], [[10,10], [20,10], [30,10]], [10,20],
                        [10, 30], [10, 40], [10, 50], [10,60])
    
    def test_move_to_xy(self):
        xy = [10,20]
        mount = Mount(Stepper(200, 8, HAT_SETUP('stepper1', "0x64"), HAT_CONTROL), None, None)
        gantry = Gantry(Stepper(200, 8, HAT_SETUP('stepper2', "0x64"), HAT_CONTROL),
                        Stepper(200, 8, HAT_SETUP('stepper1', '0x66'), HAT_CONTROL),
                        mount, None, [[10,0], [20,0], [30,0]], [[10,10], [20,10], [30,10]], [10,20],
                        [10, 30], [10, 40], [10, 50], [10,60])

        self.assertEqual(gantry.x_motor.current_cartisan, 0.0)
        self.assertEqual(gantry.y_motor.current_cartisan, 0.0)
        gantry.move_to_xy(xy)
        self.assertEqual(gantry.x_motor.current_cartisan, 10.)
        self.assertEqual(gantry.y_motor.current_cartisan, 20.)
        
        gantry.move_to_home()
        self.assertEqual(gantry.x_motor.current_cartisan, 0.0)
        self.assertEqual(gantry.y_motor.current_cartisan, 0.0)
        
    def test_move_to_piece(self):
        road_position = [50., 20.]
        mount = Mount(Stepper(200, 8, HAT_SETUP('stepper1', "0x64"), HAT_CONTROL), None, None)
        gantry = Gantry(Stepper(200, 8, HAT_SETUP('stepper2', "0x64"), HAT_CONTROL),
                        Stepper(200, 8, HAT_SETUP('stepper1', '0x66'), HAT_CONTROL),
                        mount, None, [[10,0], [20,0], [30,0]], [[10,10], [20,10], [30,10]], [10,20],
                        [10, 30], [10, 40], [10, 50], [10,60])
        
        road = Road('red', road_position)
        gantry.move_to(road)
        self.assertEqual(gantry.x_motor.current_cartisan, road_position[0])
        self.assertEqual(gantry.y_motor.current_cartisan, road_position[1] - mount.offset)
        
    def test_pick_up_tile(self):
        tile_position = [50., 20.]
        mount = Mount(Stepper(200, 8, HAT_SETUP('stepper1', "0x64"), HAT_CONTROL), None, None)
        gantry = Gantry(Stepper(200, 8, HAT_SETUP('stepper2', "0x64"), HAT_CONTROL),
                        Stepper(200, 8, HAT_SETUP('stepper1', '0x66'), HAT_CONTROL),
                        mount, None, [[10,0], [20,0], [30,0]], [[10,10], [20,10], [30,10]], [10,20],
                        [10, 30], [10, 40], [10, 50], [10,60])
        
        hex = Hex("empty", 1, tile_position)
        gantry.move_to(hex)
        self.assertEqual(gantry.x_motor.current_cartisan, tile_position[0])
        self.assertEqual(gantry.y_motor.current_cartisan, tile_position[1] + mount.offset)
        
    def test_piece_to_bin(self):
        road_position = [50., 20.]
        pump_1 = PumpAssembly(DCMotor(HAT_SETUP("motor_M3")), DCMotor(HAT_SETUP("motor_M4")), DCMotor(HAT_SETUP("motor_M1", "0x62")))
        pump_2 = PumpAssembly(DCMotor(HAT_SETUP("motor_M2", "0x62")), DCMotor(HAT_SETUP("motor_M3", "0x62")), DCMotor(HAT_SETUP("motor_M4", "0x62")))
        mount = Mount(Stepper(200, 8, HAT_SETUP('stepper1', "0x64"), HAT_CONTROL), pump_1, pump_2)
        gantry = Gantry(Stepper(200, 8, HAT_SETUP('stepper2', "0x64"), HAT_CONTROL),
                        Stepper(200, 8, HAT_SETUP('stepper1', '0x66'), HAT_CONTROL),
                        mount, None, [[10,0], [20,0], [30,0]], [[10,10], [20,10], [30,10]], [10,20],
                        [10, 30], [10, 40], [10, 50], [10,60])
        
        road = Road('red', road_position)
        gantry.move_to(road)
        self.assertIsNone(gantry.current_suckable)
        
        gantry.pick_up(road)
        self.assertIs(gantry.current_suckable, road)
        
        gantry.place(gantry.red_bin)
        self.assertIsNone(gantry.current_suckable)
        self.assertEqual(gantry.x_motor.current_cartisan, gantry.red_bin[0].position[0])
        self.assertEqual(gantry.y_motor.current_cartisan, gantry.red_bin[0].position[1] - mount.offset)
        
    def test_pick_up_tile(self):
        tile_position = [50., 20.]
        pump_1 = PumpAssembly(DCMotor(HAT_SETUP("motor_M3")), DCMotor(HAT_SETUP("motor_M4")), DCMotor(HAT_SETUP("motor_M1", "0x62")))
        pump_2 = PumpAssembly(DCMotor(HAT_SETUP("motor_M2", "0x62")), DCMotor(HAT_SETUP("motor_M3", "0x62")), DCMotor(HAT_SETUP("motor_M4", "0x62")))
        mount = Mount(Stepper(200, 8, HAT_SETUP('stepper1', "0x64"), HAT_CONTROL), pump_1, pump_2)
        gantry = Gantry(Stepper(200, 8, HAT_SETUP('stepper2', "0x64"), HAT_CONTROL),
                        Stepper(200, 8, HAT_SETUP('stepper1', '0x66'), HAT_CONTROL),
                        mount, None, [[10,0]], [[10,10], [20,10], [30,10]], [10,20],
                        [10, 30], [10, 40], [10, 50], [10,60])
        
        hex = Hex("empty", 1, tile_position)
        gantry.move_to(hex)
        self.assertIsNone(gantry.current_suckable)
        
        gantry.pick_up(hex)
        self.assertIs(gantry.current_suckable, hex)
        
        gantry.place(gantry.tile_stacks)
        self.assertIsNone(gantry.current_suckable)
        self.assertEqual(gantry.x_motor.current_cartisan, gantry.tile_stacks[0].position[0])
        self.assertEqual(gantry.y_motor.current_cartisan, gantry.tile_stacks[0].position[1] + mount.offset)
        
    def test_no_more_tile_stacks(self):
        tile_position = [50., 20.]
        pump_1 = PumpAssembly(DCMotor(HAT_SETUP("motor_M3")), DCMotor(HAT_SETUP("motor_M4")), DCMotor(HAT_SETUP("motor_M1", "0x62")))
        pump_2 = PumpAssembly(DCMotor(HAT_SETUP("motor_M2", "0x62")), DCMotor(HAT_SETUP("motor_M3", "0x62")), DCMotor(HAT_SETUP("motor_M4", "0x62")))
        mount = Mount(Stepper(200, 8, HAT_SETUP('stepper1', "0x64"), HAT_CONTROL), pump_1, pump_2)
        gantry = Gantry(Stepper(200, 8, HAT_SETUP('stepper2', "0x64"), HAT_CONTROL),
                        Stepper(200, 8, HAT_SETUP('stepper1', '0x66'), HAT_CONTROL),
                        mount, None, [[10,0]], [[10,10], [20,10], [30,10]], [10,20],
                        [10, 30], [10, 40], [10, 50], [10,60])
        
        thick_tile = Tile(None, 12, tile_position)
        for i in range(2):
            gantry.move_to(thick_tile)
            gantry.pick_up(thick_tile)
            gantry.place(gantry.tile_stacks)
            
        gantry.move_to(thick_tile)
        gantry.pick_up(thick_tile)
        
        with self.assertRaises(AttributeError) as expected:
            gantry.place(gantry.tile_stacks)
    
    def test_tile_stacks(self):
        tile_position = [50., 20.]
        pump_1 = PumpAssembly(DCMotor(HAT_SETUP("motor_M3")), DCMotor(HAT_SETUP("motor_M4")), DCMotor(HAT_SETUP("motor_M1", "0x62")))
        pump_2 = PumpAssembly(DCMotor(HAT_SETUP("motor_M2", "0x62")), DCMotor(HAT_SETUP("motor_M3", "0x62")), DCMotor(HAT_SETUP("motor_M4", "0x62")))
        mount = Mount(Stepper(200, 8, HAT_SETUP('stepper1', "0x64"), HAT_CONTROL), pump_1, pump_2)
        gantry = Gantry(Stepper(200, 8, HAT_SETUP('stepper2', "0x64"), HAT_CONTROL),
                        Stepper(200, 8, HAT_SETUP('stepper1', '0x66'), HAT_CONTROL),
                        mount, None, [[10,0], [20,0]], [[10,10], [20,10], [30,10]], [10,20],
                        [10, 30], [10, 40], [10, 50], [10,60])
        
        thick_tile = Tile(None, 12, tile_position)
        for i in range(3):
            gantry.move_to(thick_tile)
            gantry.pick_up(thick_tile)
            gantry.place(gantry.tile_stacks)
        
        self.assertEqual(gantry.x_motor.current_cartisan, gantry.tile_stacks[1].position[0])
        self.assertEqual(gantry.y_motor.current_cartisan, gantry.tile_stacks[1].position[1] + mount.offset)
        
    def test_tile_stacks_remove(self):
        tile_position = [50., 20.]
        place_position = [1., 3,]
        pump_1 = PumpAssembly(DCMotor(HAT_SETUP("motor_M3")), DCMotor(HAT_SETUP("motor_M4")), DCMotor(HAT_SETUP("motor_M1", "0x62")))
        pump_2 = PumpAssembly(DCMotor(HAT_SETUP("motor_M2", "0x62")), DCMotor(HAT_SETUP("motor_M3", "0x62")), DCMotor(HAT_SETUP("motor_M4", "0x62")))
        mount = Mount(Stepper(200, 8, HAT_SETUP('stepper1', "0x64"), HAT_CONTROL), pump_1, pump_2)
        gantry = Gantry(Stepper(200, 8, HAT_SETUP('stepper2', "0x64"), HAT_CONTROL),
                        Stepper(200, 8, HAT_SETUP('stepper1', '0x66'), HAT_CONTROL),
                        mount, None, [[100,100], [75,25]], [], [10,20],
                        [10, 30], [10, 40], [10, 50], [10,60])
        
        thick_tile = Tile(None, 12, tile_position)
        empty_hex = EmptyHex(1,[], place_position)
        
        for i in range(3):
            copied_tile = copy.deepcopy(thick_tile)
            gantry.move_to(copied_tile)
            gantry.pick_up(copied_tile)
            gantry.place(gantry.tile_stacks)
        
        self.assertIsNone(gantry.current_suckable)
        gantry.pick_up(gantry.tile_stacks)
        self.assertEqual(gantry.x_motor.current_cartisan, gantry.tile_stacks[1].position[0])
        self.assertEqual(gantry.y_motor.current_cartisan, gantry.tile_stacks[1].position[1] + mount.offset)
        
        gantry.place(copy.deepcopy(empty_hex))
        self.assertIsNone(gantry.current_suckable)
        self.assertEqual(gantry.x_motor.current_cartisan, place_position[0])
        self.assertEqual(gantry.y_motor.current_cartisan, place_position[1] + mount.offset)
        self.assertTrue(len(gantry.tile_stacks[1]) == 0)
        
        gantry.pick_up(gantry.tile_stacks)
        self.assertEqual(gantry.x_motor.current_cartisan, gantry.tile_stacks[0].position[0])
        self.assertEqual(gantry.y_motor.current_cartisan, gantry.tile_stacks[0].position[1] + mount.offset)
        
    def test_tile_stacks_remove_same_tile(self):
        tile_position = [50., 20.]
        place_position = [1., 3,]
        pump_1 = PumpAssembly(DCMotor(HAT_SETUP("motor_M3")), DCMotor(HAT_SETUP("motor_M4")), DCMotor(HAT_SETUP("motor_M1", "0x62")))
        pump_2 = PumpAssembly(DCMotor(HAT_SETUP("motor_M2", "0x62")), DCMotor(HAT_SETUP("motor_M3", "0x62")), DCMotor(HAT_SETUP("motor_M4", "0x62")))
        mount = Mount(Stepper(200, 8, HAT_SETUP('stepper1', "0x64"), HAT_CONTROL), pump_1, pump_2)
        gantry = Gantry(Stepper(200, 8, HAT_SETUP('stepper2', "0x64"), HAT_CONTROL),
                        Stepper(200, 8, HAT_SETUP('stepper1', '0x66'), HAT_CONTROL),
                        mount, None, [[100,100], [75,25]], [], [10,20],
                        [10, 30], [10, 40], [10, 50], [10,60])
        
        thick_tile = Tile(None, 12, tile_position)
        empty_hex = EmptyHex(1,[], place_position)
        
        for i in range(3):
            # copied_tile = copy.deepcopy(thick_tile)
            # since we are pulling the same tile, we are cuasing some memory issues. We should only pick up a designated object in memory
            # not a reference to the same one
            gantry.move_to(thick_tile)
            gantry.pick_up(thick_tile)
            gantry.place(gantry.tile_stacks)

        gantry.pick_up(gantry.tile_stacks)
        
        gantry.place(copy.deepcopy(empty_hex))
        
        gantry.pick_up(gantry.tile_stacks)
        self.assertIs(gantry.current_suckable, thick_tile)
        self.assertNotEqual(gantry.x_motor.current_cartisan, gantry.tile_stacks[0].position[0])
        self.assertNotEqual(gantry.y_motor.current_cartisan, gantry.tile_stacks[0].position[1] + mount.offset)
            
    
if __name__ == '__main__':
    unittest.main()