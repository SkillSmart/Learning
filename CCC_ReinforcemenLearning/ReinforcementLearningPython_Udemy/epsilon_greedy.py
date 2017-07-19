import numpy as np
import matplotlib.pyplot as plt
from random import random, randint

class Bandit(object):
    def __init__(self, m):
        self.m = m
        self.mean = 0
        self.N = 0

    def pull(self):
        return np.random.randn() + self.m

    def update(self, x):
        self.N += 1
        self.mean = (1-1.0/self.N)*self.mean + 1.0/self.N*x
    
def run_experiment(m1, m2, m3, eps, N):
    bandits = [Bandit(m1), Bandit(m2), Bandit(m3)]

    data = np.empty(N)
    results = []
    for i in range(N):
        
        # epsilon greedy implementation
        p = random()
        if p < 1/(i+1):
            # Explore a random Bandit
            j = np.random.choice(3)
        else:
            j = np.argmax([b.mean for b in bandits])
            
            # Exploit the best option
        x = bandits[j].pull()
        bandits[j].update(x)
            
        # For the plotting
        data[i] = x
    cumulative_average = np.cumsum(data) / (np.arange(N) + 1)

    # plotting the moving averae ctr
    plt.plot(cumulative_average)
    plt.plot(np.ones(N)*m1)
    plt.plot(np.ones(N)*m2)
    plt.plot(np.ones(N)*m3)
    plt.xscale('log')
    plt.show()

    for b in bandits:
        print(b.mean)

    return cumulative_average


run_experiment(1.0, 2.0, 3.0 , 0.1, 10000)