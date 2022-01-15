from utils import index2coordinate
import numpy as np
from replay import Replay


class Rule:
    def __init__(self, cfg):
        self.cfg = cfg
        self.reward = 0
        self.done = False

    # def move(self, color):  # 지우기
    #     # action = ...
    #     # value = ...
    #     self.replays.replays.append([self.board, color, action, value])

    #     act = index2coordinate(action, BOARD_SIZE)
    #     self.board[act[0]][act[1]] = color

    #     self.end_check(action, color)
    #     return self.reward, self.done

    def get_action(self, board):
        f_board = np.ravel(board)
        observation = []
        for i in range(self.cfg.BOARD_SIZE * self.cfg.BOARD_SIZE):
            if f_board[i] == 0:
                observation.append(i)
        return observation

    def get_nextColor(self, board):  # board -> 다음 둘 돌의 색깔 리턴
        cnt = 0
        f_board = np.ravel(board)
        for i in range(self.cfg.BOARD_SIZE * self.cfg.BOARD_SIZE):
            if f_board[i] != 0:
                cnt += 1

        if cnt % 2 == 0:
            return self.cfg.BLACK
        return self.cfg.WHITE

    def end_check(self, board):  # 수정 가운데 돌 놓았을 때 판정 필요-> 브르투포스 + 보드 인풋 받아서, -> 리턴으로 done, reward 할 수 있게
        color = self.get_nextColor(board) * (-1)  # 마지막으로 둔 돌의 색

        counts = []
        # 가로줄 체크
        for i in range(self.cfg.BOARD_SIZE):
            for j in range(self.cfg.BOARD_SIZE - 4):
                if board[i][j] != 0 and board[i][j] == board[i][j+1] and board[i][j] == board[i][j+2] and board[i][j] == board[i][j+3] and board[i][j] == board[i][j+4]:
                    self.done = True
                    self.reward = color
                    return self.done, self.reward

        # 세로줄 체크
        for i in range(self.cfg.BOARD_SIZE - 4):
            for j in range(self.cfg.BOARD_SIZE):
                if board[i][j] != 0 and board[i][j] == board[i+1][j] and board[i][j] == board[i+2][j] and board[i][j] == board[i+3][j] and board[i][j] == board[i+4][j]:
                    self.done = True
                    self.reward = color
                    return self.done, self.reward

        # 우상향 대각선
        for i in range(self.cfg.BOARD_SIZE - 4):
            for j in range(4, self.cfg.BOARD_SIZE):
                if board[i][j] != 0 and board[i][j] == board[i+1][j-1] and board[i][j] == board[i+2][j-2] and board[i][j] == board[i+3][j-3] and board[i][j] == board[i+4][j-4]:
                    self.done = True
                    self.reward = color
                    return self.done, self.reward

        # 우하향 대각선
        for i in range(self.cfg.BOARD_SIZE - 4):
            for j in range(self.cfg.BOARD_SIZE - 4):
                if board[i][j] != 0 and board[i][j] == board[i+1][j+1] and board[i][j] == board[i+2][j+2] and board[i][j] == board[i+3][j+3] and board[i][j] == board[i+4][j+4]:
                    self.done = True
                    self.reward = color
                    return self.done, self.reward

        # 보드에 빈 공간이 없을 때 비긴 상태가 된다.
        observation = self.get_action(board)
        if len(observation) == 0:
            self.done = True
            self.reward = 0
        return self.done, self.reward
