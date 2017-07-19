import numpy as np
import matplotlib.pyplot as plt
from grid_world import standard_grid

SMALL_ENOUGH = 1e-3

def print_values(V, g):
    for i in range(g.width):
        print("---------------------------")
        for j in range(g.height):
            v = V.get((i,j), 0)
            if v >= 0:
                print(" %.2f|" %v, end="")
            else:
                print("%.2f|" % v, end='')
        print("")

def print_policy(P, g):
    '''Only works for deterministic Policies'''
    for i in range(g.width):
        print("---------------------------")
        for j in range(g.height):
            a = P.get((i,j), " ")
            print(" %s |" % a, end="")
        print("")

if __name__ == '__main__':
    # iterative policy evaluation
    # given a policy, let's find it's value functions V(s)
    # we will do this for both a uniform random policy and fixed policy
    grid = standard_grid()
    states = grid.all_states()

    V = {}
    for s in states:
        V[s] = 0
    gamma = 1.0
    while True:
        biggest_change = 0
        for s in states:
            old_v = V[s]

            # V(s) only has value if it's not a terminal state
            if s in grid.actions:

                new_v = 0
                p_a = 1.0 / len(grid.actions[s])
                for a in grid.actions[s]:
                    grid.set_state(s)
                    r = grid.move(a)
                    new_v += p_a * (r + gamma * V[grid.current_state()])
                V[s] = new_v
                biggest_change = max(biggest_change, np.abs(old_v - V[s]))
                
        if biggest_change < SMALL_ENOUGH:
            break
    print("values for uniformly random actions:")
    print_values(V, grid)
    print('\n\n')


    ### fixed Policy ###
    policy = {
        (2,0): 'U',
        (1,0): 'U', 
        (0,0): "R",
        (0,1): 'R',
        (0,2): 'R',
        (1,2): 'R',
        (2,1): 'R',
        (2,2): 'R',
        (2,3): 'U'
    }
    print_policy(policy, grid)

    # initialize V(s) = 0
    V = {}
    for s in states:
        V[s] = 0
    
    # let's see how V(s) changes as we get further away from the reward
    gamma = 0.9

    # repeat until convergence
    while True:
        biggest_change = 0
        for s in states:
            old_v = V[s]

            # V(s) only has value if it's not a terminal state
            if s in policy:
                a = policy[s]
                grid.set_state(s)
                r = grid.move(a)
                V[s] = r + gamma * V[grid.current_state()]
                biggest_change = max(biggest_change, np.abs(old_v - V[s]))
            
        if biggest_change < SMALL_ENOUGH:
            break
    print('Values for fixed Policy')
    print_values(V, grid)