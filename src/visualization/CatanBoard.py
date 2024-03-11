from visualization.tile import *
from collections import deque
import random
import copy

class CatanBoard():
    def __init__(self, configuration, unit = 1):
        # The possible spaces on the catan board
        self.m_emptySpaces = [EmptyHex(unit, config[0][0], config[0][2], config[0][1]) for config in configuration]
        # The resources on the catan board
        self.m_resources = [config[1] for config in configuration]
        # The numbers on the catan board
        self.m_numbers = [config[2] for config in configuration]

        # Setting the location of the resources and numbers via the spaces they currently occupy
        # IE how they match up to the board
        for i, config in enumerate(self.m_resources):
            config.UpdatePosition(self.m_emptySpaces[i].m_shape.xy)
            if config.m_name == 'desert':
                desertHex = config.m_shape.xy
                
            self.m_numbers[i].UpdatePosition(self.m_emptySpaces[i].m_shape.xy)
        
        # Remove the desert number tile of 0
        desertNumber = [x for x in self.m_numbers if x.m_shape.center == desertHex][0]
        self.m_numbers.remove(desertNumber)
        
        # Empty variables which will get populated later
        self.desertPosition = None
        self.m_newBoardConfigurationResources = deque()
        self.m_newBoardConfigurationNumbers = deque()
        self.m_resourceDeque = deque()
        self.m_numberDeque = deque()
        
    # Remove numbers from an already set board randomly
    def RemoveNumbers(self):
        while len(self.m_numbers) != 0:
            randomNumber = random.choice(self.m_numbers)
            self.m_numbers.remove(randomNumber)
            self.m_numberDeque.append(randomNumber)
    
    # Remove resources from an already set board randomly
    def RemoveResources(self):
        while len(self.m_resources) != 0:
            randomResource = random.choice(self.m_resources)
            self.m_resources.remove(randomResource)
            self.m_resourceDeque.append(randomResource)
    
    # Clears the Board
    def ClearBoard(self):
        self.RemoveNumbers()
        self.RemoveResources()
    
    # Updates the neighbors of a hex given the possible emptyHexes and the placed Hex
    def UpdateNeighbors(self, hex, emptyHexes):
        for emptyHex in emptyHexes:
            if hex.m_name in emptyHex.m_neighbors:
                emptyHex.m_neighborCount += 1
                
    def PlaceResources(self):
        # assuming its completely empty
        # Want to make a deepcopy so we can reuse the empty hexes
        CopyEmptySpaces = copy.deepcopy(self.m_emptySpaces)
            
        while len(self.m_resourceDeque) != 0:
            # Select random empty tile
            availableHex = self.SelectEmptyTileWithNeighbors(CopyEmptySpaces)
            CopyEmptySpaces.remove(availableHex)
            self.UpdateNeighbors(availableHex, CopyEmptySpaces)
            
            # Select top of deque
            removedResource = self.m_resourceDeque.pop()
            removedResource.UpdatePosition(availableHex.m_shape.xy)
            
            # Store loaction of desert, so to not place a number on it
            if(removedResource.m_name == 'desert'):
                self.desertPosition = removedResource.m_shape.xy
            
            self.m_newBoardConfigurationResources.append(removedResource)
    
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
        
        while len(self.m_numberDeque) != 0:
            # Select random empty tile
            availableHex = self.SelectEmptyTile(CopyEmptySpaces)
            CopyEmptySpaces.remove(availableHex)
            if availableHex.m_shape.xy != self.desertPosition:
                removedNumber = self.m_numberDeque.pop()
                removedNumber.UpdatePosition(availableHex.m_shape.xy)
                
                self.m_newBoardConfigurationNumbers.append(removedNumber)
            
    def PlaceBoard(self):
        self.PlaceResources()
        self.PlaceNumbers()