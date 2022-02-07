from mcts import MCTS

class Agent:
    def __init__(self, game, board, color, cfg):
        self.color = color
        self.cfg = cfg
        self.game = game
        self.mcts = MCTS(board, self.color, self.cfg)

    def get_action(self, last_action=None):
        return self.mcts.rollout(self.game.board, last_action)