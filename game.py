import numpy as np

class Game:
    def __init__(self, cfg, rule):
        self.cfg = cfg
        self.rule = rule

        self.color = cfg.BLACK
        self.board = np.zeros((self.cfg.BOARD_SIZE, self.cfg.BOARD_SIZE))
        self.over = False
        self.num = 0
    
    def action(self, act):
        x,y = act//self.cfg.BOARD_SIZE, act%self.cfg.BOARD_SIZE
        if self.board[x][y]:
            return False
        self.board[x][y] = self.color

        self.num += 1
        self.color *= -1
        return True