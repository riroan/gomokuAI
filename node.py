import numpy as np
from config import *

class Node:
    def __init__(self, action, color, P=0, parent = None):
        self.N = 0
        self.Q = 0
        self.W = 0
        self.U = 0
        self.P = P

        self.color = color # next color

        self.parent = parent
        self.action = action
        self.children = []

        self.end = False

    def get_action(self):
        N_tau = np.array([child.N**(1/tau) for child in self.children])
        s = sum(N_tau)
        pi = np.array([i/s for i in N_tau])

        # Deterministic Policy
        return np.argmax(pi)

        # Stochastic Policy
        # return np.random.choice(np.arange(BOARD_SIZE**2), p=pi)
        

    def is_root(self):
        return self.parent == None

    def is_leaf(self):
        return len(self.children) == 0
    
    def selection(self, valid):
        ucb_list = np.array([child.UCB() for child in self.children])
        index = np.argsort(ucb_list)[::-1]
        for ix in index:
            if valid[ix]:
                action = ix
                break
        next_node = self.children[action]
        return next_node, action

    def expansion(self, p):
        for i in range(BOARD_SIZE*BOARD_SIZE):
            self.children.append(Node(i, -self.color, p[i], self))

    def backup(self, value):
        self.N+=1
        self.W+=value
        self.Q = self.W/self.N
        if not self.is_root():
            self.parent.backup(-decay * value)

    def UCB(self):
        self.U = c_puct * self.P * np.sqrt(self.parent.N) / (1+self.N)
        return self.U + self.Q