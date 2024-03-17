from catan_objects.Motor import *
from unit_tests.motor_test_methods import *

import unittest

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
    
    def test_init_ABC(self):
        with self.assertRaises(TypeError) as expected:
            motor = Motor(HAT_SETUP('stepper1'))
            
    def test_init_DC_hat(self):
        motor = DCMotor(HAT_SETUP("motor1"))
        self.assertIn(0x60, motor.s_hats)
        self.assertEqual(motor.motor.type, 'M1')
        
    def test_init_DC_hat_invalid(self):
        motor = DCMotor(HAT_SETUP("fake"))
        self.assertIs(motor.motor, None)
        
    def test_init_DC_multiple_hat(self):
        motor = DCMotor(HAT_SETUP("motor1"))
        motor2 = DCMotor(HAT_SETUP("motor2"))
        
        self.assertIn(0x60, motor.s_hats)
        self.assertEqual(len(motor.s_hats), 1)
        self.assertIs(motor.s_hats, motor2.s_hats)
        
    def test_init_DC_hat_multiple(self):
        motor1 = DCMotor(HAT_SETUP("motor1"))
        motor2 = DCMotor(HAT_SETUP("motor1",0x62))
        motor3 = DCMotor(HAT_SETUP("motor1",0x64))
        motor4 = DCMotor(HAT_SETUP("motor2",0x64))
        
        self.assertIn(0x60, motor1.s_hats)
        self.assertIn(0x62, motor1.s_hats)
        self.assertIn(0x64, motor1.s_hats)
        
        self.assertEqual(len(motor1.s_hats), 3)
        self.assertIs(motor1.s_hats, motor2.s_hats)
        self.assertIs(motor1.s_hats, motor3.s_hats)
        self.assertIs(motor1.s_hats, motor4.s_hats)
        
    def test_DC_start(self):
        motor1 = DCMotor(HAT_SETUP("motor1"))
        motor1.start(1)
        self.assertEqual(motor1.motor.throttle, 1)
        
        motor1.stop()
        self.assertEqual(motor1.motor.throttle, 0)
        
    def test_init_Stepper(self):
        steps_per_rotation = 200
        translator = 8
        
        stepper = Stepper(1, 0, None, None)
        
        stepper2 = Stepper(steps_per_rotation, translator, None, None)
        self.assertEqual(stepper2.distance_per_step, translator / steps_per_rotation)
        
    def test_init_Stepper_Hat_Setup(self):    
        stepper1 = Stepper(200, 8, HAT_SETUP('stepper1'), HAT_CONTROL)
        self.assertIn(0x60, stepper1.s_hats)
        self.assertEqual(stepper1.motor.type, 'A')
        
    def test_init_Stepper_move_to(self):    
        stepper1 = Stepper(200, 8, HAT_SETUP('stepper1'), HAT_CONTROL)
        self.assertEqual(stepper1.current_cartisan, 0.0)
        
        stepper1.move_to(10)
        self.assertEqual(stepper1.current_cartisan, 10.0)
        
    # Can test the rest of them, but they will change with actual motor stuff
        
if __name__ == '__main__':
    unittest.main()
    
# M = Stepper(200, 8, HAT_SETUP('stepper1'), HAT_CONTROL)
# M2 = Stepper(200, 8, HAT_SETUP('stepper2'), HAT_CONTROL)
# LM = LinkedMotor(M, M2, LINKED_HAT_CONTROL)
# LM.move_to([20, 10])
# M3 = Stepper(200, 8, HAT_SETUP('stepper1', '0x72'), HAT_CONTROL)

# DC = DCMotor(HAT_SETUP("motor1"))

# G1 = Stepper(200, 8, GPIO_SETUP(20, 32), GPIO_CONTROL, 20, 32)
# G1.move_to(20)