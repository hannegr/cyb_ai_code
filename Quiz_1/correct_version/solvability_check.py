import npuzzle

def puzzle_list(env): 
    '''
    Returns the puzzle_list for a 1, 2, 3 or 4 puzzle
    '''
    numbers_list = []
    for i in range(4): 
        for j in range(4): 
            try: 
                numbers_list.append(env.read_tile(i,j))
            except: print ("out of range")
    return numbers_list
def four_or_three_puzzle(env):
    '''
    Returns the number corresponding to the npuzzle 
    ''' 
    numbers_list = puzzle_list(env)
    if(15 in numbers_list): 
        return 4 
    return 3

def puzzle_splitted_list(env): 
    '''
    Returns a splitted list with the npuzzle
    '''
    numbers_list = puzzle_list(env) 
    npuzzle_number = four_or_three_puzzle(env)
    splitted_list = [numbers_list[i:i+npuzzle_number]for i in range(0, len(numbers_list),npuzzle_number)]
    return splitted_list

def odd_inversions(env): 
        '''
        return true if inversions are odd, false if they are not odd. 
        '''
        
        inversions = 0
        in_front_of_current_row = False 
        numbers_list = puzzle_list(env)
        splitted_list = puzzle_splitted_list(env)
        for i in numbers_list: 
            in_front_of_current_row = False 
            for j in splitted_list: 
                if (i in j) and (splitted_list[-1] == j): 
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
    


def odd_tile_placement(env): 
        """
        Returns True if tile placement is odd. Returns False if tile placement is even. 
        """
        splitted_list = puzzle_splitted_list(env)
        for sub_split_list in range (len(splitted_list)): 
            if None in splitted_list[sub_split_list]: 
                if(len(splitted_list) - (sub_split_list))%2: 
                    return True 
                
        return False  
    
    

def is_solvable(env): 
    '''
    Returns whether the solution is solvable or not 
    '''
    if(four_or_three_puzzle(env) == 3): 
        if(odd_inversions(env)): 
            return True
    else: 
            if((not odd_inversions(env) and not odd_tile_placement(env)) or (odd_inversions(env) and odd_tile_placement(env))): 
                return True
    return False          

if __name__=="__main__": # testing suite
    env = npuzzle.NPuzzle(4) # instance of NPuzzle class
    env.reset()              # random shuffle
    env.visualise()          # just to show the board
    # just check
    print(is_solvable(env))  # should output True or False
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    