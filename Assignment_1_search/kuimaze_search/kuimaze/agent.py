from kuimaze.baseagent import BaseAgent
import random 
import time
import kuimaze
import numpy as np



class Agent(BaseAgent):
    '''
    Simple example of agent class that inherits kuimaze.BaseAgent class 
    '''
    def __init__(self, environment, distance_matrix=None):
        self.environment = environment
    
    def _h_score(self, position, goal): 
        """
        Returns the heuristic distance of a position, the h score, here chosen as the euclidian distance. 
        Input:
            position: The position we want to find the heuristic distance of. 
            goal: The end position. 
        Output:
            dx + dy: The euclidian distance between position and goal
        """
        dx = pow(abs(position[0] - goal[0]),2)
        dy = pow(abs(position[1] - goal[1]),2)
        return np.sqrt(dx + dy)    
    
    def _g_score(self, position, previous_position):
        """
        Returns the sum of the g score from the start position to the current position. 
        Input:
            position: The position we want to find the g score of
            previous_position: The previous position 
        Output:
            position[0][1]: the new g score of position
        """ 
        position[1] = position[1] + previous_position[0][1]
        return position[0][1]
        
    
    def _f_score(self, goal, positions, prev_pos):
        """
        Returns the f score of a list of positions, by summing their h score and g score.
        Input:
            positions: The positions we want to find the f scores of
            prev_pos: The previous position
            goal: the end position
        Output:
            f_score_list: a list of the positions with their f scores
        """ 
        f_score_list = []
        for position in positions: 
            pos_h_score = self._h_score(position[0], goal)
            pos_g_score = self._g_score(position, prev_pos)
            pos_f_score = pos_h_score + pos_g_score
            f_score_list.append([position, pos_f_score])
        return f_score_list 
    
            
    def _smallest_f_value(self, frontier_list, frontier): 
        """
        Returns the smallest f score given in the list frontier_list. Is used to find out if the position is already 
        in the explore list with a smaller value than the new explored version of it.  
        Input:
            frontier_list: list of every frontier. 
            frontier: The frontier we want to check if has the smallest f score in its position
        Output:
            True if frontier had the smallest f score in its position, if not False
        """ 
        same_place_frontiers = [frontier]
        for successor in frontier_list: 
            if frontier[0][0] in successor: 
                same_place_frontiers.append(successor)
        if min(same_place_frontiers) != frontier: 
            return False
        return True
            
        
    
    
    def find_path(self):
        '''
        Implemented A* algorithm. Returns the optimal path from a start position to goal. 
        Contains 
        - frontiers: list showing the neighbours of the explored nodes
        - explored: a set of already explored nodes
        - predecessors_and_children: a dictionary containing predecessor of nodes, used for returning the shortest path. 
        Output: path, list of the shortest path from start node to goal node. 
        '''
        observation = self.environment.reset()
        goal = observation[1][0:2] #goal position
        start = observation[0][0:2] #start position
        current = [[start, 0], self._h_score(start, goal)]
        predecessors_and_children = {}    
        path = []    
        frontiers = [current]
        explored = set()
         
        while frontiers: 
            frontiers.sort(reverse=True) #make a priority queue
            current = frontiers.pop() 
            explored.add(current[0][0])
            if(current[0][0] == goal): #goal was found, can therefore go out of the loop
                break
            current_successors = self.environment.expand(current[0][0])  
            successors_with_f_values = self._f_score(goal, current_successors, current)
            for successor in successors_with_f_values: 
                if(successor[0][0] not in explored): 
                    predecessors_and_children[current[0][0]] = successor[0][0]
                    if(self._smallest_f_value(frontiers, successor)): 
                        frontiers.append(successor)
        if goal not in predecessors_and_children.values(): 
            return None
        path_node = start
        while goal not in path: 
            if path_node == None: 
                return None
            path.append(path_node)
            path_node = predecessors_and_children.get(path_node)
        return path
        
    
    
   