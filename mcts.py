from node import Node
import numpy as np
from rule import Rule

class MCTS:
    def __init__(self, board, color, cfg):
        self.board = board.copy()
        self.color = color

        self.node = Node(board, cfg, color)
        self.model_b = None
        self.model_w = None
        self.rule = Rule(cfg)
        self.cfg = cfg

    def simulation(self):
        for epoch in range(self.cfg.NUM_SIMULATION):
            game_board = np.copy(self.board)
            color = self.color
            valid = self.rule.get_action(game_board)

            current_node = self.node

            action = -1
            while not current_node.is_leaf():
                current_node, action = current_node.selection(valid)
                game_board[action//self.cfg.BOARD_SIZE][action%self.cfg.BOARD_SIZE] = color
                color *= -1

                valid[action] = 0
                current_node.N+=1
            
            
            if color == self.cfg.BLACK:
                model = self.model_b
            else:
                model = self.model_w

            if current_node.end:
                current_node.backup(-current_node.value)
                continue

            #p, v = model.predict(game_board)
            #p = p[0]
            p = np.ones((225,))/255
            v = 0
            #current_node.value = v
            current_node.expansion(p)

            done, reward = self.rule.end_check(game_board)  # game result
            if done:
                current_node.end = True
                current_node.value = reward

            current_node.backup(reward)
    
    def rollout(self):
        self.simulation()
        return self.node.get_action()