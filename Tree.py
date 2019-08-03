from Node import Node
from param import *
import numpy as np
import random

epsilon = 0.1

class Tree:
    # player is who will put dol next time
    def __init__(self, player, root_state):
        self.player = player
        self.Node = Node()    # root node
        self.root_state = np.array(root_state).flatten()
        self.rollout_count = 0
        
    def rollout(self):
        for i in range(EPOCH):
            valid_vector = [1 if i == NONE else 0 for i in self.root_state]

            Node = self.Node

            current_board = self.root_state.copy()
            player = self.player

            while Node.child:
                Node, action = Node.selection(valid_vector)

                valid_vector[action] = 0
                player = -player
                current_board[getAction(action)] = player

            # now Node is leaf node
            if check_winner(current_board, player):
                Node.Over = True

            if Node.Over:
                Node.backup()
                continue
                
            # get vector p and scalar v from network
            # p, Node.v = model.predict(current_board)            <-- do it!
            Node.expansion(p)
            Node.backup()
        
        pi_t = np.array([i.P for i in self.Node.child])
        if rollout_count >= 30:
            pi_t = pi_t ** (1/epsilon)
        pi_t_sum = np.sum(pi_t)
        pi_t = pi_t / pi_t_sum
        
        s_t = self.root_state.copy()
        
        return s_t, pi_t
        
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