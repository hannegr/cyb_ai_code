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
    
    def _f_score(self, goal, positions):
        f_score_list = []
        for position in positions: 
            pos_h_score = self._h_score(position[0], goal)
            pos_cost = position[1]
            pos_f_score = pos_h_score + pos_cost
            f_score_list.append([position, pos_f_score])
        return f_score_list 
    
            
    def _smallest_f_value(self, frontier_list, successor_place): 
        same_place_successors = [successor_place]
        for successor in frontier_list: 
            if successor_place[0][0] in successor: 
                same_place_successors.append(successor)
        if min(same_place_successors) != successor_place: 
            return False
        return True
            
        
    
    
    def a_algorithm(self):
        '''
        Implemented A* algorithm. Contains 
        - frontier_list: list showing the neighbournodes that may be expanded if the cost is minimal. 
        - closed_set: a set s.t the values are not repeated. Includes every node that is finished. 
        - predecessor_dictionary: a dictionary containing predecessor of nodes, used for returning the shortest path. 
          Chose to do this, due to what was written on the wikipedia-page of the A* algorithm about it returning the 
          shortest path, but not the way to get there. 
        
        Returns: list of the shortest path from start node to goal node. 
        '''
        observation = self.environment.reset() #returns start position and goal position
        goal = observation[1][0:2] #goal position
        start_pos = observation[0][0:2] #start position
        q = [[start_pos], self._h_score(start_pos, goal)]
        predecessor_dictionary = {}    
        path_list = []    
        #print("goal: ", goal) 
        #print("position: ", q)
        frontier_list = [q]
        explored_set = set()
         
        while frontier_list: 
            frontier_list.sort(reverse=True)
            q = frontier_list.pop() 
            explored_set.add(q[0][0])
            if(q[0][0] == goal): 
                print("done!")
                path_node = start_pos
                while goal not in path_list: 
                    path_list.append(path_node)
                    path_node = predecessor_dictionary.get(path_node)
                return path_list
            else: 
                q_successors = self.environment.expand(q[0][0])
                
                successors_with_f_values = self._f_score(goal, q_successors)
                for successor in successors_with_f_values: 
                    if(successor[0][0] not in explored_set and self._smallest_f_value(frontier_list, successor)): 
                        frontier_list.append(successor)
                        predecessor_dictionary[q[0][0]] = successor[0][0]
                        
