from cmath import inf
import random
import numpy as np 
#import kuimaze.maze
import itertools
#import copy 
import time 


def find_policy_via_value_iteration1(problem, discount_factor, epsilon): 
    '''
    TODO write a description here. 
    '''
    value = 0.0
    all_states = problem.get_all_states()
    value_list = [] 
    for state in all_states: 
        value_list.append([state, None,value])
    threshold = epsilon*(1-discount_factor)*discount_factor
    start_time = time.time()
    while True:
        delta = 0.0
        for state_value_index in range(len(value_list)): 
            old_max_value = value_list[state_value_index][2]
            #updated_max_value = sum_probability_values(problem, state_value_index, value_list, discount_factor)
            delta = max(sum_probability_values(problem, state_value_index, value_list, discount_factor) - old_max_value , delta)
        if delta <= threshold or time.time() - start_time > 28: 
            break   
    return turn_list_into_dictionary(value_list)

def sum_probability_values(problem, state_value_index, value_list, discount_factor):
    '''
    TODO write a description here. 
    '''
    max_value = -inf
    max_action = None 
    all_actions = problem.get_actions(value_list[state_value_index][0])
    for action in all_actions: 
        sum_action_values = 0
        next_states_and_probs = problem.get_next_states_and_probs(value_list[state_value_index][0], action)
        for next_state in next_states_and_probs:
            sum_action_values += next(itertools.dropwhile(lambda value : value[0][0:2] != next_state[0][0:2], value_list))[2]*next_state[1] #even a little bit faster than previous one lol 
        if sum_action_values > max_value: 
            max_value = sum_action_values
            max_action = action
    value_list[state_value_index][2] = value_list[state_value_index][0][2] + discount_factor*max_value
    value_list[state_value_index][1] = max_action 
    return value_list[state_value_index][2]

    


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
            if (better_action != None) and better_action != policy_list[policy_index][1]:
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

def find_policy_via_value_iteration(problem, discount_factor, epsilon):
    '''
    TODO description here 
    '''
    state_reward_actions = {}
    all_states = problem.get_all_states()
    threshold = epsilon*(1-discount_factor)*discount_factor 
    for state in all_states:
        state_reward_actions[state[0:2]] = [0.0, None]
    while True: 
        delta = 0.0 
        for state in all_states: 
            max_action = None 
            max_value = -inf
            #test = (max([sum((probability*state_reward_actions[next_state[0:2]][0]) for next_state, probability in problem.get_next_states_and_probs(state, action))] for action in problem.get_actions(state)))[0]
            for action in problem.get_actions(state): 
                value = sum((probability*state_reward_actions[next_state[0:2]][0]) for next_state, probability in problem.get_next_states_and_probs(state, action))
                if value > max_value: 
                    max_value = value 
                    max_action = action 
            max_value = state[2] + discount_factor*max_value 
            delta = max(delta, max_value - state_reward_actions[state[0:2]][0])
            state_reward_actions[state[0:2]] = [max_value, max_action]
        if(delta <= threshold):
            break 
    for state in state_reward_actions:
        state_reward_actions[state] = state_reward_actions[state][1]
    return  state_reward_actions                                                                                                      

        
        