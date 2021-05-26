import numpy as np


class Node:
    t = 0
    def __init__(self, game):
        self.game = game
        self.state = game.getState()
        self.w = 0
        self.n = 0
        self.child_nodes = []

    def getUCB(self):
        return self.w / self.n + np.sqrt(2 * np.log(Node.t) / self.n)

