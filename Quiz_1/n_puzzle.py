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
        self.puzzle_list = [i for i in range (1,size)]
        self.puzzle_list.append(None)
        self.splitted_list = []
        
 
    def reset(self):
        '''
        initialize the board by a random shuffle of symbols
        :return: None

        I assume that we are to randomly shuffle, but at the same time make a solvable puzzle here.
        draw solvable 4-1 puzzles. Solvable if: 
        - The unnumbered tile is on an even row and the number of inversions is odd 
        - The unnumbered tile is on an odd row and the number of inversions is even  
        
        Draw solvable 3-1 puzzles. Solvable if: 
        - the number of inversions is even in the input state.
        (got this from https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/)
        '''
        self.splitted_list = []
        random.shuffle(self.puzzle_list) 
        print(self.odd_inversions())
       
            
    
            
    def odd_inversions(self): 
        '''
        return true if inversions are odd, false if they are not odd. 
        '''
        #Funker ikke I fucked up oof 
        
        inversions = 0
        row = 0
        modulo = int(np.sqrt(self.size))
        for i in range(self.size): 
            print(inversions)
            if(i%modulo == 0):
                row += 1
            for j in range(i+1, len(self.puzzle_list)): 
                if(i < j): 
                    inversions += 1 
                    
        print(inversions%2)
        if(inversions%2 != 0): 
            return True 
        return False 
                
        
    def visualise(self):
        '''
        just print itself to the standard output
        :return: None
        '''
        split_size = int(np.sqrt(self.size))
        splitted_list = self.puzzle_list.copy()
        self.splitted_list = [splitted_list[i:i + split_size] for i in range(0, len(splitted_list), split_size)]
        
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

