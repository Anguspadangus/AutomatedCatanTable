class Piece():
    def __init__(self, height, color):
        self.m_height = height
        self.m_color = color
        
class Robber(Piece):
    def __init__(self):
        super().__init__(self, 32, 'grey')
        
class Road(Piece):
    def __init__(self, color):
        super().__init__(self, 5, color)
        
class City(Piece):
    def __init__(self, color):
        super().__init__(self, 19, color)
        
class Settlememt(Piece):
    def __init__(self, color):
        super().__init__(self, 12, color)