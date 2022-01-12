import numpy as np

class Game:
    def __init__(self, cfg, rule):
        self.cfg = cfg
        self.board = np.zeros((self.cfg.BOARD_SIZE, self.cfg.BOARD_SIZE))
        self.rule = rule
    
    def action(self, act, color):
        x,y = act//self.cfg.BOARD_SIZE, act%self.cfg.BOARD_SIZE
        if self.board[x][y]:
            return False
        self.board[x][y] = color
        return True

    def check(self):
        pass
        #return self.rule.end_check(...)