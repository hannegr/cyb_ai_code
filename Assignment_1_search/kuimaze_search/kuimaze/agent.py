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
    
    def _h_score(self, position, goal): 
        """
        Chooses the Manhattan distance as my heuristic distance, because of how the maze looks like (because we have 8 
        neighbours). 
        """
        dx = abs(position[0] - goal[0])
        dy = abs(position[1] - goal[1])
        return (dx + dy)    
    
    def _g_score(self, position, previous_position): 
        position[1] = position[1] + previous_position[0][1]
        return position[0][1]
        
    
    def _f_score(self, goal, positions, prev_pos):
        """
        Used to find the f-score of the predecessor nodes. 
        """
        f_score_list = []
        for position in positions: 
            pos_h_score = self._h_score(position[0], goal)
            pos_g_score = self._g_score(position, prev_pos)
            pos_f_score = pos_h_score + pos_g_score
            f_score_list.append([position, pos_f_score])
        return f_score_list 
    
            
    def _smallest_f_value(self, frontier_list, successor_place): 
        """
        A helping function for find_path. Is used to find out if the position is already in the explore_list with a 
        smaller value than the new explored version of it. 
        
        """
        same_place_successors = [successor_place]
        for successor in frontier_list: 
            if successor_place[0][0] in successor: 
                same_place_successors.append(successor)
        if min(same_place_successors) != successor_place: 
            return False
        return True
            
        
    
    
    def find_path(self):
        '''
        Implemented A* algorithm. Contains 
        - frontier_list: list showing the neighbournodes that may be expanded if the cost is minimal. 
        - closed_set: a set s.t the values are not repeated. Includes every node that is finished. 
        - predecessor_dictionary: a dictionary containing predecessor of nodes, used for returning the shortest path. 
          Chose to do this, due to what was written on the wikipedia-page of the A* algorithm about it returning the 
          shortest path, but not the way to get there. 
    
        Returns: path_list, list of the shortest path from start node to goal node. 
        '''
        observation = self.environment.reset()
        goal = observation[1][0:2] #goal position
        start_node = observation[0][0:2] #start position
        q = [[start_node, 0], self._h_score(start_node, goal)]
        predecessor_dictionary = {}    
        path_list = []    
        frontier_list = [q]
        explored_set = set()
         
        while frontier_list: 
            frontier_list.sort(reverse=True)
            q = frontier_list.pop() 
            explored_set.add(q[0][0])
            if(successor[0][0] == goal): #goal was found, can therefore go out of the loop
                break
            q_successors = self.environment.expand(q[0][0])  
            successors_with_f_values = self._f_score(goal, q_successors, q)
            for successor in successors_with_f_values: 
                if(successor[0][0] not in explored_set and self._smallest_f_value(frontier_list, successor)): 
                    frontier_list.append(successor)
                    predecessor_dictionary[q[0][0]] = successor[0][0]
                    if(successor[0][0] == goal): #goal was found, can therefore go out of the loop
                        break
        if goal not in predecessor_dictionary.values(): 
            return None
        path_node = start_node
        while goal not in path_list: 
            if path_node == None: 
                return None
            path_list.append(path_node)
            path_node = predecessor_dictionary.get(path_node)
        return path_list
