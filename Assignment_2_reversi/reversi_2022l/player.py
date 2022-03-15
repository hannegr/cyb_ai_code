from unittest import expectedFailure
import numpy as np
from game_board import GameBoard
import copy
import itertools
from operator import itemgetter
import time 
import math

class MyPlayer():
    '''My player is the best player and will win any tournament! Just wait!!!''' # TODO a short description of your player

    def __init__(self, my_color,opponent_color, board_size=8):
        self.name = 'alvhehan'
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.board_size = board_size
        
        self.search_depth = 6
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
        _, move = self.max_value(board, 0)
        return move
        #return self.get_all_valid_moves(board)[0]
        

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
    
    def eval(self,board,state): 
        '''
        -eval to get the evaluation of the opposing player. 
        '''
        board_size = self.board_size -1
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
        #print("depth: ", depth)
        v = -1000000 
        if depth == 0: 
            successors = self.get_all_valid_moves(self.board_copy)
        else: 
            successors = self.get_thought_out_valid_moves(state, self.opponent_color)
        move = (-1,-1)
        depth = depth + 1 
        if successors == None: 
            return 0, state
        for successor in successors: 
            v = max(v, self.min_value(successor, depth)[0])
            move = successor
            if v >= self.beta: 
                return v, move
            self.alpha = max(self.alpha, v)
        #print("alpha: ", self.alpha)
        #print("v: ", v)
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
        #print("beta: ", self.beta)
        #print("v: ", v)
        return v, move
    
    def is_cutoff(self, depth): 
        if (depth >= 6): 
            return True 
        return False
    def is_terminal(self): 
        if(self.get_all_valid_moves(self.board_copy)):
            return None 
        return None
    
    
  
class RandomPlayer():
    '''My player is the best player and will win any tournament! Just wait!!!''' # TODO a short description of your player

    def __init__(self, my_color,opponent_color, board_size=8):
        self.name = 'alvhehan'
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.board_size = board_size
        
        self.search_depth = 6
        self.alpha = -1000
        self.beta = 1000
        self.board_copy = None
        

    def move(self,board):
        valid_moves = self.get_all_valid_moves(board)
        idx = np.random.choice(len(valid_moves))
        return valid_moves[idx]
        

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

