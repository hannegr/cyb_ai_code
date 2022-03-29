from cmath import inf
import collections
import random

import kuimaze.maze


def find_policy_via_value_iteration(problem, discount_factor, epsilon): 
    '''
    TODO write a description here. 
    '''
    value = 0.0
    all_states = problem.get_all_states()
    value_list = []
    for state_index in range(len(all_states)): 
        value_list.append([all_states[state_index], None, value, value])#[0], all_states[state_index][1]])
    while True:
        delta = 0.0
        for state_value_index in range(len(value_list)): 
            reward = value_list[state_value_index][0][2]
            updated_value_list = sum_probability_values(problem, state_value_index, value_list)
            new_state_value = reward + discount_factor*updated_value_list
            value_difference = abs(value_list[state_value_index][3] - new_state_value)
            if(value_difference > delta): 
                delta = value_difference
            value_list[state_value_index][3] = new_state_value
        if delta <= (epsilon*(1-discount_factor)*discount_factor): 
            break   
    return turn_value_list_into_dictionary(value_list)

def sum_probability_values(problem, state_value_index, value_list):
    '''
    TODO write a description here. 
    '''
    max_value = -inf
    all_actions = problem.get_actions(value_list[state_value_index][0])
    for action in all_actions: 
        sum_action_values = 0
        next_states_and_probs = problem.get_next_states_and_probs(value_list[state_value_index][0], action)
        
        for next_state in next_states_and_probs: 
            for value in value_list: 
                if value[0][0:2] in next_state:
                #if next_state == value[0][0:2]: 
                    sum_action_values += value[3]*next_state[1]
        
        if sum_action_values > max_value: 
            max_value = sum_action_values
            value_list[state_value_index][2] = sum_action_values
            value_list[state_value_index][1] = action
            
    return max_value


def turn_value_list_into_dictionary(value_list): 
    '''
    TODO write a description here. 
    '''
    state_action_dictionary = {}
    for state_values in value_list:
        #state_values[1] contains the state which we want to be the key, and state_values[2] 
        #contains the optimal action. 
        state_action_dictionary[state_values[0][0:2]] = state_values[1]
    return state_action_dictionary
            
        
      

def find_policy_via_policy_iteration(problem, discount_factor): 
    '''
    TODO write a description here. 
    '''
    return None 