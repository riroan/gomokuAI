import numpy as np

class Node:
    def __init__(self, action, cfg, color, P=0, parent = None):
        self.N = 0
        self.Q = 0
        self.W = 0
        self.U = 0
        self.P = P
        self.value = 0

        self.color = color # next color

        self.parent = parent
        self.action = action
        self.children = []

        self.end = False
        self.cfg = cfg

    def get_action(self):
        N_tau = np.array([child.N**(1/self.cfg.tau) for child in self.children])
        s = sum(N_tau)
        pi = np.array([i/s for i in N_tau])

        # Deterministic Policy
        #return np.argmax(pi)

        # Stochastic Policy
        return np.random.choice(np.arange(self.cfg.BOARD_SIZE**2), p=pi)
        

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
        for i in range(self.cfg.BOARD_SIZE*self.cfg.BOARD_SIZE):
            self.children.append(Node(i, self.cfg, -self.color, p[i], self))

    def backup(self, value):
        self.N+=1
        self.W+=value
        self.Q = self.W/self.N
        if not self.is_root():
            self.parent.backup(-self.cfg.decay * value)

    def UCB(self):
        self.U = self.cfg.c_puct * self.P * np.sqrt(self.parent.N) / (1+self.N)
        return self.U + self.Q