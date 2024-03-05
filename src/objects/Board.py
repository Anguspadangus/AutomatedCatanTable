from objects.BoardComponents import *
from collections import deque
import random
import copy
import json

class Board():
    def __init__(self, configuration, unit = 1):
        # The possible spaces on the catan board
        self.empty_spaces = [EmptyHex(unit, config[0][2],
                                       (config[0][1][0], config[0][1][1])) for config in configuration]
        
        # The resources on the catan board
        self.resources = [config[1] for config in configuration]
        # The numbers on the catan board
        self.numbers = None
        # Position of the deseret tile
        self.desert_position = self.load_desert()

        # Setting the location of the resources and numbers via the spaces they currently occupy
        # IE how they match up to the board
        for i, config in enumerate(self.resources):
            config.position = self.empty_spaces[i].position
        
    # Remove numbers from an already set board randomly
    def remove_numbers(self):
        removal_order = []
        while len(self.numbers) != 0:
            random_number = random.choice(self.numbers)
            self.numbers.remove(random_number)
            removal_order.append(random_number)
            
        return removal_order
    
    # Remove resources from an already set board randomly
    def remove_resources(self):
        removal_order = []
        while len(self.resources) != 0:
            random_resource = random.choice(self.resources)
            self.resources.remove(random_resource)
            removal_order.append(random_resource)
            
        return removal_order
    
    # Clears the Board
    def clear_board(self):
        numbers = self.remove_numbers()
        resources = self.remove_resources()
        return numbers, resources
    
    # Updates the neighbors of a hex given the possible emptyHexes and the placed Hex
    def update_neighbors(self, hex, empty_hexes):
        for empty_hex in empty_hexes:
            if hex.name in empty_hex.neighbors:
                empty_hex.neighbor_count += 1
    
    # I do not update the name of the hex after it was placed, so could not run this multiple times programmatically.
    # Would need to create a new board instance.
    def place_resources(self, resources):
        # assuming its completely empty
        # Want to make a deepcopy so we can reuse the empty hexes
        copy_empty_spaces = copy.deepcopy(self.empty_spaces)
        
        # Bool to check if desert has been placed yet, avoid recursion
        desert_placed = False
            
        while len(self.resource_deque) != 0:
            # Select random empty tile
            available_hex = self.select_empty_tile_with_neighbors(copy_empty_spaces)
            copy_empty_spaces.remove(available_hex)
            
            # Select top of deque
            removed_resource = resources.pop()
            self.update_neighbors(removed_resource, copy_empty_spaces)
            
            # Check if the resource removed was the desert Hex, the update the new position
            if (removed_resource.position == self.desert_position and not desert_placed):
                self.desert_position = available_hex.position
                self.save_desert()
                desert_placed = True
                
            removed_resource.position = available_hex.position
            
            self.resources.append(removed_resource)
    
    def select_empty_tile(self, empty_spaces):
        random_available_hex = random.choice(empty_spaces)
        return random_available_hex
    
    # Algorithym for choosing where to place a tile
    def select_empty_tile_with_neighbors(self, empty_spaces):
        empty_available_hexes = list(filter(lambda space : space.neighbor_count >= 2, empty_spaces))
        random_available_hex = random.choice(empty_available_hexes)
        return random_available_hex
    
    # Same implementation as PlaceResources(). But we can place the numbers in any order
    def place_numbers(self, numbers):
        copy_empty_spaces = copy.deepcopy(self.empty_spaces)
        
        while len(self.number_deque) != 0:
            # Select random empty tile
            available_hex = self.select_empty_tile(copy_empty_spaces)
            copy_empty_spaces.remove(available_hex)
            if available_hex.position != self.desert_position:
                removed_number = numbers.pop()
                removed_number.position = available_hex.position
                
                self.numbers.append(removed_number)
    
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