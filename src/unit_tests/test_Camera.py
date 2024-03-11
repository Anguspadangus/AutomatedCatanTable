from unit_tests.StandardBoard import StandardSetup
from catan_objects.BoardComponents import *
from catan_objects.TableComponents import CameraRig
from catan_objects.Motor import *
from unit_tests.motor_test_methods import *

import unittest
import os
import numpy as np

class CVTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.K = np.array([[113.49354735654141, 0.0, 371.5786534104595], [0.0, 116.6060998517777, 205.3861581256824], [0.0, 0.0, 1.0]])
        cls.D = np.array([[0.12694667308062602], [0.6454345033192549], [-0.5465056949757663], [0.25172851391836865]])
        cls.H = np.array([[ 3.98379589e-01, 8.28098023e-02, 5.48000000e+02], [-6.12605764e-03,-3.84345357e-01, 1.03000000e+02], [-6.28872633e-05, 2.09711523e-04, 1.00000000e+00]])
        
        cls.images = []
        for file in os.listdir('src\\test\\images\\'):
            cls.images.extend(['src\\test\\images\\' + file])
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_init(self):
        camera = CameraRig(DCMotor(HAT_SETUP("motor_M1")), None)
        camera.K = self.K
        camera.D = self.D
        camera.H = self.H
        
    def test_pose(self):
        camera = CameraRig(DCMotor(HAT_SETUP("motor_M1")), None)
        # camera.K = np.array([[1.0, 0.0, 0.0], [0.0, 1., 0.0], [0.0, 0.0, 1.0]])
        # camera.D = np.array([[0.0], [0.0], [0.0], [0.0]])
        camera.H = np.array([[ 1.0, 0.0, 0.0], [ 0.0, 1.0, 0.0], [ 0.0, 0.0, 1.0]])
        
        uv = [10,10]
        xy = camera.convert_to_world_single(uv)
        self.assertEqual(xy, uv)

        x_offset = 10.
        y_offset = 25.
        camera2 = CameraRig(DCMotor(HAT_SETUP("motor_M1")), None, [x_offset, y_offset])
        camera2.H = np.array([[ 1.0, 0.0, 0.0], [ 0.0, 1.0, 0.0], [ 0.0, 0.0, 1.0]])
        xy = camera2.convert_to_world_single(uv)
        self.assertEqual([uv[0] + x_offset, uv[1] + y_offset], xy)
    
    def test_pose_list(self):
        camera = CameraRig(DCMotor(HAT_SETUP("motor_M1")), None)
        camera.H = np.array([[ 1.0, 0.0, 0.0], [ 0.0, 1.0, 0.0], [ 0.0, 0.0, 1.0]])
    
        uvs = [[0,0], [10, 10], [20., 25.]]
        xys = camera.convert_to_world(uvs)
        self.assertListEqual(uvs, xys)
        
    def test_set_image(self):
        camera = CameraRig(DCMotor(HAT_SETUP("motor_M1")), None)
        self.assertIs(camera.image, None)
        camera.load_image(self.images[0])
        # print(type(camera.image))
        # self.assertIs(camera.image, np.ndarray)
        self.assertIsNotNone(camera.image)
        
        saved_image = camera.image
        camera.undistort_picture()
        self.assertFalse(np.array_equal(saved_image, camera.image))
        
    def test_analyze_board_numbers(self):
        camera = CameraRig(DCMotor(HAT_SETUP("motor_M1")), None)
        camera.H = np.array([[ 1.0, 0.0, 0.0], [ 0.0, 1.0, 0.0], [ 0.0, 0.0, 1.0]])
        catan_board = StandardSetup()
        catan_board.desert_position = catan_board.empty_spaces[5].position # for testing
        
        for image_path in self.images:
            camera.load_image(image_path)
            numbers = camera.analyze_board(catan_board, [Number()])
            # camera.display_on_image(numbers)
            self.assertEqual(len(numbers), 18)
            
    def test_analyze_board_pieces(self):
        camera = CameraRig(DCMotor(HAT_SETUP("motor_M1")), None)
        camera.H = np.array([[ 1.0, 0.0, 0.0], [ 0.0, 1.0, 0.0], [ 0.0, 0.0, 1.0]])
        catan_board = StandardSetup()
        catan_board.desert_position = catan_board.empty_spaces[5].position # for testing
        
        camera.load_image('src\\test\\images\\settlements1.jpeg')
        colors = ['red', 'blue', 'white', 'orange']
        for color in colors:
            pieces = camera.analyze_board(catan_board, [Settlememt(color), City(color), Road(color)])
            self.assertTrue(len(pieces) != 0)
            # Maybe one day we'll get this good
            # self.assertTrue(any(isinstance(piece, Settlememt) for piece in pieces))
            # self.assertTrue(any(isinstance(piece, City) for piece in pieces))
            # self.assertTrue(any(isinstance(piece, Road) for piece in pieces))
            
    def test_analyze_board_robber(self):
        camera = CameraRig(DCMotor(HAT_SETUP("motor_M1")), None)
        camera.H = np.array([[ 1.0, 0.0, 0.0], [ 0.0, 1.0, 0.0], [ 0.0, 0.0, 1.0]])
        catan_board = StandardSetup()
        catan_board.desert_position = catan_board.empty_spaces[5].position # for testing
        
        camera.load_image('src\\test\\images\\settlements1.jpeg')
        robber = camera.analyze_board(catan_board, [Robber()])
        self.assertTrue(len(robber) != 0)

if __name__ == '__main__':
    unittest.main()