import numpy as np
import random
import  copy

class NPuzzle:
    '''
    sliding puzzle class of a general size
    https://en.wikipedia.org/wiki/15_puzzle
    
    
    '''
    def __init__(self, size):
        '''
        create the list of symbols, typically from 1 to 8 or 15. Empty tile
        is represented by None
        :param size: the board will be size x size,
                     size=3 - 8-puzzle; 4 - 15 puzzle
        '''
        self.size = size 
        self.puzzle_list = [i for i in range (1,size**2)]
        self.puzzle_list.append(None)
        self.splitted_list = []
        
 
    def reset(self):
        '''
        initialize the board by a random shuffle of symbols
        :return: None

        I assume that we are to randomly shuffle, but at the same time make a solvable puzzle here.
        draw solvable even puzzles. Solvable if: 
        - The unnumbered tile is on an even row and the number of inversions is odd 
        - The unnumbered tile is on an odd row and the number of inversions is even  
        
        Draw solvable odd puzzles. Solvable if: 
        - the number of inversions is even in the input state.
        (got these rules from https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/)
        '''
        self.splitted_list = []
        random.shuffle(self.puzzle_list) 
        while(not self.is_solvable()): 
            random.shuffle(self.puzzle_list)
        
    def is_solvable(self): 
        if(self.size%2): 
            if(self.odd_inversions()): 
                return False
        else: 
            if((not self.odd_inversions() and not self.odd_tile_placement()) or (self.odd_inversions() and self.odd_tile_placement())): 
                return False
        return True
               
    def odd_tile_placement(self): 
        """
        Returns True if tile placement is odd. Returns False if tile placement is even. 
        """
        for sub_split_list in range (len(self.splitted_list)): 
            if None in self.splitted_list[sub_split_list]: 
                if(len(self.splitted_list) - (sub_split_list))%2: 
                    return True 
                
        return False     
    def odd_inversions(self): 
        '''
        return true if inversions are odd, false if they are not odd. 
        '''
        
        splitted_list = self.puzzle_list.copy()
        self.splitted_list = [splitted_list[i:i + self.size] for i in range(0, len(splitted_list), self.size)]
        inversions = 0
        in_front_of_current_row = False 
        for i in self.puzzle_list: 
            in_front_of_current_row = False 
            for j in self.splitted_list: 
                if (i in j) and (self.splitted_list[-1] == j): 
                    break 
                if in_front_of_current_row: 
                    for k in j: 
                        if i != None and k != None and i < k: 
                            inversions += 1
                if i in j: 
                    in_front_of_current_row = True
        if inversions%2:
            return True 
        return False
                
        
    def visualise(self):
        '''
        just print itself to the standard output
        :return: None
        '''
        for i in range(len(self.splitted_list)): 
            print(self.splitted_list[i])        
 
    def read_tile(self, row, col):
        '''
        returns a symbol on row, col position
        :param row: index of the row
        :param column: index of the column
        :return: value of the tile - int 1 to size^2-1, None for empty tile
        The function raises IndexError exception if outside the board
        '''
        try:
            return(self.splitted_list[row][col])
            
        except IndexError as e:
            return(e)

