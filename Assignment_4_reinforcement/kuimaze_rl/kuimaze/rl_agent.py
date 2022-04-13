import math
import numpy as np
import random 
import time 

def find_epsilon(number_of_iterations): 
    '''
    Used to find epsilon, which works as a threshold in the function find_action. 
    epsilon will be a value between 1 and 0, because it should be a probability. It 
    will depend on the number of iterations in the given episode, and grow smaller as 
    the number of iterations increases. The formula chosen is based on a previous 
    course I had, where we were taught that it should grow smaller with time. 
    Input: 
        number_of_iterations: the number of iterations in the given episode 
    Output: 
        epsilon: value between 0 and 1 
    '''
    epsilon = 0.99/number_of_iterations 
    return epsilon

def find_action(epsilon, env, state, q_table, policy, eps_greedy): 
    '''
    Used to find the action in the given state. Finds a random value between 0 and 1, 
    and if that value is lower than epsilon and we want to use the epsilon-greedy strategy, 
    the action will be chosen at random. If not the action will be the action resulting in 
    the maximum q-value. 
    Input: 
        epsilon: value between 0 and 1 
        env: environment the agent operates in 
        state: current state 
        q_table: table with q-values 
        policy: dictionary with states as key-values and actions as item-values 
        eps_greedy: boolean value that is True if we want to use the epsilon-greedy strategy
    Output: 
        action: the calculated action 
    '''
    threshold = random.uniform(0,1)
    if threshold <= epsilon and eps_greedy:
        action = env.action_space.sample()
    else: 
        action = np.argmax(q_table[state[0]][state[1]])
        policy[state] = action
    return action 



def learn_policy(env): 
    '''
    This is an implementation of the TD q-learning algorithm precented in lecture 9 of the 
    course Cybernetics and Artificial Intelligence 
    (page 16 in this lecture: https://cw.fel.cvut.cz/wiki/_media/courses/be5b33kui/lectures/09_rl.pdf). 
    Temporal difference learning is in this case used in order to find the new q-value of a given state, 
    and an epsilon-greedy algorithm is deployed to find a good exploration-vs-exploitation strategy. 
    alpha and the discount rate have been found experimentally. 
    Input: 
        env: The environment the agent operates in. 
    Output: 
        policy: A dictionary containing states as key-values and corresponing actions (as integers) as items. 
    '''
    # Number of discrete x- and y-dimensions 
    x_dims = env.observation_space.spaces[0].n
    y_dims = env.observation_space.spaces[1].n
    maze_size = tuple((x_dims, y_dims))
    # Number of discrete actions
    num_actions = env.action_space.n
    # Table with q-values:
    q_table = np.zeros([maze_size[0], maze_size[1], num_actions], dtype=float)
    #how much weight is putted on future values 
    discount_rate = 0.8
    policy = {}
    start_time = time.time()
    while True:
        #want to keep learning as long as possible, so check the time 
        #if(time.time() - start_time > 19.5): 
        #    break 
        epsilon = 1
        alpha = 0.2
        number_of_iterations = 1
        terminal = False
        obv = env.reset()
        state = obv[0:2]
        #stop if we have terminal state
        while not terminal: 
            action = find_action(epsilon, env, state, q_table, policy, True)
            obv, reward, terminal, _ = env.step(action)
            epsilon = find_epsilon(number_of_iterations)
            next_state = obv[0:2]
            next_state_max_action = find_action(epsilon, env, next_state, q_table, policy, False) 
            #uses the formula q(state, action) = q(state, action) + alpha*[reward + discount factor*max(q(next state, next action)) - q(state, action)]
            q_table[state[0]][state[1]][action] = q_table[state[0]][state[1]][action] + alpha*(reward + discount_rate*q_table[next_state[0]][next_state[1]][next_state_max_action] - q_table[state[0]][state[1]][action])
            state = next_state
            number_of_iterations += 1 
    return policy

def learn_policy2(env): 
    '''
    This is Sarsa. Did not work as well as normal q-learning in this case.
    '''
    x_dims = env.observation_space.spaces[0].n
    y_dims = env.observation_space.spaces[1].n
    maze_size = tuple((x_dims, y_dims))
    # Number of discrete actions
    num_actions = env.action_space.n
    # Q-table:
    q_table = np.zeros([maze_size[0], maze_size[1], num_actions], dtype=float)
    discount_rate = 0.8
    policy = {}
    for episode_length in range(1000):
        epsilon = 1
        alpha = 1
        number_of_iterations = 1
        terminal = False
        obv = env.reset()
        state = obv[0:2]
        action = find_action(alpha, env, state, q_table, policy, True)
        obv, reward, terminal, _ = env.step(action)
        while not terminal and epsilon > 0.0009:  
            obv, new_reward, terminal, _ = env.step(action)
            next_state = obv[0:2]
            next_action = find_action(alpha, env, next_state, q_table, policy, True) 
            alpha = find_alpha(number_of_iterations)
            epsilon = find_epsilon(number_of_iterations)
            q_table[state[0]][state[1]][action] = q_table[state[0]][state[1]][action] + alpha*(reward + discount_rate*q_table[next_state[0]][next_state[1]][next_action] - q_table[state[0]][state[1]][action])
            state, action, reward = next_state, next_action, new_reward 
            number_of_iterations += 1
    return policy

def find_alpha(number_of_iterations): 
    '''
    TODO function description here! 
    '''
    alpha = math.exp(-0.05*(number_of_iterations-1))
    return alpha