from catan_objects.BoardComponents import *

import random
import copy
import math
import numpy as np

class CatanBoard():
    def __init__(self, configuration):
        # The possible spaces on the catan board
        self.empty_spaces = [EmptyHex(config[0][0], config[0][2], config[0][1], config[0][3]) for config in configuration]
        
        for i, resource in enumerate(configuration):
            self.empty_spaces[i].push(resource[1])
 
    def add_to_board_lazy(self, to_add):
        # The lazy way but safe
        i = 0
        for obj in to_add:
            if not self.empty_spaces[i].stack[0].is_desert:
                self.empty_spaces[i].reveal(obj)
                i += 1
            else:
                self.empty_spaces[i+1].reveal(obj)
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
                    break
            
    # Remove numbers or hexes from an already set board randomly
    def remove_tiles(self):
        # np.random.permutation performs a shallow copy, allowing us to edit the stack inside (theordically) 
        removal_order = np.random.permutation(self.empty_spaces).tolist()
        # TODO CHECK THIS
        if (isinstance(self.empty_spaces[0].stack[-1], Number) or isinstance(self.empty_spaces[1].stack[-1], Number)):
            for hexagon in removal_order:
                if hexagon.stack[0].is_desert:
                    removal_order.remove(hexagon)
                    break
            
        return removal_order
    
    # Updates the neighbors of a hex given the possible emptyHexes and the placed Hex
    def update_neighbors(self, hexagon, empty_hexes):
        for empty_hex in empty_hexes:
            if hexagon.name in empty_hex.neighbors:
                empty_hex.neighbor_count += 1
    
    # Returns a place order for the hexes, will update the desert position when it is placed.
    def place_resources(self):
        place_order = []
        copy_empty_spaces = copy.copy(self.empty_spaces)
        while len(copy_empty_spaces) != 0:
            available_hex = self.select_empty_tile_with_neighbors(copy_empty_spaces)
            copy_empty_spaces.remove(available_hex)
            self.update_neighbors(available_hex, copy_empty_spaces)
            
            place_order.append(available_hex)
            
        return place_order
            
    def place_numbers(self):
        place_order = []
        # This should be a clean shallow copy (ref)
        copy_empty_spaces = [space for space in self.empty_spaces if not space.stack[0].is_desert]
        
        while len(copy_empty_spaces) != 0:
            available_hex = self.select_empty_tile(copy_empty_spaces)
            copy_empty_spaces.remove(available_hex)
            
            place_order.append(available_hex)
            
        return place_order
            
    def select_empty_tile(self, empty_spaces):
        random_available_hex = random.choice(empty_spaces)
        return random_available_hex
    
    # Algorithym for choosing where to place a tile
    def select_empty_tile_with_neighbors(self, empty_spaces):
        empty_available_hexes = list(filter(lambda space : space.neighbor_count >= 3, empty_spaces))
        random_available_hex = random.choice(empty_available_hexes)
        return random_available_hex
    
    def get_robber(self):
        tiles = []
        for tile in self.empty_spaces:
            if isinstance(tile.stack[-1], Robber):
                tiles.append(tile)
                
        return tiles
    
    def get_desert_hex(self):
        for tile in self.empty_spaces:
            if tile.stack[-1].is_desert:
                return tile     