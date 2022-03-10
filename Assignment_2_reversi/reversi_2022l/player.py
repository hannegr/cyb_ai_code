import numpy as np
from game_board import GameBoard

class MyPlayer():
    '''My player is the best player and will win any tournament! Just wait!!!''' # TODO a short description of your player

    def __init__(self, my_color,opponent_color, board_size=8):
        self.name = 'alvhehan'
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.board_size = board_size
        
        self.search_depth = 8 
        self.alpha = -1000
        self.beta = 1000
        self.board_copy = None
        

    def move(self,board):
        # TODO: write you method
        # you can implement auxiliary functions, of course
        #if(board.get_all_valid_moves(self.my_color) == None):
        if(self.get_all_valid_moves(board) == None): 
            return None 
        self.board_copy = board.get_board_copy()
        #search_tree = SearchTree()
        #value = search_tree.max_value(board)
        #return value
        return self.get_all_valid_moves(board)[0]
        

    def __is_correct_move(self, move, board):
        dx = [-1, -1, -1, 0, 1, 1, 1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]
        for i in range(len(dx)):
            if self.__confirm_direction(move, dx[i], dy[i], board)[0]:
                return True, 
        return False

    def __confirm_direction(self, move, dx, dy, board):
        posx = move[0]+dx
        posy = move[1]+dy
        opp_stones_inverted = 0
        if (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
            if board[posx][posy] == self.opponent_color:
                opp_stones_inverted += 1
                while (posx >= 0) and (posx <= (self.board_size-1)) and (posy >= 0) and (posy <= (self.board_size-1)):
                    posx += dx
                    posy += dy
                    if (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
                        if board[posx][posy] == -1:
                            return False, 0
                        if board[posx][posy] == self.my_color:
                            return True, opp_stones_inverted
                    opp_stones_inverted += 1

        return False, 0

    def get_all_valid_moves(self, board):
        valid_moves = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if (board[x][y] == -1) and self.__is_correct_move([x, y], board):
                    valid_moves.append( (x, y) )

        if len(valid_moves) <= 0:
            print('No possible move!')
            return None
        return valid_moves
    
    def get_thought_out_valid_moves(self, state, player_color): 
        self.board_copy[state[0]][state[1]] = player_color
        valid_moves = self.get_all_valid_moves(self.board_copy)
        return valid_moves 
        
        
        
        
    
    def eval(self,board,state): 
        '''
        print -eval to get the evaluation of the opposing player. 
        '''
        board_size = board.board_size -1
        row_modulo = state[0]%board_size
        column_modulo = state[1]%board_size
        
        #if the state is in a corner: 
        if(row_modulo == 0 and column_modulo == 0):
            return 50
        #if player puts the disc at least 2 spaces away from both the horizontal wall and the vertical wall: 
        if(row_modulo < (board_size -1) and column_modulo > 1): 
            if(column_modulo < (board_size -1) and row_modulo > 1):
                return 10
        #if the state is one diagonal away from a corner: 
        if(row_modulo == 1 or row_modulo == board_size-1): 
            if(column_modulo == 1 or column_modulo == board_size-1): 
                return -50
        #if the state is one point in the vertical or horizontal space away from the corner: 
        if(row_modulo == 0 and (column_modulo == 1 or column_modulo == (board_size -1))): 
            return -25 
        if(column_modulo == 0 and (row_modulo == 1 or row_modulo == (board_size -1))): 
            return -25 
        return -10
    
    def full_score(): 
        '''
        See what the full score of the evaluation is
        '''
        return None 
    
    def max_value(self, state, depth):
        v = 1000000 
        successors = self.get_thought_out_valid_moves(self, state, self.my_color)
        move = (-1,-1)
        for successor in successors: 
            v = self.min_value(successor)
            move = successor
            if v >= self.beta: 
                return v, move
            self.alpha = max(self.alpha, v)
        return v, move
    
    def min_value(self, state, depth): 
        v = -1000000 
        successors = self.get_thought_out_valid_moves(self, state, self.opponent_color)
        move = (-1,-1)
        for successor in successors: 
            v = self.max_value(successor)
            if v <= self.alpha: 
                return v, move
            self.beta = min(self.beta, v)
        return v, move
        

"""class SearchTree(): 
    def __init__(self): 
        #self.player_utilities = np.array([50, 10, 2, -25, -50])
        #self.opponent_utilities = -self.player_utilities
    
            
class Node(): 
    def __init__(self, parent, depth, state):
        self.parent = parent 
        self.depth = depth 
        self.cost = None 
        self.state = state
"""           
if __name__ == "__main__": 
    board = GameBoard()
    board.print_board()
    agent = MyPlayer(0,1)
    print(agent.move(board))
    state = (2,2)
    
            
    
