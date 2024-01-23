from objects.StandardBoard import StandardSetup
from Algorithms.imageProcessing import load_image, analyze_board
from objects.BoardComponents import *

import unittest
import os

class CVTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
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
    
    def test_NumberRecognizer(self):
        for image_path in self.images:
            b = StandardSetup()
            b.desert_position = b.empty_spaces[5].shape.xy # for testing
            image = load_image(image_path)
            locs = analyze_board(b, image)
            
            self.assertEqual(len(locs), 18, f'{image_path} does not have 18 numbers')
            
    def test_RobberRecognizer(self):
        for image_path in self.images:
            if "robber" in image_path:
                b = StandardSetup()
                b.desert_position = b.empty_spaces[5].shape.xy # for testing
                image = load_image(image_path)
                locs = analyze_board(b, image, [Robber()])
                
                self.assertGreaterEqual(len(locs), 1+18, f'{image_path} does not have 1 robber')
            
    # Many other tests could be made, but it isn't perfect in analysing all of the other objects

            
if __name__ == '__main__':
    unittest.main()