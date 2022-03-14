import numpy as np
from game_board import GameBoard
import copy
"""

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
        valid_moves = self.get_all_valid_moves(board)
        if(valid_moves == None): 
            return None 
        if(len(valid_moves) == 1): 
            return valid_moves[0]
        self.board_copy = copy.deepcopy(board)
        _, move = self.max_value(None, board, 0)
        return move
        

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
            #print('No possible move!')
            return None
        return valid_moves
    
    def get_thought_out_valid_moves(self, state, player_color): 
        self.board_copy[state[0]][state[1]] = player_color
        #print("state: ", state)
        valid_moves = self.get_all_valid_moves(self.board_copy)
        #print("valid moves: ", valid_moves)
        return valid_moves  
    
    def utility(self, board): 
        return 1000
    
    def eval(self,board,state): 
        '''
        -eval to get the evaluation of the opposing player. 
        '''
        board_size = board.board_size -1
        row_modulo = state[0]%board_size
        column_modulo = state[1]%board_size
        
        #if the state is in a corner: 
        if(row_modulo == 0 and column_modulo == 0):
            return 50
        #if player puts the disc at least 2 spaces away from both the horizontal and vertical wall: 
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
    
    def max_value(self, state, depth):
        v = -1000000
        if depth == 0: 
            successors = self.get_all_valid_moves(self.board_copy)
        else: 
            successors = self.get_thought_out_valid_moves(state, self.opponent_color)
        if(state == None) and (successors == None): 
            return self.utility(self.board_copy), state
        if(self.is_cutoff): 
            return self.eval(state), state
        move = (-1,-1)
        depth = depth + 1  
        if successors == None: 
            return 0, state
        for successor in successors: 
            v = self.min_value(successor, depth)[0]
            move = successor
            if v >= self.beta: 
                return v, move
            self.alpha = max(self.alpha, v)
        
        return v, move
    
    def min_value(self, state, depth): 
        print("depth:", depth)
        v = 1000000 
        successors = self.get_thought_out_valid_moves(state, self.opponent_color)
        move = (-1,-1)
        depth = depth + 1 
        if successors == None: 
            return 0, state
        for successor in successors: 
            v = self.max_value(successor, depth)[0]
            if v <= self.alpha: 
                return v, move
            self.beta = min(self.beta, v)
        print("beta: ", self.beta)
        print("v: ", v)
        return v, move
    
    def is_cutoff(self, depth): 
        if (depth >= 6): 
            return True 
        return False
    def is_terminal(self): 
        if(self.get_all_valid_moves(self.board_copy)):
            return None 
        return None
    """
    
    
    
    

        

