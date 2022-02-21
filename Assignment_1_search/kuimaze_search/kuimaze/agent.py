from kuimaze.baseagent import BaseAgent
import random 
import time
import kuimaze



class Agent(BaseAgent):
    '''
    Simple example of agent class that inherits kuimaze.BaseAgent class 
    '''
    def __init__(self, environment, distance_matrix=None):
        self.environment = environment

    def find_path(self):
        '''
        Method that must be implemented by you. 
        Expects to return a path_section as a list of positions [(x1, y1), (x2, y2), ... ].
        '''
        observation = self.environment.reset() # must be called first, it is necessary for maze initialization
        goal = observation[1][0:2]
        position = observation[0][0:2]                               # initial state (x, y)
        print("Starting random searching")
        while True:
            new_positions = self.environment.expand(position)         # [[(x1, y1), cost], [(x2, y2), cost], ... ]
            # print(new_positions)
            position = random.choice(new_positions)[0]                # select next at random, ignore the cost infor
            print(position)
            if position == goal:                    # break the loop when the goal position is reached
                print("goal reached")
                break
            self.environment.render()               # show enviroment's GUI       DO NOT FORGET TO COMMENT THIS LINE BEFORE FINAL SUBMISSION!      
            time.sleep(0.1)                         # sleep for demonstartion     DO NOT FORGET TO COMMENT THIS LINE BEFORE FINAL SUBMISSION! 

        path = [(4,0),(4,1)]        # create path as list of tuples in format: [(x1, y1), (x2, y2), ... ] 
        return path
    
    def heuristic_distance(self, position, goal, D): 
        dx = abs(position.x - goal.x)
        dy = abs(position.y - goal.y)
        return D * (dx + dy)
    
    
    def a_algorithm(self):
        observation = self.environment.reset()
        goal = observation[1][0:2]
        position = observation[0][0:2]   
        
        