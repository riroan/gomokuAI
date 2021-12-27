import numpy as np
from Game import Game
import copy


class Node:
    t = 0
    threshold = 10

    def __init__(self, state, player):
        self.state = state
        self.player = player  # 지금 둔사람    !! 둘사람 아님 !!
        self.w = 0
        self.n = 0
        self.child_nodes = {}
        self.parent = None
        self.size = len(self.state)


    def getUCB(self):
        if self.n == 0:
            return 0
        return self.w / self.n + np.sqrt(2 * np.log(Node.t) / self.n)

    def getAbleAction(self, state):
        actions = []
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] == 0:
                    actions.append(i * self.size + j)
        return actions

    def selection(self):
        node = self
        while len(node.child_nodes):
            candidate = []
            for k in self.child_nodes:
                if self.child_nodes[k].n == 0:
                    candidate.append(k)
            if candidate:
                node = self.child_nodes[np.random.choice(candidate)]
            else:
                UCB = {}
                m = -1
                action = 0
                for k in self.child_nodes:
                    UCB[k] = self.child_nodes[k].getUCB()
                    if m < UCB[k]:
                        m = UCB[k]
                        action = k
                node = self.child_nodes[action]

        return node

    def expansion(self):
        actions = self.getAbleAction(self.state)
        for action in actions:
            new_state = copy.deepcopy(self.state)
            new_state[action // self.size][action % self.size] = -self.player
            self.child_nodes[action] = Node(new_state, -self.player)
            self.child_nodes[action].parent = self

    def simulation(self):
        game = Game(self.size)
        game.board = self.state.copy()
        game.player = -self.player

        while not game.gameOver:
            actions = self.getAbleAction(game.board)
            randomAction = np.random.choice(actions)
            game.doAction(randomAction)
        self.n += 1
        if game.winner == self.player:
            self.w += 1
            return True  # 이김
        else:
            return False  # 짐

    def update(self, isWin):
        self.n += 1
        Node.t += 1
        node = self.parent
        while node is not None:
            if isWin:
                node.w += 1
            else:
                node.w -= 1
            node.n += 1
            node = node.parent

    def rollout(self):
        node = self.selection()
        if node.n >= self.threshold:
            node.expansion()
            node = node.selection()
        isWin = node.simulation()
        node.update(isWin)

    def getAction(self, epochs=500):
        self.expansion()
        for _ in range(epochs):
            self.rollout()
        UCB = {}
        m = -1
        action = 0
        for k in self.child_nodes:
            UCB[k] = self.child_nodes[k].getUCB()
            if m < UCB[k]:
                m = UCB[k]
                action = k
        Node.t = 0
        print(UCB)

        return action

    def getAbleActions(self, state):
        actions = []
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] == 0:
                    actions.append(i * self.size + j)
        return actions
