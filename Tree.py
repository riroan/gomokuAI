from Node import Node
from param import *
import random
import time

class Tree:
    # player is who will put dol next time
    def __init__(self, player, root_state, random_policy = True):
        self.player = player
        self.Node = Node()    # root node
        self.root_state = root_state
        self.count = 0
        self.random_policy = random_policy
        
    def rollout(self, engine_b, engine_w):
        '''s_i = self.root_state
        self.root_state[random.randint(0,18)][random.randint(0,18)] = self.player
        self.player = -self.player
        return s_i, s_i, random.randint(0,360)'''
        
        EPOCH = 500
        last_action = -1
        s_t = self.root_state
        pi_t = self.root_state
        is_it =0
        
        for i in range(EPOCH):
            #valid_vector = [1 if i is 0 else 0 for i in self.root_state]
            valid_vector = np.ones(BOARD_SIZE * BOARD_SIZE)
            for j in range(BOARD_SIZE*BOARD_SIZE):
                if self.root_state[getAction(j)] != NONE:
                    valid_vector[j] = 0

            Node = self.Node

            current_board = self.root_state.copy()
            player = self.player
            
            
            # 9e-5
            while Node.child:
                Node, action = Node.selection(valid_vector)

                valid_vector[action] = 0
                player = -player
                current_board[getAction(action)] = player
                last_action = action
            #0.0001
            # now Node is leaf node
            if self.check_winner(current_board, player):
                Node.Over = True
            if Node.Over:
                s_t = self.root_state.copy()
                self.root_state[getAction(last_action)] = player
                pi_t = np.zeros((BOARD_SIZE,BOARD_SIZE))
                pi_t[getAction(last_action)] = 1
                return s_t, pi_t, last_action
            #0.002
            
            # get vector p and scalar v from network
            inputs = np.array([state2input(current_board, player, last_action)])
            if player == BLACK:
                Node.v, p = engine_b.model.predict(inputs)
            else:
                Node.v, p = engine_w.model.predict(inputs)
            # 4s
            p = p[0]
            Node.v = Node.v[0][0]
            Node.expansion(p)
            Node.backup()
            #0.6
        # 0.8 epoch = 10
        # 3.7 epoch = 100
            
        pi_t = self.n2pi()
        # 10s epoch = 400
        s_t = self.root_state.copy()
        if random_policy:
            action = np.random.choice(np.arange(pi_t.size),p=pi_t)
        else:
            action = np.argmax(pi_t)
        #print(pi_t)
        # 56 epoch = 500
        # 48 epoch = 500
        # 42 epoch = 400
        # 13 epoch = 100
        '''while self.root_state[getAction(action)] != NONE:
            temp = pi_t[action]
            temp /= pi_t.size-1
            for i in pi_t:
                i+=temp
            pi_t[action] = 0
            pi_t/=np.sum(pi_t)
            action = np.random.choice(np.arange(pi_t.size),p=pi_t)'''
        self.Node = self.Node.child[action]
        ind = 0
        for i in range(BOARD_SIZE*BOARD_SIZE):
            if self.Node.parent.child[ind] is not self.Node:
                self.Node.delete_node(self.Node.parent.child[ind])
                #self.Node.parent.child[ind].delete_node(self.Node.parent.child[ind])
                #del self.Node.parent.child[ind]
            else:   
                ind = 1
        
        self.root_state[getAction(action)] = self.player
        self.player = -self.player
        del self.Node.parent
        self.Node.parent = None
        self.count+=1
        
        return s_t, pi_t, action
        
    def n2pi(self):
        N = np.array([_.N for _ in self.Node.child])
        tau = 1.0
        if self.count>30:
            tau = 0.05
        N = N ** (1/tau)
        if np.sum(N) !=0:
            pi = N / np.sum(N)
        else:
            pi = N
        return pi
        
    def check_winner(self,board,player):
        BOARD_SIZE = board.shape[0]
        STONE_MAX = 5
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                match = 0
                for i in range(STONE_MAX):
                    if x+i>=BOARD_SIZE:
                        break
                    if board[y][x+i] == player:
                        match+=1
                    else:
                        break
                    if match >= STONE_MAX:
                        return True
                    
                match = 0
                for i in range(STONE_MAX):
                    if y+i>=BOARD_SIZE:
                        break
                    if board[y+i][x] ==player:
                        match+=1
                    else:
                        break
                    if match >= STONE_MAX:                     
                        return True
                    
                match = 0
                for i in range(STONE_MAX):
                    if x+i>=BOARD_SIZE or y+i>=BOARD_SIZE:
                        break
                    if board[y+i][x+i] == player:
                        match+=1
                    else:
                        break
                    if match >= STONE_MAX:                     
                        return True
                    
                match = 0
                for i in range(STONE_MAX):
                    if x-i<0 or y+i>=BOARD_SIZE:
                        break
                    if board[y+i][x-i] == player:
                        match+=1
                    else:
                        break
                    if match >= STONE_MAX:                     
                        return True
        return False