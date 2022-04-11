from cmath import inf
import random
import numpy as np 
import time 
            
            
def find_policy_via_policy_iteration(problem, discount_factor): 
    '''
    Uses policy iteration in order to find the hopefully optimal policy for the agent to use in the maze. 
    The pseudocode for policy iteration from lecture 7 i Cybernetics and AI is used, with a slight change in how the 
    expected value is found, taken from this link: https://core-robotics.gatech.edu/2021/01/19/bootcamp-summer-2020-week-3-value-iteration-and-q-learning/
    Input: 
        problem: the enviroment the agent is in 
        discount_factor: a number between 0 and 1 that tells us how much less we value the future actions compared with the current 
    Output: 
        policy_dictionary: Dictionary with state-action pair, a.k.a the policy (state as key and action as item).
    ''' 
    all_states = problem.get_all_states()
    policy_dictionary = {}
    changed = True
    for state in all_states: 
        #adds the state (without the reward) as the key, and a list with value of 0.0 and a random action as the items
        policy_dictionary[state[0:2]] = [0.0, random.choice(list(problem.get_actions(state)))]   
    while changed: 
        for state in all_states:     
            policy_evaluation(problem, policy_dictionary, discount_factor, state)
        changed = False
        for state in all_states: 
            best_action = better_max_action(problem, policy_dictionary, state, discount_factor)
            #checks if a better action exists and if it is not equal to the current action
            if(best_action != None and best_action != policy_dictionary[state[0:2]][1]): 
                changed = True 
                policy_dictionary[state[0:2]][1] = best_action
        
    for state in all_states: 
        policy_dictionary[state[0:2]] = policy_dictionary[state[0:2]][1] 
        if problem.is_terminal_state(state):
            #do not need an action for the terminal states 
            policy_dictionary[state[0:2]] = None
    return policy_dictionary
    
def better_max_action(problem, policy_dictionary, state, discount_factor):
    '''
    Finds out if there is a better action given the state the robot is in.
    Output: 
        best_action: The best action that can be taken considering the expected value. 
    ''' 
    max_value = policy_dictionary[state[0:2]][0]
    best_action = None
    reward = state[2]
    all_actions = problem.get_actions(state)
    for action in all_actions: 
        value = sum((probability*(reward + discount_factor*policy_dictionary[next_state[0:2]][0])) for next_state, probability in problem.get_next_states_and_probs(state, action))
        if(value > max_value):
            max_value, best_action = value, action 
    return best_action
      
def policy_evaluation(problem, policy_dictionary, discount_factor, state): 
    '''
    Evaluates the given policy at the moment, by finding the expected value given the state and action. 
    '''
    action = policy_dictionary[state[0:2]][1]
    reward = state[2]
    policy_dictionary[state[0:2]][0] = sum((probability*(reward + discount_factor*policy_dictionary[next_state[0:2]][0])) for next_state, probability in problem.get_next_states_and_probs(state, action))


def find_policy_via_value_iteration(problem, discount_factor, epsilon):
    
    '''
    Uses value iteration in order to find the hopefully optimal policy for the agent to use in the maze. 
    The pseudocode for value iteration from lecture 7 i Cybernetics and AI is used, with a slight change in how the 
    expected value is found, taken from this link: https://core-robotics.gatech.edu/2021/01/19/bootcamp-summer-2020-week-3-value-iteration-and-q-learning/ 
    Input: 
        problem: the enviroment the agent is in 
        discount_factor: a number between 0 and 1 that tells us how much less we value the future actions compared with the current
        epsilon: small value that helps decide the threshold for when the change of values are so small that we are happy with our policy 
    Output: 
        policy_dictionary: Dictionary with state-action pair, a.k.a the policy (state as key and action as item).  
    '''
    
    policy_dictionary = {}
    all_states = problem.get_all_states()
    #The threshold delta must be smaller than for us to be happy with our policy solution 
    threshold = epsilon*(1-discount_factor)*discount_factor 
    start_time = time.time() 
    for state in all_states:
        #adds the state (without the reward) as the key, and a list with value of 0.0 and None, meaning that the robot has no policy yet 
        policy_dictionary[state[0:2]] = [0.0, None]

    while True: 
        delta = 0.0 
        for state in all_states: 
            max_action = None 
            max_value = -inf
            for action in problem.get_actions(state):
                #state[2] is the reward
                value = sum(probability*(state[2] + discount_factor*policy_dictionary[next_state[0:2]][0]) for next_state, probability in problem.get_next_states_and_probs(state, action))
                if value > max_value: 
                    max_value = value
                    if not problem.is_terminal_state(state): 
                        max_action = action 
            difference_new_and_old_value = max_value - policy_dictionary[state[0:2]][0]
            delta = max(delta, difference_new_and_old_value)
            #add the new value and associated action to the dictionary 
            policy_dictionary[state[0:2]] = [max_value, max_action]
        if(delta <= threshold or time.time() - start_time > 29.3):
            break 
    for state in policy_dictionary:
        #we only want to get out the state and associated action, not the value
        policy_dictionary[state] = policy_dictionary[state][1]
    return  policy_dictionary                                                                                                    