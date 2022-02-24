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
    
    def _f_score(self, goal, positions): #, finished_nodes): 
        """
        Sum of heuristic score and cost 
        """
        a = None
        f_score = 0
        for position in positions: 
            pos_h_score = self._h_score(position[0], goal)
            pos_cost = position[1]
            pot_f_score = pos_h_score + pos_cost
            if(pot_f_score > f_score): 
                f_score = pot_f_score
                a =[position, f_score]
                
        return a            
            
    
    
    def a_algorithm(self):
        '''
        Implemented A* algorithm 
        '''
        observation = self.environment.reset() #returns start position and goal position
        goal = observation[1][0:2]
        q = observation[0][0:2] 
        q = [q, self._h_score(q, goal)]
        
        print("goal: ", goal) 
        print("position: ", q)
        open_set = [q]
        closed_set = []
        children_and_parents = {} 
        while open_set: 
            #finn noden med lavest f i list, kall den q 
            min_f_score_index = open_set.index(min(open_set))
            q = open_set[min_f_score_index]
            del open_set[min_f_score_index]
            q_successors = self.environment.expand(q[0])
            children_and_parents[q[0][0]] = q_successors
            best_child = self._f_score(goal, q_successors)
            print(best_child)
            #open_set.append(best_child)
            #closed_set.append(q)
            #print(open_set)
            #print(closed_set)
            
                  
            """                           
            break
            if init_position in open_set: 
                q = init_position
                q_successors = self.environment.expand(q)
                q_successors_f_score = self._f_score(goal, q_successors)
                children_and_parents[q] = q_successors
            else: 
                max_f_score_index = open_set.index(max(open_set))
                q = open_set[max_f_score_index]
                del open_set[max_f_score_index]
                q_successors = self.environment.expand(q[0])
                children_and_parents[q[0][0]] = q_successors
            """
            
        
        
        