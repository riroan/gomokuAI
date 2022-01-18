from mcts import MCTS

class Agent:
    def __init__(self, color, cfg):
        self.color = color
        self.cfg = cfg

    def get_action(self, board):
        mcts = MCTS(board, self.color, self.cfg)
        return mcts.rollout()