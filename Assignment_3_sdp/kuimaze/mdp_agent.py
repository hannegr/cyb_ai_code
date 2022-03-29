from cmath import inf
import random
import numpy as np 

import kuimaze.maze


def find_policy_via_value_iteration(problem, discount_factor, epsilon): 
    '''
    TODO write a description here. 
    '''
    value = 0.0
    all_states = problem.get_all_states()
    value_list = [] 
    threshold = epsilon*(1-discount_factor)*discount_factor
    
    for state_index in range(len(all_states)): 
        value_list.append([all_states[state_index], None, value, value])        
    while True:
        delta = 0.0
        for state_value_index in range(len(value_list)): 
            reward = value_list[state_value_index][0][2]
            updated_value_list = sum_probability_values(problem, state_value_index, value_list)
            new_state_value = reward + discount_factor*updated_value_list
            value_difference = new_state_value- value_list[state_value_index][3]  #abs(value_list[state_value_index][3] - new_state_value)
            delta = max(value_difference, delta)
            value_list[state_value_index][3] = new_state_value
        if delta <= threshold: 
            break   
    return turn_list_into_dictionary(value_list)

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
                    sum_action_values += value[3]*next_state[1]
        
        if sum_action_values > max_value: 
            max_value = sum_action_values
            value_list[state_value_index][2] = sum_action_values
            value_list[state_value_index][1] = action
            
    return max_value

    


def turn_list_into_dictionary(mdp_list): 
    '''
    TODO write a description here. 
    '''
    state_action_dictionary = {}
    for state_values in mdp_list:
        #state_values[1] contains the state which we want to be the key, and state_values[2] 
        #contains the optimal action. 
        state_action_dictionary[state_values[0][0:2]] = state_values[1]
    return state_action_dictionary
            
        
      

def find_policy_via_policy_iteration(problem, discount_factor): 
    '''
    TODO write a description here. 
    '''
    V = 0.0
    all_states = problem.get_all_states()
    policy_list = []
    changed = True
    for state in all_states: 
        policy_list.append([state, random.choice(list(problem.get_actions(state))), V]) #trenger muligens ikke V. 
    while changed: 
        changed = False
        for policy_index in range(len(policy_list)): 
            policy_evaluation(problem, policy_index, policy_list, discount_factor)
        for policy_index in range(len(policy_list)):
            better_action = better_max_action(problem, policy_index, policy_list)
            if (better_action != None) and better_action != policy_list[policy_index][1]: #muligens heller sammenligne verdier her!!!
                #better_max_action: return first the value of the maximum action, and then the best action as the second element! 
                policy_list[policy_index][1] = better_action
                changed = True 
    return turn_list_into_dictionary(policy_list)


def policy_evaluation(problem, policy_list_index, policy_list, discount_factor): 
    '''
    TODO write a description here. 
    '''
    policy_value = 0
    next_states_and_probs = problem.get_next_states_and_probs(policy_list[policy_list_index][0], policy_list[policy_list_index][1])
    for next_state in next_states_and_probs: 
            for policy in policy_list: 
                if policy[0][0:2] in next_state:
                    policy_value += policy[2]*next_state[1]
    policy_value = policy_list[policy_list_index][0][2] + discount_factor*policy_value
    policy_list[policy_list_index][2] = policy_value
    #return policy_value #do I even need to return anything here? 



def better_max_action(problem, policy_index, policy_list):
    '''
    TODO write a description here. 
    ''' 
    max_value = -inf
    best_action = None
    all_actions = problem.get_actions(policy_list[policy_index][0])
    for action in all_actions: 
        sum_action_values = 0
        next_states_and_probs = problem.get_next_states_and_probs(policy_list[policy_index][0], action)
        for next_state in next_states_and_probs: 
            for policy in policy_list: 
                if policy[0][0:2] in next_state:
                    sum_action_values += policy[2]*next_state[1]
        if sum_action_values > max_value: 
            max_value = sum_action_values
            best_action = action           
    return best_action