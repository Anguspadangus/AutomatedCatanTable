from objects.BoardComponents import *

import random
import copy
import json
import math
import numpy as np

class Board():
    def __init__(self, configuration):
        # The possible spaces on the catan board
        self.empty_spaces = [EmptyHex(config[0][0], config[0][2], config[0][1]) for config in configuration]
        
        # Position of the desert tile
        desert_position = self.load_desert()
        
        for i, resource in enumerate(configuration):
            if self.empty_spaces[i].position == desert_position:
                resource[1].isDesert = True
                
            self.empty_spaces[i].push(resource[1])
 
    def add_numbers(self, numbers):
        # The lazy way
        i = 0
        for number in numbers:
            if not self.empty_spaces[i].stack[0].isDesert:
                self.empty_spaces[i].reveal(number)
                i += 1
            else:
                self.empty_spaces[i+1].reveal(number)
                i += 2
                
    def add_to_board(self, to_add):
        # We can do something like this, if we really to, this way would evalaute the closest number to a hex in real world space
        # When we get everything working we can do this
        
        for obj in to_add:
            # This might get bad, but I think we're going to have to use the locations of numbers
            # Check if number is in the radius of one of the hexes
            for empty_hex in self.empty_spaces:
                distance = math.sqrt((obj.position[0] - empty_hex.position[0])**2 + (obj.position[1] - empty_hex.position[1])**2)
                if distance < empty_hex.radius:   
                    # add it to the empty_hex
                    empty_hex.reveal(obj)
                    # If there exists one already there choose closest one?
            
    # Remove numbers or hexes from an already set board randomly
    def remove_tiles(self):
        # np.random.permutation performs a shallow copy, allowing us to edit the stack inside (theordically) 
        removal_order = np.random.permutation(self.empty_spaces).tolist()
        # TODO CHECK THIS
        if (isinstance(self.empty_spaces[0].stack[-1], Number) or isinstance(self.empty_spaces[1].stack[-1], Number)):
            for hex in removal_order:
                if hex.stack[0].isDesert:
                    removal_order.remove(hex)
                    break
            
        return removal_order
    
    # Updates the neighbors of a hex given the possible emptyHexes and the placed Hex
    def update_neighbors(self, hex, empty_hexes):
        for empty_hex in empty_hexes:
            if hex.name in empty_hex.neighbors:
                empty_hex.neighbor_count += 1

## START HERE##
    # we do not want to push it here, instead this acts as "in what order do I place the resources in?"
    def place_resources(self, resources):
        place_order = []
        # assuming its completely empty
        # Want to make a deepcopy so we can reuse the empty hexes
        copy_empty_spaces = copy.copy(self.empty_spaces)
            
        while len(resources) != 0:
            # Select random empty tile
            available_hex = self.select_empty_tile_with_neighbors(copy_empty_spaces)
            copy_empty_spaces.remove(available_hex)
            
            # Select top of deque
            removed_resource = resources.pop()
            self.update_neighbors(removed_resource, copy_empty_spaces)
            
            # Check if the resource removed was the desert Hex, the update the new position
            if (removed_resource.isDesert):
                desert_position = available_hex.position
                self.save_desert(desert_position)
            
            place_order.append(copy_empty_spaces)
    
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
    
    def load_desert(self):
        f = open('src\Algorithms\desertPosition.json')
        data = json.load(f)
        f.close()
        return tuple(data["pos"])

    def save_desert(self, desert_position):
        with open('src\Algorithms\desertPosition.json', 'w') as f:
            json.dump({"pos" : desert_position}, f)         