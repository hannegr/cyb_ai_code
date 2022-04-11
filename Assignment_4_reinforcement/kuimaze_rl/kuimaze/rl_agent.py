import math
import numpy as np
import random 
import time 

def learn_policy2(env): 
    '''
    This is Sarsa 
    TODO function description here! 
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
    #print(policy)
    #print(q_table)
    return policy



def find_epsilon(number_of_iterations): 
    '''
    TODO function description here! 
    '''
    epsilon = 0.99/(number_of_iterations) 
    return epsilon


 
def find_alpha(number_of_iterations): 
    '''
    TODO function description here! 
    '''
    alpha = math.exp(-0.05*(number_of_iterations-1))
    return alpha

def find_action(epsilon, env, state, q_table, policy, eps_greedy): 
    threshold = random.uniform(0,1)
    if threshold <= epsilon and eps_greedy:
        action = env.action_space.sample()
    else: 
        action = np.argmax(q_table[state[0]][state[1]])
        policy[state] = action
    return action 



def learn_policy(env): 
    '''
    This is TD with q-learning 
    TODO function description here! 
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
    start_time = time.time()
    #for episode_length in range(1000):
    while True:
        epsilon = 1
        alpha = 1
        number_of_iterations = 1
        terminal = False
        obv = env.reset()
        state = obv[0:2]
        #action = find_action(alpha, env, state, q_table, policy) 
        #obv, reward, terminal, _ = env.step(action)
        while not terminal and epsilon > 0.0009:  
            action = find_action(alpha, env, state, q_table, policy, True)
            obv, reward, terminal, _ = env.step(action)
            alpha = find_alpha(number_of_iterations)
            epsilon = find_epsilon(number_of_iterations)
            next_state = obv[0:2]
            next_state_optimal_action = find_action(alpha, env, next_state, q_table, policy, False) 
            
            q_table[state[0]][state[1]][action] = q_table[state[0]][state[1]][action] + alpha*(reward + discount_rate*q_table[next_state[0]][next_state[1]][next_state_optimal_action] - q_table[state[0]][state[1]][action])
            #state, action, reward = next_state, next_action, new_reward 
            state = next_state
            number_of_iterations += 1
        if(time.time() - start_time > 19.6): 
            break 
    #print(policy)
    #print(q_table)
    return policy