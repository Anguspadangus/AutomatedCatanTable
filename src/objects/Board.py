from objects.tile import *
from collections import deque
import random
import copy
import json

class Board():
    def __init__(self, configuration, unit = 1, position = (0,0)):
        # Position of the btm left center of hexigon in world position
        self.m_position = position
        # The possible spaces on the catan board
        self.m_emptySpaces = [EmptyHex(unit, config[0][2],
                                       (config[0][1][0]+self.m_position[0], config[0][1][1]+self.m_position[1])) for config in configuration]
        
        # The resources on the catan board
        self.m_resources = [config[1] for config in configuration]
        # The numbers on the catan board
        self.m_numbers = [config[2] for config in configuration]
        # Position of the deseret tile
        self.m_desertPosition = self.LoadDesert()

        # Setting the location of the resources and numbers via the spaces they currently occupy
        # IE how they match up to the board
        for i, config in enumerate(self.m_resources):
            config.UpdatePosition(self.m_emptySpaces[i].m_shape.xy)
                
            self.m_numbers[i].UpdatePosition(self.m_emptySpaces[i].m_shape.xy)
        
        # Remove the desert number tile of 0
        desertNumber = [x for x in self.m_numbers if x.m_shape.center == self.m_desertPosition][0]
        self.m_numbers.remove(desertNumber)
        
        # Empty variables which will get populated later
        self.m_resourceDeque = deque()
        self.m_numberDeque = deque()
        
    # Remove numbers from an already set board randomly
    def RemoveNumbers(self):
        removalPositionsX = []
        removalPositionsY = []
        while len(self.m_numbers) != 0:
            randomNumber = random.choice(self.m_numbers)
            self.m_numbers.remove(randomNumber)
            self.m_numberDeque.append(randomNumber)
            
            removalPositionsX.append(randomNumber.m_shape.center[0])
            removalPositionsY.append(randomNumber.m_shape.center[1])
            
        return removalPositionsX, removalPositionsY
    
    # Remove resources from an already set board randomly
    def RemoveResources(self):
        removalPositionsX = []
        removalPositionsY = []
        while len(self.m_resources) != 0:
            randomResource = random.choice(self.m_resources)
            self.m_resources.remove(randomResource)
            self.m_resourceDeque.append(randomResource)
            
            removalPositionsX.append(randomResource.m_shape.xy[0])
            removalPositionsY.append(randomResource.m_shape.xy[1])
            
        return removalPositionsX, removalPositionsY
    
    # Clears the Board
    def ClearBoard(self):
        self.RemoveNumbers()
        self.RemoveResources()
    
    # Updates the neighbors of a hex given the possible emptyHexes and the placed Hex
    def UpdateNeighbors(self, hex, emptyHexes):
        for emptyHex in emptyHexes:
            if hex.m_name in emptyHex.m_neighbors:
                emptyHex.m_neighborCount += 1
    
    # I do not update the name of the hex after it was placed, so could not run this multiple times programmatically.
    # Would need to create a new board instance.
    def PlaceResources(self):
        # assuming its completely empty
        # Want to make a deepcopy so we can reuse the empty hexes
        CopyEmptySpaces = copy.deepcopy(self.m_emptySpaces)
        
        # Bool to check if desert has been placed yet, avoid recursion
        desertPlaced = False
        
        rescourcePostionsX = []
        rescourcePostionsY = []
            
        while len(self.m_resourceDeque) != 0:
            # Select random empty tile
            availableHex = self.SelectEmptyTileWithNeighbors(CopyEmptySpaces)
            CopyEmptySpaces.remove(availableHex)
            
            # Select top of deque
            removedResource = self.m_resourceDeque.pop()
            self.UpdateNeighbors(removedResource, CopyEmptySpaces)
            
            # Check if the resource removed was the desert Hex, the update the new position
            if (removedResource.m_shape.xy == self.m_desertPosition and not desertPlaced):
                self.m_desertPosition = availableHex.m_shape.xy
                self.SaveDesert()
                desertPlaced = True
                
            removedResource.UpdatePosition(availableHex.m_shape.xy)
            
            rescourcePostionsX.append(removedResource.m_shape.xy[0])
            rescourcePostionsY.append(removedResource.m_shape.xy[1])
    
        return rescourcePostionsX, rescourcePostionsY
    
    def SelectEmptyTile(self, emptySpaces):
        randomAvailableHex = random.choice(emptySpaces)
        return randomAvailableHex
    
    # Algorithym for choosing where to place a tile
    def SelectEmptyTileWithNeighbors(self, emptySpaces):
        emptyAvailableHexes = list(filter(lambda space : space.m_neighborCount >= 2, emptySpaces))
        randomAvailableHex = random.choice(emptyAvailableHexes)
        return randomAvailableHex
    
    # Same implementation as PlaceResources(). But we can place the numbers in any order
    def PlaceNumbers(self):
        CopyEmptySpaces = copy.deepcopy(self.m_emptySpaces)
        
        numberPostionsX = []
        numberPostionsY = []
        
        while len(self.m_numberDeque) != 0:
            # Select random empty tile
            availableHex = self.SelectEmptyTile(CopyEmptySpaces)
            CopyEmptySpaces.remove(availableHex)
            if availableHex.m_shape.xy != self.m_desertPosition:
                removedNumber = self.m_numberDeque.pop()
                removedNumber.UpdatePosition(availableHex.m_shape.xy)
                
                numberPostionsX.append(removedNumber.m_shape.center[0])
                numberPostionsY.append(removedNumber.m_shape.center[1])
    
        return numberPostionsX, numberPostionsY
    
    def PlaceBoard(self):
        self.PlaceResources()
        self.PlaceNumbers()
        
    def LoadDesert(self):
        f = open('Algorithms\desertPosition.json')
        data = json.load(f)
        f.close()
        return tuple(data["pos"])

    def SaveDesert(self):
        with open('Algorithms\desertPosition.json', 'w') as f:
            json.dump({"pos" :self.m_desertPosition}, f)         