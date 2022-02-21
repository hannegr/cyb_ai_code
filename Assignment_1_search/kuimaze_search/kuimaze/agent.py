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
    
    def _h_score(self, position, goal): 
        """
        Chooses the normal bla bla as my heuristic distance, because of how the maze looks like. 
        """
        dx = abs(position[0] - goal[0])
        dy = abs(position[1] - goal[1])
        return (dx + dy) 
    
    def _f_score(self, position, goal, positions, finished_nodes): 
        """
        Sum of heuristic score and cost 
        """
        for position_index in positions: 
            
    
    
    def a_algorithm(self):
        '''
        Implemented A* algorithm 
        '''
        observation = self.environment.reset() #returns start position and goal position
        goal = observation[1][0:2]
        position = observation[0][0:2]  
        finished_nodes = []
        current_nodes = [position]
        potential_nodes = []
        #print('Starting random searching') 
        while True: 
            positions_with_cost = self.environment.expand(position)
            #må i tillegg adde heuristic distance på en eller annen måte. 
            print(positions_with_cost)
            print(self._heuristic_distance(position, goal))
            break
            
        
        
        