class BestPlayer():
    #TODO se gjennom move om alt er rett, finn ut hvorfor spilleren alltid tar det siste movet i lista valid_moves. 
    #Dette er feil lol. 
    '''My player is the best player and will win any tournament! Just wait!!!''' # TODO a short description of your player

    def __init__(self, my_color,opponent_color, board_size=8):
        self.name = 'alvhehan'
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.board_size = board_size
        
        self.search_depth = 5
        self.alpha = -1000
        self.beta = 1000        

    def move(self,board): 
        valid_moves = self.get_all_valid_moves(board, self.my_color)
        if(valid_moves == None): 
            return None 
        if(len(valid_moves) == 1): 
            return valid_moves[0]
        self.alpha = -100000
        self.beta = 100000 
        
        best_move = None
        best_val = -50000
        for move in valid_moves: 
            if move == (0,0) or move ==(self.board_size-1, self.board_size-1) or move == (0, self.board_size-1) or move == (self.board_size-1, 0): 
                return move
            alpha_beta_board = copy.deepcopy(board)
            val = self.minimax_with_pruning(alpha_beta_board, alpha_beta_board, board, 0, True)
            if val > best_val: 
                best_val = val 
                best_move = move
        return best_move        

    def __is_correct_move(self, move, board, player):
        dx = [-1, -1, -1, 0, 1, 1, 1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]
        for i in range(len(dx)):
            if self.__confirm_direction(move, dx[i], dy[i], board, player)[0]:
                return True, 
        return False
    
    def __confirm_direction(self, move, dx, dy, board, player):
        posx = move[0]+dx
        posy = move[1]+dy
        opp_stones_inverted = 0
        if (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
            if board[posx][posy] != player and board[posx][posy] != -1:
                opp_stones_inverted += 1
                while (posx >= 0) and (posx <= (self.board_size-1)) and (posy >= 0) and (posy <= (self.board_size-1)):
                    posx += dx
                    posy += dy
                    if (posx >= 0) and (posx < self.board_size) and (posy >= 0) and (posy < self.board_size):
                        if board[posx][posy] == -1:
                            return False, 0
                        if board[posx][posy] == player:
                            return True, opp_stones_inverted
                    opp_stones_inverted += 1

        return False, 0
    
    def get_all_valid_moves(self, board, player):
        valid_moves = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if (board[x][y] == -1) and self.__is_correct_move([x, y], board, player):
                    valid_moves.append( (x, y) )

        if len(valid_moves) <= 0:
            #print('No possible move!')
            return None
        return valid_moves
    
    def get_thought_out_valid_moves(self, state, board,  player_color): 
        try: 
            self.board_copy[state[0]][state[1]] = player_color
        except: 
            return self.get_all_valid_moves(board, player_color)
        valid_moves = self.get_all_valid_moves(board, player_color)
        return valid_moves  
    
    def utility(self, board): 
        my_discs = 0
        opponents_discs = 0
        for row in board: 
            my_discs += row.count(self.my_color)
            opponents_discs += row.count(self.opponent_color)
        if my_discs > opponents_discs: 
            return 500
        elif my_discs < opponents_discs: 
            return -500
        return 0             
    
    
    def minimax_with_pruning(self, state, board, old_board, depth, maximize): 
        if maximize:
            successors = self.get_thought_out_valid_moves(state, board, self.opponent_color)
        else: 
            successors = self.get_thought_out_valid_moves(state, board, self.my_color)
            
        if state == None and successors == None: 
            return self.utility(board)
        if successors == None or depth >= self.search_depth: 
            return self.eval(board, old_board)
        depth = depth + 1 
        
        if maximize: 
            v = -1000000 
            for successor in successors: 
                v = max(v, self.minimax_with_pruning(successor, board, old_board, depth+1, False))
                if v >= self.beta: 
                    return v
                self.alpha = max(self.alpha, v)
            return v
        else: 
            v = 1000000 
            for successor in successors: 
                v = min(v, self.minimax_with_pruning(successor, board, old_board, depth+1, True))
                if v <= self.alpha: 
                    return v
                self.beta = min(self.beta, v)
            return v
        
                
    """
        
    def max_value(self, state, board,  depth):
        if depth == 0: 
            successors = self.get_all_valid_moves(board, self.opponent_color)
        else: 
            successors = self.get_thought_out_valid_moves(state, board, self.opponent_color)
        if state == None and successors == None: 
            return self.utility(board)
        if successors == None or depth >= self.search_depth: 
            return self.eval(board)
        depth = depth + 1 
        v = -1000000 
        for successor in successors: 
            v = max(v, self.min_value(successor, board, depth))
            if v >= self.beta: 
                return v
            self.alpha = max(self.alpha, v)
        return v
    
    def min_value(self, state, board, depth):
        successors = self.get_thought_out_valid_moves(state, board, self.my_color)
        if state == None and successors == None: 
            return self.utility(board)
        if successors == None or depth >= self.search_depth: 
            return self.eval(board)
        depth = depth + 1 
        v = 1000000 
        for successor in successors: 
            v = min(v, self.max_value(successor, board, depth))
            if v <= self.alpha: 
                return v
            self.beta = min(self.beta, v)
        return v
    """

    def is_cutoff(self, depth): 
        if (depth >= self.search_depth): 
            return True 
        return False   
    
    def corners(self, board, player): 
        number_of_corners = 0
        if board[0][0] == player: 
            number_of_corners += 1 
        if board[0][-1] == player: 
            number_of_corners += 1 
        if board[-1][0] == player: 
            number_of_corners += 1 
        if board[-1][-1] == player: 
            number_of_corners += 1 
        return number_of_corners 
    
    def edges_away_from_corners(self, board, player):
        number_of_edges_away_from_corners = 0
        first_vertical_edge = list( map(itemgetter(0), board))[1:-1]
        last_vertical_edge = list(map(itemgetter(len(board)-1), board))[1:-1]
        first_horizontal_edge = board[0][1:-1]
        last_horizontal_edge = board[-1][1:-1]
        edges = [first_vertical_edge, last_vertical_edge, first_horizontal_edge, last_horizontal_edge]
        for row_or_column in edges: 
            for color in row_or_column:
                if color == player: 
                    number_of_edges_away_from_corners += 1
        return number_of_edges_away_from_corners
    
    def diagonal_away_from_corners(self, board, old_board, player): 
        number_of_diagonals_away_from_corners = 0
        if old_board[0][0] != player:
            if board[1][1] == player: 
                number_of_diagonals_away_from_corners += 1
        if old_board[0][-1] != player: 
            if board[1][-2] == player: 
                number_of_diagonals_away_from_corners += 1
        if old_board[-1][0] != player: 
            if board[-2][1] == player: 
                number_of_diagonals_away_from_corners += 1
        if old_board[-1][-1] != player: 
            if board[-2][-2] == player: 
                number_of_diagonals_away_from_corners += 1
        return number_of_diagonals_away_from_corners
    
    def edges_close_to_corners(self, board, old_board, player): 
        number_of_edges_close_to_corner = 0 
        if old_board[0][0] != player:                     
            if board[0][1] == player: 
                number_of_edges_close_to_corner += 1
            if board[1][0] == player: 
                number_of_edges_close_to_corner += 1
        if old_board[0][-1] != player:     
            if board[0][-2] == player: 
                number_of_edges_close_to_corner += 1
            if board[1][-1] == player: 
                number_of_edges_close_to_corner += 1
        if old_board[-1][0] != player: 
            if board[-2][0] == player: 
                number_of_edges_close_to_corner += 1  
            if board[-1][1] == player: 
                number_of_edges_close_to_corner += 1
        if old_board[-1][-1] != player:
            if board[-2][-1] == player: 
                number_of_edges_close_to_corner += 1
            if board[-1][-2] == player: 
                number_of_edges_close_to_corner += 1
        return number_of_edges_close_to_corner
        
        
    
    def insides(self, board, player):
        number_of_insides = 0
        for row in itertools.islice(board, 2, len(board)-2): 
            for color in itertools.islice(row , 2, len(row)-2):
                if color == player: 
                    number_of_insides += 1
        return number_of_insides 
    
    def changes_in_board(self, board, old_board): 
        for row in range(len(board)): 
            same_values = [h == j for h, j in zip(board[row], old_board[row])]
            for value in range(len(same_values)): 
                if same_values[value] == False: 
                    board[value] = -1
        return board
        
        
    
    def eval(self,board, old_board): 
        '''
        '''
        changed_board = self.changes_in_board(board, old_board)
        corners_value = 80*self.corners(changed_board, self.my_color) 
        edges_away_from_corners_value = 30*self.edges_away_from_corners(changed_board, self.my_color) 
        edges_close_to_corners_value = -80*self.edges_close_to_corners(changed_board, old_board, self.my_color)
        diagonal_away_from_corners_value = -100*self.diagonal_away_from_corners(changed_board, old_board, self.my_color) 
        insides_value = 20*self.insides(changed_board, self.my_color)
        total_value = corners_value + edges_away_from_corners_value + diagonal_away_from_corners_value + insides_value + edges_close_to_corners_value
        return total_value
        

