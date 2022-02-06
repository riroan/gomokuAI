from mcts import MCTS

class Agent:
    def __init__(self, board, color, cfg):
        self.color = color
        self.cfg = cfg
        self.mcts = MCTS(board, self.color, self.cfg)

    def get_action(self, last_action=None):
        if last_action is not None:
            self.mcts.node = self.mcts.node.children[last_action]
        return self.mcts.rollout()