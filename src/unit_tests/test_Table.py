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
    
    def setUp(self):
        camera = CameraRig(DCMotor(HAT_SETUP("motor_M1")), DCMotor(HAT_SETUP("motor_M2")))
        camera.H = np.array([[ 1.0, 0.0, 0.0], [ 0.0, 1.0, 0.0], [ 0.0, 0.0, 1.0]])
        
        pump_1 = PumpAssembly(DCMotor(HAT_SETUP("motor_M3")), DCMotor(HAT_SETUP("motor_M4")), DCMotor(HAT_SETUP("motor_M1", "0x62")))
        pump_2 = PumpAssembly(DCMotor(HAT_SETUP("motor_M2", "0x62")), DCMotor(HAT_SETUP("motor_M3", "0x62")), DCMotor(HAT_SETUP("motor_M4", "0x62")))
        mount = Mount(Stepper(200, 8, HAT_SETUP('stepper1', "0x64"), HAT_CONTROL), pump_1, pump_2)
        catan_board = StandardSetup()
        gantry = Gantry(LinkedMotor(Stepper(200, 8, HAT_SETUP('stepper2', "0x64"), None),
                        Stepper(200, 8, HAT_SETUP('stepper1', '0x66'), None), LINKED_HAT_CONTROL),
                        mount, catan_board, [[10,0], [20,0], [30,0]], [[10,10], [20,10], [30,10]], [10,20],
                        [10, 30], [10, 40], [10, 50], [10,60])
        solenoid_1 = SingleDegreeComponent(DCMotor(HAT_SETUP("motor_M1", "0x68")), 1, 0)
        solenoid_2 = SingleDegreeComponent(DCMotor(HAT_SETUP("motor_M2", "0x68")), 1, 0)
        lift = Lift(Stepper(200, 8, GPIO_SETUP(20, 32), GPIO_CONTROL, 20, 32), 100, 0, solenoid_1, solenoid_2)
        cover = SingleDegreeComponent(Stepper(200, 8, HAT_SETUP('stepper2', "0x66"), HAT_CONTROL), 300, 0)
        self.table = Table(gantry, camera, lift, cover)
    
    def tearDown(self):
        # In running python the static var is created and not destroyed between tests
        Motor.s_hats.clear()
        
    def test_init(self):
        # Check to make sure setup is performed
        pass
        
    # def test_remove_robber(self):
    #     robber = self.table.camera.analyze_board(self.table.gantry.catan_board, [Robber()])
    #     numbers = self.table.camera.analyze_board(self.table.gantry.catan_board, [Number(10)])
    #     self.table.gantry.add_numbers(numbers)
    #     self.table.gantry.add_numbers(robber)
        
if __name__ == '__main__':
    unittest.main()