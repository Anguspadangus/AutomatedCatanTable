from objects.BoardComponents import *
from collections import deque
import random
import copy
import json

class Board():
    def __init__(self, configuration, unit = 1, position = (0,0)):
        # Position of the btm left center of hexigon in world position
        self.position = position
        # The possible spaces on the catan board
        self.empty_spaces = [EmptyHex(unit, config[0][2],
                                       (config[0][1][0]+self.position[0], config[0][1][1]+self.position[1])) for config in configuration]
        
        # The resources on the catan board
        self.resources = [config[1] for config in configuration]
        # The numbers on the catan board
        self.numbers = [config[2] for config in configuration]
        # Position of the deseret tile
        self.desert_position = self.load_desert()

        # Setting the location of the resources and numbers via the spaces they currently occupy
        # IE how they match up to the board
        for i, config in enumerate(self.resources):
            config.update_position(self.empty_spaces[i].shape.xy)
                
            self.numbers[i].update_position(self.empty_spaces[i].shape.xy)
        
        # Remove the desert number tile of 0
        desert_number = [x for x in self.numbers if x.shape.center == self.desert_position][0]
        self.numbers.remove(desert_number)
        
        # Empty variables which will get populated later
        self.resource_deque = deque()
        self.number_deque = deque()
        
    # Remove numbers from an already set board randomly
    def remove_numbers(self):
        removal_positions_x = []
        removal_positions_y = []
        while len(self.numbers) != 0:
            random_number = random.choice(self.numbers)
            self.numbers.remove(random_number)
            self.number_deque.append(random_number)
            
            removal_positions_x.append(random_number.shape.center[0])
            removal_positions_y.append(random_number.shape.center[1])
            
        return removal_positions_x, removal_positions_y
    
    # Remove resources from an already set board randomly
    def remove_resources(self):
        removal_positions_x = []
        removal_positions_y = []
        while len(self.resources) != 0:
            random_resource = random.choice(self.resources)
            self.resources.remove(random_resource)
            self.resource_deque.append(random_resource)
            
            removal_positions_x.append(random_resource.shape.xy[0])
            removal_positions_y.append(random_resource.shape.xy[1])
            
        return removal_positions_x, removal_positions_y
    
    # Clears the Board
    def clear_board(self):
        self.remove_numbers()
        self.remove_resources()
    
    # Updates the neighbors of a hex given the possible emptyHexes and the placed Hex
    def update_neighbors(self, hex, empty_hexes):
        for empty_hex in empty_hexes:
            if hex.name in empty_hex.neighbors:
                empty_hex.neighbor_count += 1
    
    # I do not update the name of the hex after it was placed, so could not run this multiple times programmatically.
    # Would need to create a new board instance.
    def place_resources(self):
        # assuming its completely empty
        # Want to make a deepcopy so we can reuse the empty hexes
        copy_empty_spaces = copy.deepcopy(self.empty_spaces)
        
        # Bool to check if desert has been placed yet, avoid recursion
        desert_placed = False
        
        rescource_postions_x = []
        rescource_postions_y = []
            
        while len(self.resource_deque) != 0:
            # Select random empty tile
            available_hex = self.select_empty_tile_with_neighbors(copy_empty_spaces)
            copy_empty_spaces.remove(available_hex)
            
            # Select top of deque
            removed_resource = self.resource_deque.pop()
            self.update_neighbors(removed_resource, copy_empty_spaces)
            
            # Check if the resource removed was the desert Hex, the update the new position
            if (removed_resource.shape.xy == self.desert_position and not desert_placed):
                self.desert_position = available_hex.shape.xy
                self.save_desert()
                desert_placed = True
                
            removed_resource.update_position(available_hex.shape.xy)
            
            rescource_postions_x.append(removed_resource.shape.xy[0])
            rescource_postions_y.append(removed_resource.shape.xy[1])
    
        return rescource_postions_x, rescource_postions_y
    
    def select_empty_tile(self, empty_spaces):
        random_available_hex = random.choice(empty_spaces)
        return random_available_hex
    
    # Algorithym for choosing where to place a tile
    def select_empty_tile_with_neighbors(self, empty_spaces):
        empty_available_hexes = list(filter(lambda space : space.neighbor_count >= 2, empty_spaces))
        random_available_hex = random.choice(empty_available_hexes)
        return random_available_hex
    
    # Same implementation as PlaceResources(). But we can place the numbers in any order
    def place_numbers(self):
        copy_empty_spaces = copy.deepcopy(self.empty_spaces)
        
        number_postions_x = []
        number_postions_y = []
        
        while len(self.number_deque) != 0:
            # Select random empty tile
            available_hex = self.select_empty_tile(copy_empty_spaces)
            copy_empty_spaces.remove(available_hex)
            if available_hex.shape.xy != self.desert_position:
                removed_number = self.number_deque.pop()
                removed_number.update_position(available_hex.shape.xy)
                
                number_postions_x.append(removed_number.shape.center[0])
                number_postions_y.append(removed_number.shape.center[1])
    
        return number_postions_x, number_postions_y
    
    def place_board(self):
        self.place_resources()
        self.place_numbers()
        
    def load_desert(self):
        f = open('src\Algorithms\desertPosition.json')
        data = json.load(f)
        f.close()
        return tuple(data["pos"])

    def save_desert(self):
        with open('src\Algorithms\desertPosition.json', 'w') as f:
            json.dump({"pos" :self.desert_position}, f)         