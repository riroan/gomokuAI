from param import *
import math

class Node:
    def __init__(self, P = 0, player = BLACK, parent = None):
        self.N = 0
        self.W = 0
        self.Q = 0
        self.v = 0
        self.P = P
        self.value_decay = 0.95
        self.player = player
        self.child = []
        self.parent = parent
        self.Over = False
        
    def selection(self, valid_vector):
        PUCT = [5*i.P*i.parent.N/(1+i.N) + i.Q for i in self.child]
        idx = np.argsort(PUCT)
        idx = np.flip(idx, axis = 0)
        for i in idx:
            if valid_vector[i]:
                return self.child[i], i
            
    def expansion(self,p):
        #for i in range(BOARD_SIZE*BOARD_SIZE):
        #    self.child.append(Node(p[i],-self.player,self))
        self.child = [Node(p[i],-self.player,self) for i in range(BOARD_SIZE*BOARD_SIZE)]
                
    def backup(self):
        Node = self
        v = self.v
        if Node.parent is None:
            Node.N+=1
            Node.W+=self.v
            Node.Q=Node.W/Node.N
            return
        
        while Node.parent:
            Node.N += 1
            Node.W += self.v
            Node.Q = Node.W/Node.N
            Node = Node.parent
            v *= self.value_decay
            
    def delete_node(self,node):
        if not node.child:
            return
        for i in node.child:
            self.delete_node(i)
            del i
        del node
        