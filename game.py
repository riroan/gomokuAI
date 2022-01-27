import numpy as np
import time
from agent import Agent

class Game:
    def __init__(self, cfg, rule, replay):
        self.cfg = cfg
        self.rule = rule
        self.replay = replay

        self.init()

    def init(self):
        self.color = self.cfg.BLACK
        self.board = np.zeros((self.cfg.BOARD_SIZE, self.cfg.BOARD_SIZE))
        self.over = False
        self.num = 0
        self.replay.clear()
    
    def action(self, act):
        x,y = act//self.cfg.BOARD_SIZE, act%self.cfg.BOARD_SIZE
        if self.board[x][y]:
            return False
            
        self.replay.put_replay(self.board, act, 0)
        self.board[x][y] = self.color

        self.num += 1
        self.color *= -1
        return True

    def self_play(self):
        agent_b = Agent(self.cfg.BLACK, self.cfg)
        agent_w = Agent(self.cfg.WHITE, self.cfg)
        start = time.time()
        while not self.over:
            if self.color == self.cfg.BLACK:
                act = agent_b.get_action(self.board)
            else:
                act = agent_w.get_action(self.board)
            data = (self.board, act, 0)
            if self.action(act):
                done, reward = self.rule.end_check(self.board)
                self.over = done
        print(self.board)
        if reward == self.cfg.BLACK:
            print(f">> black win, elapsed time : {time.time()-start}, max_turn : {self.num}")
        else:
            print(f">> white win, elapsed time : {time.time()-start}, max_turn : {self.num}")
