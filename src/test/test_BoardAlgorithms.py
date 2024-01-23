import unittest
from objects.StandardBoard import StandardSetup

class BoardTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        self.board = StandardSetup()
    
    def tearDown(self):
        pass
    
    def test_desertLocation(self):
        current_desert_location = self.board.desert_position
        new_desert_location = self.board.empty_spaces[3].shape.xy
        
        self.board.desert_position = new_desert_location
        self.board.save_desert()
        self.assertEqual(self.board.desert_position, new_desert_location)
        
        board2 = StandardSetup()
        self.assertEqual(board2.desert_position, new_desert_location)
        
        board2.desert_position = current_desert_location
        board2.save_desert()
        
        # Hasn't been read yet from JSON
        self.assertNotEqual(self.board.desert_position, current_desert_location)
        
    def test_RemoveResources(self):
        available_spaces_x = [space.shape.xy[0] for space in self.board.empty_spaces]
        available_spaces_y = [space.shape.xy[1] for space in self.board.empty_spaces]
        
        resource_removal_order_x, resource_removal_order_y = self.board.remove_resources()
        self.assertEqual(len(resource_removal_order_x), len(available_spaces_x))
        self.assertEqual(len(resource_removal_order_y), len(available_spaces_y))
        self.assertNotEqual(resource_removal_order_x, available_spaces_x)
        self.assertNotEqual(resource_removal_order_y, available_spaces_y)
        
        sorted_x  = sorted(resource_removal_order_x)
        sorted_y  = sorted(resource_removal_order_y)
        sorted_spaces_x = sorted(available_spaces_x)
        sorted_spaces_y = sorted(available_spaces_y)
        
        self.assertEqual(sorted_x, sorted_spaces_x)
        self.assertEqual(sorted_y, sorted_spaces_y)
        
    def test_RemoveNumbers(self):
        available_spaces_x = [space.shape.xy[0] for space in self.board.empty_spaces]
        available_spaces_y = [space.shape.xy[1] for space in self.board.empty_spaces]
        
        number_removal_order_x, number_removal_order_y = self.board.remove_numbers()
        self.assertEqual(len(number_removal_order_x)+1, len(available_spaces_x))
        self.assertEqual(len(number_removal_order_y)+1, len(available_spaces_y))
        
        number_removal_order_x.append(self.board.desert_position[0])
        number_removal_order_y.append(self.board.desert_position[1])
        
        self.assertNotEqual(number_removal_order_x, available_spaces_x)
        self.assertNotEqual(number_removal_order_y, available_spaces_y)
        
        sorted_x  = sorted(number_removal_order_x)
        sorted_y  = sorted(number_removal_order_y)
        sorted_spaces_x = sorted(available_spaces_x)
        sorted_spaces_y = sorted(available_spaces_y)
        
        self.assertEqual(sorted_x, sorted_spaces_x)
        self.assertEqual(sorted_y, sorted_spaces_y)
        
    def test_PlaceResourse(self):
        _ = self.board.remove_numbers()
        resource_removal_order_x, resource_removal_order_y = self.board.remove_resources()
        resource_place_order_x, resource_place_order_y = self.board.place_resources()
        
        self.assertNotEqual(resource_removal_order_x, resource_place_order_x)
        self.assertNotEqual(resource_removal_order_y, resource_place_order_y)
        
        sorted_remove_order_x = sorted(resource_removal_order_x)
        sorted_remove_order_y = sorted(resource_removal_order_y)
        sorted_place_order_x = sorted(resource_place_order_x)
        sorted_place_order_y = sorted(resource_place_order_y)
        
        self.assertEqual(sorted_remove_order_x, sorted_place_order_x)
        self.assertEqual(sorted_remove_order_y, sorted_place_order_y)

    def test_PlaceNumbers(self):
        number_removal_order_x, number_removal_order_y = self.board.remove_numbers()
        old_desert_position = self.board.desert_position
        _ = self.board.remove_resources()
        _ = self.board.place_resources()
        number_place_order_x, number_place_order_y = self.board.place_numbers()
        new_desert_position = self.board.desert_position
        
        self.assertNotEqual(number_removal_order_x, number_place_order_x)
        self.assertNotEqual(number_removal_order_y, number_place_order_y)
        
        sorted_remove_order_x = sorted(number_removal_order_x)
        sorted_remove_order_y = sorted(number_removal_order_y)
        sorted_place_order_x = sorted(number_place_order_x)
        sorted_place_order_y = sorted(number_place_order_y)
        
        sorted_remove_order_x.append(old_desert_position[0])
        sorted_remove_order_y.append(old_desert_position[1])
        sorted_place_order_x.append(new_desert_position[0])
        sorted_place_order_y.append(new_desert_position[1])
        
        sorted_remove_order_x = sorted(sorted_remove_order_x)
        sorted_remove_order_y = sorted(sorted_remove_order_y)
        sorted_place_order_x = sorted(sorted_place_order_x)
        sorted_place_order_y = sorted(sorted_place_order_y)
        
        self.assertEqual(sorted_remove_order_x, sorted_place_order_x)
        self.assertEqual(sorted_remove_order_y, sorted_place_order_y)
    
if __name__ == '__main__':
    unittest.main()