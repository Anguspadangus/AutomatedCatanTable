from matplotlib.patches import RegularPolygon, Circle

# Base class of all Catan tiles. Has a shape and a color.
class Tile():
    def __init__(self, shape):
        self.m_shape = shape
        return
    
    def UpdatePosition(self, xy):
        if(isinstance(self.m_shape, Circle)):
            self.m_shape.center = xy
        else:
            self.m_shape.xy = xy

# Resource Hex, has a hexagonal radius, a name (like desert) and a center position
class Hex(Tile):
    def __init__(self, name, radius, center = (0,0)):
        Tile.__init__(self, RegularPolygon(center, 6, radius=radius))
        self.m_name = name
    
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
class EmptyHex(Tile):
    def __init__(self, radius, neighbors, center):
        Tile.__init__(self, RegularPolygon(center, 6, radius=radius))
        self.m_neighbors = neighbors
        self.m_neighborCount = 0
        for neighbor in neighbors:
            if neighbor == '0':
                self.m_neighborCount += 1 
           
class Number(Tile):
    def __init__(self, radius):
        Tile.__init__(self, Circle((0,0), radius=radius))
            