from unittest import expectedFailure
import numpy as np
from game_board import GameBoard
import copy
import itertools
from operator import itemgetter
import time 
import math


class MyPlayer: 
    def __init__(self, my_color,opponent_color, board_size=8):
        self.name = 'alvhehan'
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.board_size = board_size
        self.time_start = 0
        self.search_depth = 5
 
    def move(self,board):
        self.time_start = time.time()
        states = self.get_all_valid_moves(board, self.my_color)
        if not states:
            return None
        best_val = -5000000
        best_state = None
        for state in states:
            alpha = -5000000
            beta = 5000000
            val = self.maximize(board, board, state, 0, alpha, beta)
            #val = self.minimax(board, board, state, True, 0, alpha, beta)
            if val > best_val:
                best_val = val
                best_state = state
        return best_state 
    
    def maximize(self, board, old_board, state, depth, alpha, beta): 
        potential_board = copy.deepcopy(board)
        successors = self.get_thought_out_valid_moves(state, potential_board, self.my_color)
        if successors == None or depth >= self.search_depth or time.time()-self.time_start >= 4.7: 
            return self.eval(potential_board, old_board)
        v = -5000000
        for successor in successors: 
            v_temp = self.minimize(potential_board, old_board, successor, depth+1, alpha, beta)
            if v < v_temp: 
                v = v_temp 
            alpha = max(alpha,v)
            if beta <= alpha:
                break 
        return v
    def minimize(self, board, old_board, state, depth, alpha, beta): 
        potential_board = copy.deepcopy(board)
        successors = self.get_thought_out_valid_moves(state, potential_board, self.opponent_color)
        if successors == None or depth >= self.search_depth or time.time()-self.time_start >= 4.7: 
            return self.eval(potential_board, old_board)
        v = 5000000
        for successor in successors: 
            v_temp = self.maximize(potential_board, old_board, successor, depth+1, alpha, beta)
            if v_temp < v: 
                v = v_temp 
            beta = min(beta,v)
            if alpha >= beta:
                break 
        return v
    
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
            board[state[0]][state[1]] = player_color
        except: 
            return self.get_all_valid_moves(board, player_color)
        valid_moves = self.get_all_valid_moves(board, player_color)
        return valid_moves  
    
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
    def eval(self,board, old_board): 
        '''
        '''
        #changed_board = self.changes_in_board(board, old_board)
        corners_value = 80*self.corners(board, self.my_color) 
        edges_away_from_corners_value = 30*self.edges_away_from_corners(board, self.my_color) 
        edges_close_to_corners_value = -80*self.edges_close_to_corners(board, old_board, self.my_color)
        diagonal_away_from_corners_value = -100*self.diagonal_away_from_corners(board, old_board, self.my_color) 
        insides_value = 20*self.insides(board, self.my_color)
        total_value = corners_value + edges_away_from_corners_value + diagonal_away_from_corners_value + insides_value + edges_close_to_corners_value
        return total_value
    
    
    """
    def minimax(self, board, old_board, state, me, depth, alpha, beta):
        potential_board = copy.deepcopy(board)
        if me: 
            successors = self.get_thought_out_valid_moves(state, potential_board, self.my_color)
        else: 
            successors = self.get_thought_out_valid_moves(state, potential_board, self.opponent_color)
        if successors == None or depth >= self.search_depth or time.time()-self.time_start >= 4.7: 
            return self.eval(potential_board, old_board)
        
        if me: 
            v = -5000000
            for successor in successors: 
                v_temp = self.minimax(potential_board, old_board, successor, not me, depth+1, alpha, beta)
                if v < v_temp: 
                    v = v_temp 
                alpha = max(alpha,v)
                if beta <= alpha:
                    break 
        else: 
            v = 5000000
            for successor in successors: 
                v_temp = self.minimax(potential_board, old_board, successor, me, depth+1, alpha, beta)
                if v_temp < v: 
                    v = v_temp 
                beta = min(beta,v)
                if alpha >= beta:
                    break 
        return v
                
        """