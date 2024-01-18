class Piece():
    # Class static, defines range for colors
    __colorDictionary = {'grey' : [(110,50,60), (125,100,120)],
                        'blue' : [(100, 150, 100), (120, 255, 255)],
                        'red' : [(170, 190, 50), (180, 255, 125)],
                        'orange' : [(10, 150, 100), (20, 255, 255)],
                        'white': [(100,30,200), (150,60,255)]}
    
    def __init__(self, height, color, area):
        self.m_height = height
        self.m_color = Piece.__colorDictionary[color]
        self.m_area = area
        
class Robber(Piece):
    def __init__(self):
        super().__init__(32, 'grey', [20000,30000])
        
class Road(Piece):
    def __init__(self, color):
        super().__init__(5, color, [4000,7000])
        
class City(Piece):
    def __init__(self, color):
        super().__init__(19, color, [15000,22000])
        
class Settlememt(Piece):
    def __init__(self, color):
        super().__init__(12, color, [7000,15000])