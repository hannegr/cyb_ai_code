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
        self.children_and_parents = {}

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
    
    def _f_score(self, goal, positions):
        f_score_list = []
        for position in positions: 
            pos_h_score = self._h_score(position[0], goal)
            pos_cost = position[1]
            pos_f_score = pos_h_score + pos_cost
            f_score_list.append([position, pos_f_score])
        return f_score_list 
    
    
    def a_algorithm(self):
        '''
        Implemented A* algorithm 
        '''
        observation = self.environment.reset() #returns start position and goal position
        goal = observation[1][0:2] #goal position
        q = observation[0][0:2] #start position
        q = [[q], self._h_score(q, goal)]
        test = []
        
        #print("goal: ", goal) 
        #print("position: ", q)
        frontier_list = [q]
        explored_set = set()
         
        while frontier_list: 
            frontier_list.sort(reverse=True)
            
            q = frontier_list.pop() 
            if(q[0][0] in test): 
                test.remove(q[0][0])
                test.append(q[0][0])
            else: 
                test.append(q[0][0])
            explored_set.add(q[0][0])
            if(q[0][0] == goal): 
                print("done!")
                return test
            else: 
                q_successors = self.environment.expand(q[0][0])
                self.children_and_parents[q[0][0]] = q_successors
                successors_with_f_values = self._f_score(goal, q_successors)
                for successor in successors_with_f_values: 
                    if(successor[0][0] not in explored_set): 
                        frontier_list.append(successor)
                        
