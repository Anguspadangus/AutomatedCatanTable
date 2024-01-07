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
        current_desert_location = self.board.m_desertPosition
        new_desert_location = self.board.m_emptySpaces[3].m_shape.xy
        
        self.board.m_desertPosition = new_desert_location
        self.board.SaveDesert()
        self.assertEqual(self.board.m_desertPosition, new_desert_location)
        
        board2 = StandardSetup()
        self.assertEqual(board2.m_desertPosition, new_desert_location)
        
        board2.m_desertPosition = current_desert_location
        board2.SaveDesert()
        
        # Hasn't been read yet from JSON
        self.assertNotEqual(self.board.m_desertPosition, current_desert_location)
        
    def test_RemoveResources(self):
        available_spaces_x = [space.m_shape.xy[0] for space in self.board.m_emptySpaces]
        available_spaces_y = [space.m_shape.xy[1] for space in self.board.m_emptySpaces]
        
        resource_removal_order_x, resource_removal_order_y = self.board.RemoveResources()
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
        available_spaces_x = [space.m_shape.xy[0] for space in self.board.m_emptySpaces]
        available_spaces_y = [space.m_shape.xy[1] for space in self.board.m_emptySpaces]
        
        number_removal_order_x, number_removal_order_y = self.board.RemoveNumbers()
        self.assertEqual(len(number_removal_order_x)+1, len(available_spaces_x))
        self.assertEqual(len(number_removal_order_y)+1, len(available_spaces_y))
        
        number_removal_order_x.append(self.board.m_desertPosition[0])
        number_removal_order_y.append(self.board.m_desertPosition[1])
        
        self.assertNotEqual(number_removal_order_x, available_spaces_x)
        self.assertNotEqual(number_removal_order_y, available_spaces_y)
        
        sorted_x  = sorted(number_removal_order_x)
        sorted_y  = sorted(number_removal_order_y)
        sorted_spaces_x = sorted(available_spaces_x)
        sorted_spaces_y = sorted(available_spaces_y)
        
        self.assertEqual(sorted_x, sorted_spaces_x)
        self.assertEqual(sorted_y, sorted_spaces_y)
        
    def test_PlaceResourse(self):
        _ = self.board.RemoveNumbers()
        resource_removal_order_x, resource_removal_order_y = self.board.RemoveResources()
        resource_place_order_x, resource_place_order_y = self.board.PlaceResources()
        
        self.assertNotEqual(resource_removal_order_x, resource_place_order_x)
        self.assertNotEqual(resource_removal_order_y, resource_place_order_y)
        
        sorted_remove_order_x = sorted(resource_removal_order_x)
        sorted_remove_order_y = sorted(resource_removal_order_y)
        sorted_place_order_x = sorted(resource_place_order_x)
        sorted_place_order_y = sorted(resource_place_order_y)
        
        self.assertEqual(sorted_remove_order_x, sorted_place_order_x)
        self.assertEqual(sorted_remove_order_y, sorted_place_order_y)

    def test_PlaceNumbers(self):
        number_removal_order_x, number_removal_order_y = self.board.RemoveNumbers()
        old_desert_position = self.board.m_desertPosition
        _ = self.board.RemoveResources()
        _ = self.board.PlaceResources()
        number_place_order_x, number_place_order_y = self.board.PlaceNumbers()
        new_desert_position = self.board.m_desertPosition
        
        self.assertNotEqual(number_removal_order_x, number_place_order_x)
        self.assertNotEqual(number_removal_order_y, number_place_order_y)
        
        sorted_remove_order_x = sorted(number_removal_order_x)
        sorted_remove_order_y = sorted(number_removal_order_y)
        sorted_place_order_x = sorted(number_place_order_x)
        sorted_place_order_y = sorted(number_place_order_y)
        
        self.assertNotEqual(sorted_remove_order_x, sorted_place_order_x)
        self.assertNotEqual(sorted_remove_order_y, sorted_place_order_y)
        
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