from utils import index2coordinate
import numpy as np
from replay import Replay


class Rule:
    def __init__(self, board, cfg):
        self.cfg = cfg
        self.board = board
        # result : string -> reward, done
        self.reward = 0
        self.done = False
        self.replays = Replay()  # append.replay : [두기전 오목 판, 다음에 놓을 돌 색, 행동, 가치]
        

    # def move(self, color):
    #     # action = ...
    #     # value = ...
    #     self.replays.replays.append([self.board, color, action, value])

    #     act = index2coordinate(action, BOARD_SIZE)
    #     self.board[act[0]][act[1]] = color

    #     self.end_check(action, color)
    #     return self.reward, self.done

    def get_action(self):
        board = np.ravel(self.board)
        observation = []
        for i in range(self.cfg.BOARD_SIZE * self.cfg.BOARD_SIZE):
            if board[i] == 0:
                observation.append(i)
        return observation

    def get_nextColor(self, color):
        return color * -1

    def count_consecutive(self, i, j, i_direction, j_direction, color):
        count = 0
        for step in range(1, 5):
            if i + step * i_direction < 0 or i + step * i_direction > self.cfg.BOARD_SIZE - 1 or j + step * j_direction < 0 or j + step * j_direction > self.cfg.BOARD_SIZE - 1:
                break
            if self.board[i + step * i_direction][j + step * j_direction] == color:
                count += 1
            else:
                break
        return count

    def end_check(self, action, color):
        act = index2coordinate(action, self.cfg.BOARD_SIZE)
        direction = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, 1], [1, -1]]
        counts = []
        for d in direction:
            count = 1
            count += self.count_consecutive(act[0], act[1], d[0], d[1], color)
            counts.append(count)

        if max(counts) >= 5:
            self.done = True
            self.reward = color
            return

        # 보드에 빈 공간이 없을 때 비긴 상태가 된다.
        observation = self.get_action()
        if len(observation) == 0:
            self.done = True
            self.reward = 0
        return