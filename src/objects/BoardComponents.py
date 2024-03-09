from matplotlib.patches import RegularPolygon, Circle
import abc
import math

class Suckable():
    def __init__(self, height, suction_type = None, xy = [0,0]):
        self.suction_type = suction_type
        self.height = height
        self.position = xy
        
    def update_position(self, position):
        self.position = position
        
class Piece(Suckable):
    # Class static, defines range for colors
    __color_dictionary = {'grey' : [(110,50,60), (125,100,120)],
                        'blue' : [(100, 150, 100), (120, 255, 255)],
                        'red' : [(170, 190, 50), (180, 255, 125)],
                        'orange' : [(10, 150, 100), (20, 255, 255)],
                        'white': [(100,30,200), (150,60,255)]}
    
    def __init__(self, height, color, area, xy = [0,0]):
        self.color = Piece.__color_dictionary[color]
        self.area = area
        super().__init__(height, 'universal', xy)
        
class Robber(Piece):
    def __init__(self, xy = [0,0]):
        super().__init__(32, 'grey', [20000,30000], xy)
        
class Road(Piece):
    def __init__(self, color, xy = [0,0]):
        super().__init__(5, color, [4000,7000], xy)
        
class City(Piece):
    def __init__(self, color, xy = [0,0]):
        super().__init__(19, color, [15000,22000], xy)
        
class Settlememt(Piece):
    def __init__(self, color, xy = [0,0]):
        super().__init__(12, color, [7000,15000], xy)
        
"""----------------------------------------------------"""

# Base class of all Catan tiles. Has a shape and a color.
class Tile(Suckable):
    def __init__(self, shape, height = 0, xy = [0,0]):
        self.shape = shape
        super().__init__(height, 'cup', xy)
        return
    
    def update_position(self, xy):
        self.position = xy
        
class Number(Tile):
    def __init__(self, radius = 10, xy = [0,0]):
        super().__init__(Circle(xy, radius=radius), 1, xy)
        
# Resource Hex, has a hexagonal radius, a name, and a center position
class Hex(Tile):
    def __init__(self, name, radius, xy = [0,0]):
        super().__init__(RegularPolygon(xy, 6, radius=radius), 2, xy)
        self.name = name

class Container(abc.ABC):
    def __init__(self, position, max_height = math.inf):
        self.position = position
        self.stack = []
        self.stack_height = 0
        self.max_height = max_height
    
    def __len__(self):
        return len(self.stack)    
    
    @abc.abstractmethod
    def push(self, object):
        pass
    
    @abc.abstractmethod
    def pop(self):
        pass

# Stack of tiles to be manipulated with 
class TileStack(Container):
    def __init__(self, position, max_height = 30):
        super().__init__(position, max_height)
        
    def push(self, tile):
        if self.stack_height + tile.height <= self.max_height:
            tile.position = self.position
            self.stack.append(tile)
            self.stack_height += tile.height
            return True
        
        return False
    
    def pop(self):
        if self.stack:
            tile = self.stack.pop()
            self.stack_height -= tile.height
            return tile
        
        return None   

class Bin(Container):
    def __init__(self, position):
        super().__init__(position)
    
    def push(self, obj):
        obj.position = self.position
        return True
    
    def pop(self):
        return None
       
# The possible locations in a catan set for a resource card to be placed
# Uses neighbors to determine if a hex can be placed, 0 represents border
'''
     / \ / \ / \ 
    | Q | R | S |
   / \ / \ / \ / \
  | M | N | O | P |
 / \ / \ / \ / \ / \
| H | I | J | K | L |
 \ / \ / \ / \ / \ /
  | D | E | F | G |
   \ / \ / \ / \ /
    | A | B | C | 
     \ / \ / \ /
'''
# what if empty hexes where also tile stacks? in that way we could calculate the height of where to put numbers
class EmptyHex(Tile):
    def __init__(self, radius, neighbors, xy = [0,0]):
        super().__init__(RegularPolygon(xy, 6, radius=radius), 0, xy)
        self.neighbors = neighbors
        self.neighbor_count = 0
        for neighbor in neighbors:
            if neighbor == '0':
                self.neighbor_count += 1