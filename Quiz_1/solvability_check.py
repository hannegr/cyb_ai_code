
import npuzzle
 
def is_solvable(env):
    '''
    True or False?
    '''
    if(env.size%2): 
        if(env.odd_inversions()): 
            return False
    else: 
            if((not env.odd_inversions() and not env.odd_tile_placement()) or (env.odd_inversions() and env.odd_tile_placement())): 
                return False
    return True
 
if __name__=="__main__": # testing suite
    env = npuzzle.NPuzzle(4) # instance of NPuzzle class
    env.reset()              # random shuffle
    env.visualise()          # just to show the board
    # just check
    print(is_solvable(env))  # should output True or False
            