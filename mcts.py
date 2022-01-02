from node import Node
from config import *
import numpy as np

class MCTS:
    def __init__(self, board, color):
        self.board = board.copy()
        self.color = color

        self.node = Node(board, color)
        self.model_b = None
        self.model_w = None

    def simulation(self):
        for epoch in range(NUM_SIMULATION):
            game_board = np.copy(self.board)
            color = self.color
            #valid = get_valid_action(game_board)
            valid = []

            current_node = self.node


            action = -1
            while not current_node.is_leaf():
                current_node, action = current_node.selection(valid)
                game_board[action//BOARD_SIZE][action%BOARD_SIZE] = color
                color *= -1

                valid[action] = 0
                current_node.N+=1
            
            if color == BLACK:
                model = self.model_b
            else:
                model = self.model_w

            if current_node.end:
                current_node.backup(-current_node.value)
                continue

            p, v = model.predict(game_board)
            p = p[0]
            current_node.value = v
            current_node.expansion(p)

            # result = check(game_board)  # game result
            result = None
            if result in ['black_win', 'white_win', 'full']:
                current_node.end = True
                if result == 'full':
                    current_node.value = 0
                else:
                    current_node.value = -1

            current_node.backup(v)
    
    def rollout(self):
        self.simulation()
        return self.node.get_action()