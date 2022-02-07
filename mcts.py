from config import Config
from node import Node
import numpy as np
from rule import Rule
from network import RL_player

class MCTS:
    def __init__(self, board, color, cfg):
        self.board = board.copy()
        self.color = color

        self.node = Node(board, cfg, color)
        self.model_b = RL_player(cfg)
        self.model_b.model.load_weights("model_b_15.h5")
        self.model_w = RL_player(cfg)
        self.model_w.model.load_weights("model_w_15.h5")
        self.rule = Rule(cfg)
        self.cfg:Config = cfg

    def simulation(self, board, last_action):
        legal_vec_root = self.rule.get_action(board)
        for epoch in range(self.cfg.NUM_SIMULATION):
            current_node = self.node
            current_color = self.node.color
            
            legal_vec_current = np.copy(legal_vec_root)
            current_board = np.copy(board)
            select_action = last_action
            
            while not current_node.is_leaf():
                current_node, action_ix = current_node.selection(legal_vec_current)
                legal_vec_current[action_ix] = 0
                
                row, col = self.cfg.index2coordinate(action_ix)
                current_board[row][col] = current_color
                select_action = action_ix
                
                current_color = -current_color
                
            if current_node.end:
                current_node.backup(-current_node.value)
                continue
            
            if current_color == self.cfg.BLACK:
                net = self.model_b
            else:
                net = self.model_w
                
            data = net.board_preprocessing(current_board, select_action)
            data = np.expand_dims(data, axis = 0)
            print(data)
            p, v = net.predict(data)
            current_node.value = v
            prior_prob = p[0]
            if select_action is not None:
                end_flag, reward = self.rule.end_check(current_board)
                if end_flag:
                    current_node.end = True
                    if reward == 0:
                        current_node.value = 0
                    else:
                        current_node.value = -1
                else:
                    current_node.expansion(prior_prob)
            else:
                current_node.expansion(prior_prob)
            
            current_node.backup(-current_node.value)
            
    def predict(self, board, last_action):
        self.simulation(board, last_action)
        original_pi = np.array([node.N for node in self.node.children])
        try:
            pi = np.array([node.N ** (1/self.cfg.tau) for node in self.node.children])
        except:
            pi = original_pi
            
        original_pi /= sum(original_pi)
        pi/=sum(pi)
        
        return original_pi, pi
            
    def get_action(self, board, last_action):
        if self.node.is_leaf():
            last_board = np.copy(board)
            if last_action is not None:
                row, col = last_action[0], last_action[1]
                last_board[row][col] = 0
            self.simulation(last_board, last_action)
        
        if last_action is not None:
            last_action_ind = self.cfg.coordinate2index(last_action)
            self.node = self.node.children[last_action_ind]
        
        original_pi, pi = self.predict(board, last_action)
        
        position_list = [i for i in range(self.cfg.BOARD_SIZE**2)]
        action = np.random.choice(position_list)
        
        next_node = self.node.children[action]
        prior_prob = next_node.P
        value = next_node.value
            
        return action, original_pi, prior_prob, value
    
    def rollout(self, board, last_action):
        self.simulation(board, last_action)
        action, original_pi, prior_prob, value = self.get_action(board, last_action)
        return action