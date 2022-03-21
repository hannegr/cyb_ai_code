import copy
import itertools
from operator import itemgetter
import time 
import numpy as np 


class MyPlayer: 
    '''Template Docstring for MyPlayer, look at the TODOs'''
    '''
    MyPlayer will knock every other player out, due to its very simplistic nature. 
    It uses the alpha-beta algorithm, with pseudocode taken from http://aima.cs.berkeley.edu/algorithms.pdf
    (the functions on page 12, chapter 5: Adversial search and games). 
    It also considers the time limitation and the depth, and cuts off when the depth 
    reaches 6 or the time reaches 4.8 seconds (some offset to be on the safe side).
    '''
    def __init__(self, my_color,opponent_color, board_size=8):
        '''
        name (string): Username of the student 
        my_color (int): Player's color in the reversi game 
        opponent_color(int): Color of the opponent 
        board_size(int): Size of board 
        search_depth(int): The depth that when reached will cut off the search
        '''
        self.name = 'alvhehan'
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.board_size = board_size
        self.search_depth = 6
 
    def move(self,board):
        '''
        Calling the alpha-beta search algorithm (self.maximize), it will return the 
        best move my player can make calculated by it. 
        '''
        starting_time = time.time()
        moves = self.get_all_valid_moves(board, self.my_color)
        if not moves:
            return None
        if len(moves) == 1: 
            #no need to run through the algorithm then
            return moves[0]
        best_value = -5000000
        best_move = None
        for move in moves:
            alpha = -5000000
            beta = 5000000
            value = self.maximize(board, board, move, 0, alpha, beta, starting_time)
            if value > best_value:
                best_value = value
                best_move = move
        return best_move 
    
    def maximize(self, board, old_board, move, depth, alpha, beta, starting_time): 
        '''
        Implements the function MAX-VALUE from http://aima.cs.berkeley.edu/algorithms.pdf.
        Also returns an evaluation function if we either have no successors, have reached the search depth
        or are running out of time.  
        '''
        potential_board = copy.deepcopy(board)
        successors = self.get_thought_out_valid_moves(move, potential_board, self.my_color)
        if successors == None or depth >= self.search_depth or time.time()-starting_time > 4.8: 
            return self.eval(potential_board, old_board)
        v = -5000000
        for successor in successors: 
            v_temp = self.minimize(potential_board, old_board, successor, depth+1, alpha, beta, starting_time)
            if v_temp > v: 
                v = v_temp 
            alpha = max(alpha,v)
            if beta <= v:
                break 
        return v
    
    def minimize(self, board, old_board, move, depth, alpha, beta, starting_time):
        '''
        Implements the function MIN-VALUE from http://aima.cs.berkeley.edu/algorithms.pdf.
        Also returns an evaluation function if we either have no successors, have reached the search depth
        or are running out of time. 
        ''' 
        potential_board = copy.deepcopy(board)
        successors = self.get_thought_out_valid_moves(move, potential_board, self.opponent_color)
        if successors == None or depth >= self.search_depth or time.time()-starting_time > 4.8: 
            return self.eval(potential_board, old_board)
        v = 5000000
        for successor in successors: 
            v_temp = self.maximize(potential_board, old_board, successor, depth+1, alpha, beta, starting_time)
            if v_temp < v: 
                v = v_temp 
            beta = min(beta,v)
            if v <= alpha:
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
        '''
        Changed the functions a bit, by adding the playing player as input, 
        so it can find only the valid moved of that player. 
        '''
        valid_moves = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if (board[x][y] == -1) and self.__is_correct_move([x, y], board, player):
                    valid_moves.append( (x, y) )

        if len(valid_moves) <= 0:
            return None
        return valid_moves
    
    def get_thought_out_valid_moves(self, move, board,  player): 
        '''
        will try to add a new move to the board, and return the valid 
        moves that can be made by the current player with the new board configuration.
        '''
        try: 
            board[move[0]][move[1]] = player
        except: 
            return self.get_all_valid_moves(board, player)
        valid_moves = self.get_all_valid_moves(board, player)
        return valid_moves  
    
    def _corners(self, board, player): 
        '''
        Will return the number of corner positions 
        achieved by the player. 
        '''
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
    
    def _edges_away_from_corners(self, board, player):
        '''
        Will return the number of edge positions the player has, 
        that is also at least two positions away from the corners.
        '''
        number_of_edges_away_from_corners = 0
        #[2:-2] because we only retrieve the positions that are at least two positions away from the corner
        first_vertical_edge = list(map(itemgetter(0), board))[2:-2]
        second_vertical_edge = list(map(itemgetter(len(board)-1), board))[2:-2]
        first_horizontal_wall = board[0][2:-2]
        second_horizontal_wall = board[-1][2:-2]
        edges = [first_vertical_edge, second_vertical_edge, first_horizontal_wall, second_horizontal_wall]
        for row_or_column in edges: 
            for color in row_or_column:
                if color == player: 
                    number_of_edges_away_from_corners += 1
        return number_of_edges_away_from_corners
    
    def _diagonal_away_from_corners(self, board, old_board, player):
        '''
        Returns the number of positions the player has that are one diagonal away 
        from the corners. As can be seen, these numbers will only be added if the 
        player has not achieved the position of the corner the diagonal is next to. 
        See the function self.eval for why. 
        ''' 
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
    
    def _edges_close_to_corners(self, board, old_board, player): 
        '''
        Returns the number of positions the player has that are one position away 
        from the corners. As can be seen, these numbers will only be added if the 
        player has not achieved the position of the corner the positions are next to. 
        See the function self.eval for why. 
        ''' 
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
        
        
    
    def _insides(self, board, player):
        '''
        Returns the number of positions of the player that are within
        two positions of the walls of the board. 
        '''
        number_of_insides = 0
        for row in itertools.islice(board, 2, len(board)-2): 
            for color in itertools.islice(row , 2, len(row)-2):
                if color == player: 
                    number_of_insides += 1
        return number_of_insides  
    
    def _discs_on_board(self,board, player): 
        '''
        Checks how many discs the player has on the board.
        '''
        number_of_discs = 0
        for row in board: 
            number_of_discs += row.count(player)
        return number_of_discs
    
    def _utility(self, board): 
        '''
        Checks which one of the players has the most discs. If it is my player, it will return a
        positive utility. If it a draw, it will return 0. If it is the other player, it will return a 
        negative utility. 
        '''
        if(self._discs_on_board(board, self.my_color) < self._discs_on_board(board, self.opponent_color)): 
            return -1000 
        if(self._discs_on_board(board, self.my_color) == self._discs_on_board(board, self.opponent_color)): 
            return 0
        return 1000 
    
    def _threshold(self, board): 
        '''
        Sees how much space is left on the table, and compares it with a threshold found experimentally. 
        Returns True if the threshold is bigger than the available disc space
        '''
        available_disc_space = self.board_size*self.board_size - (self._discs_on_board(board, self.my_color)+self._discs_on_board(board, self.opponent_color))
        if self.board_size > available_disc_space: 
            return True
        return False
    
    def eval(self,board, old_board): 
        '''
        Some parts of the evaluation function are based on this page: https://www.ultraboardgames.com/othello/tips.php, 
        some are just based on experimenting. 
        In the evaluation function my player thinks like this: 
        - He really loves corners, because they are stable 
        - He really hates being one diagonal away from a corner, because then someone else can get his corner! 
        - He really hates being one position vertically or horizontally away from a corner, because then there 
          is also a chance that someone can take his corner 
        - If he already has possession of the corner, he does not care about the two previous situations for the
          positions near that corner. 
        - He loves being close to the edges, as long as it is not next to a corner he does not possess 
        - He likes being more than two positions within the board, because that makes him feel safe. 
        - He does not really care that much about how many pieces he has on the board, before 
          he is near the end of the game
        Based on these I have tried to give different values to the different situation, and this is 
        the end result.        
        '''
        corners_value = 120*self._corners(board, self.my_color) 
        edges_away_from_corners_value = 30*self._edges_away_from_corners(board, self.my_color) 
        edges_close_to_corners_value = -80*self._edges_close_to_corners(board, old_board, self.my_color)
        diagonal_away_from_corners_value = -110*self._diagonal_away_from_corners(board, old_board, self.my_color) 
        insides_value = 20*self._insides(board, self.my_color)
        util = 0 
        if(self._threshold):
            util = self._utility(board)
        total_value = corners_value + edges_away_from_corners_value + diagonal_away_from_corners_value + insides_value + edges_close_to_corners_value + util
        return total_value