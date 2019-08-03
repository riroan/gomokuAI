from param import *

class Node:
    def __init__(self, P = 0, player = BLACK, parent = None):
        self.N = 0
        self.W = 0
        self.Q = 0
        self.v = 0
        self.P = P
        self.player = player
        self.child = []
        self.parent = parent
        self.Over = False
        
    def selection(self, valid_vector):
        PUCT = [math.sqrt(2)*i.P*i.parent.N/(1+i.N) + i.Q for i in self.child]
        idx = np.argsort(PUCT)
        idx = np.flip(idx)
        for i in idx:
            if valid_vector[i]:
                return child[i], i
            
    def expansion(self,p):
        for i in range(BOARD_SIZE*BOARD_SIZE):
            self.child.append(Node(p[i],-player,self))
                
    def backup(self):
        Node = self
        if Node.parent is None
            Node.N+=1
            Node.W+=self.v
            Node.Q=Node.W/Node.N
            return
        
        while Node.parent:
            Node.N += 1
            Node.W += self.v
            Node.Q = Node.W/Node.N
            Node = Node.parent