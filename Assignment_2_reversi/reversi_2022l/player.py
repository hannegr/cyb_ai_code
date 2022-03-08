import numpy as np
from game_board import GameBoard

class MyPlayer():
    '''My player is the best player and will win any tournament! Just wait!!!''' # TODO a short description of your player

    def __init__(self, my_color,opponent_color, board_size=8):
        self.name = 'alvhehan'
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.board_size = board_size
        

    def move(self,board):
        # TODO: write you method
        # you can implement auxiliary fucntions, of course
        if(self.get_all_valid_moves == None): 
            return None 
        
        return (2, 1)

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
    
    class SearchTree(): 
        def __init__(self): 
            self.player_utilities = np.array([50, 10, 5, 2, -1, -25, -50])
            self.opponent_utilities = -self.player_utilities
            self.search_depth = 8 #for alpha/beta algorithm 
            self.alpha = -1000
            self.beta = 1000
        

            
    class Node(): 
        def __init__(self, parent, depth):
            self.parent = parent 
            self.depth = depth 
            self.cost = None 
            
if __name__ == "__main__": 
    board = GameBoard()
    board.print_board()
    
    agent = MyPlayer(0,1)
    #print(agent.move(board))
    print(agent.get_all_valid_moves(board))
    #moves = agent.get_all_valid_moves(board)
        
            
    
