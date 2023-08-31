from matplotlib import colors as mcolors
from matplotlib.patches import RegularPolygon, Circle

# Base class of all Catan tiles. Has a shape and a color.
class Tile():
    def __init__(self, shape, color = 'b'):
        self.m_shape = shape
        self.UpdateFaceColor(color)
        return
    
    def UpdateFaceColor(self, color):
        self.m_color = color
        self.m_shape.set_facecolor(mcolors.to_rgba(color))
    
    def UpdatePosition(self, xy):
        if(isinstance(self.m_shape, Circle)):
            self.m_shape.center = xy
        else:
            self.m_shape.xy = xy

# Resource Hex, has a hexagonal radius, a name (like desert) and a center position
class Hex(Tile):
    def __init__(self, radius, name, center = (0,0)):
        Tile.__init__(self, RegularPolygon(center, 6, radius=radius))
        self.m_name = name
        
        if name == 'desert':
            self.UpdateFaceColor(mcolors.CSS4_COLORS['sandybrown'])
        elif name == 'sheep':
            self.UpdateFaceColor(mcolors.CSS4_COLORS['lawngreen'])
        elif name == 'wheat':
            self.UpdateFaceColor(mcolors.CSS4_COLORS['yellow'])
        elif name == 'brick':
            self.UpdateFaceColor(mcolors.CSS4_COLORS['darkorange'])
        elif name == 'wood':
            self.UpdateFaceColor(mcolors.CSS4_COLORS['forestgreen'])
        elif name == 'ore':
            self.UpdateFaceColor(mcolors.CSS4_COLORS['lightgrey'])
        else:
            # If it is none of these, not a catan piece
            raise TypeError("Must be correct Resource")
    
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
    def __init__(self, radius, name, neighbors, center):
        Tile.__init__(self, RegularPolygon(center, 6, radius=radius))
        self.m_name = name
        self.m_neighbors = neighbors
        self.m_neighborCount = 0
        for neighbor in neighbors:
            if neighbor == '0':
                self.m_neighborCount += 1 
           
class Number(Tile):
    def __init__(self, value, radius):
        Tile.__init__(self, Circle((0,0), radius=radius), mcolors.CSS4_COLORS['tan'])
        self.m_value = value
            