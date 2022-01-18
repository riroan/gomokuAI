import numpy as np
from agent import Agent

class Game:
    def __init__(self, cfg, rule):
        self.cfg = cfg
        self.rule = rule

        self.init()

    def init(self):
        self.color = self.cfg.BLACK
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

    def self_play(self):
        agent_b = Agent(self.cfg.BLACK, self.cfg)
        agent_w = Agent(self.cfg.BLACK, self.cfg)
        while not self.over:
            if self.color == self.cfg.BLACK:
                act = agent_b.get_action(self.board)
            else:
                act = agent_w.get_action(self.board)
            
            if self.action(act):
                done, reward = self.rule.end_check(self.board)
                self.over = done
                print(self.board)
        if reward == self.cfg.BLACK:
            print("black win")
        else:
            print("white win")
