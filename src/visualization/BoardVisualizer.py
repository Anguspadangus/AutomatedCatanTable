import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import copy

class BoardVisualizer():
    def __init__(self, catan_board):
        # initalizing figure
        self.m_fig, self.m_ax = plt.subplots()
        self.m_ax.set_xlim(-10,20)
        self.m_ax.set_ylim(-10,20)
        
        # The inital setup of the board, from the board's constructor
        self.m_initalConfigurationHexes = copy.deepcopy(catan_board.m_resources)
        self.m_initalConfigurationNumbers = copy.deepcopy(catan_board.m_numbers)
        self.m_totalFrames = len(self.m_initalConfigurationHexes)
        
        # The stakcs of numbers and hexes after removing them from the catan_board
        catan_board.ClearBoard()
        self.m_removalSequenceHexes = copy.deepcopy(catan_board.m_resourceDeque)
        self.m_removalSequenceNumbers = copy.deepcopy(catan_board.m_numberDeque)
        
        # The place sequence of the board, the removal sequences differ by the position of the placements
        catan_board.PlaceBoard()
        self.m_placeSequenceHexes = copy.deepcopy(catan_board.m_newBoardConfigurationResources)
        self.m_placeSequenceNumbers = copy.deepcopy(catan_board.m_newBoardConfigurationNumbers)
    
    # Initial setup for the board
    def Init(self):
        # Python doesn't offer a stack or queue in the std so have to use somehting like this
        for hexagon in reversed(self.m_removalSequenceHexes):
            self.m_ax.add_patch(hexagon.m_shape)

        for number in reversed(self.m_removalSequenceNumbers):     
            self.m_ax.add_patch(number.m_shape)

        return []
    
    # The set by step frames of the removing and placing
    def Update(self, frame):
        # Removing numbers then hexes
        if frame < (self.m_totalFrames * 2) - 1:
            # For some reason need to pop each artist rendering 4 times in matplotlib 3.6.3.
            # In earlier versions, it is 3. In 3.7, you can't do it.
            for i in range(4):
                self.m_ax.patches.pop()
        # Placing of hexes
        elif frame < (self.m_totalFrames * 3) - 1:
            removedHex = self.m_placeSequenceHexes.popleft()
            self.m_ax.add_patch(removedHex.m_shape)
        # Placing of numbers
        else:
            removedNumber = self.m_placeSequenceNumbers.popleft()
            self.m_ax.add_patch(removedNumber.m_shape)

        return []
    
    # Animation function
    def Run(self):
        # Create the animation
        animation = FuncAnimation(self.m_fig, self.Update, frames=(self.m_totalFrames*4 - 2), init_func=self.Init, blit=True, repeat=False)

        plt.show()