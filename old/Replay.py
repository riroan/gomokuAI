import numpy as np
from param import *

class Replay:
    def __init__(self):
        # it has tuple which is (s_t, pi_t, z)
        self.s = []
        self.pi = []
        self.z = []
        self.h = []
        self.start = 0
        self.end = 0
    
    def initialize(self):
        self.s = []
        self.pi = []
        self.z = []
        self.h = []
        self.start = 0
        self.end = 0
    
    def add(self, s_t, pi_t, h = -1, z_t = 0):
        self.s.append(s_t)
        self.pi.append(np.array(pi_t).flatten())
        self.z.append(z_t)
        self.h.append(h)
        self.end+=1
        
    def new_game(self):
        self.start = self.end
        self.end = self.start
        
    def data_augmentation(self,s_t,pi_t,z_t=0,h=-1):
        pi_t = np.array(pi_t).reshape((BOARD_SIZE,BOARD_SIZE))
        self.add(s_t,pi_t,h,z_t)
        
        s_aug = np.zeros((BOARD_SIZE,BOARD_SIZE))
        pi_aug = np.zeros((BOARD_SIZE,BOARD_SIZE))
        h_aug = -1
        # 상하반전
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                s_aug[i][j] = s_t[BOARD_SIZE-i-1][j]
                pi_aug[i][j] = pi_t[BOARD_SIZE-i-1][j]
        (row, col) = (h//BOARD_SIZE,h%BOARD_SIZE)
        (row, col) = (BOARD_SIZE - row - 1, col)
        if h != -1:
            h_aug = row * BOARD_SIZE+col
        self.add(s_aug,pi_aug,h_aug,z_t)
        
        # 좌우반전
        s_aug = s_aug.copy()
        pi_aug = pi_aug.copy()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                s_aug[i][j] = s_t[i][BOARD_SIZE-j-1]
                pi_aug[i][j] = pi_t[i][BOARD_SIZE-j-1]
        (row, col) = (h//BOARD_SIZE,h%BOARD_SIZE)
        (row, col) = (row, BOARD_SIZE-col-1)
        if h != -1:
            h_aug = row * BOARD_SIZE+col
        self.add(s_aug,pi_aug,h_aug,z_t)
        
        # 상하, 좌우반전
        s_aug = s_aug.copy()
        pi_aug = pi_aug.copy()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                s_aug[i][j] = s_t[BOARD_SIZE-i-1][BOARD_SIZE-j-1]
                pi_aug[i][j] = pi_t[BOARD_SIZE-i-1][BOARD_SIZE-j-1]
        (row, col) = (h//BOARD_SIZE,h%BOARD_SIZE)
        (row, col) = (BOARD_SIZE - row - 1, BOARD_SIZE - col - 1)
        if h != -1:
            h_aug = row * BOARD_SIZE+col
        self.add(s_aug,pi_aug,h_aug,z_t)
        
        # 좌상 대각선 대칭
        s_aug = s_aug.copy()
        pi_aug = pi_aug.copy()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                s_aug[i][j] = s_t[j][i]
                pi_aug[i][j] = pi_t[j][i]
        (row, col) = (h//BOARD_SIZE,h%BOARD_SIZE)
        (row, col) = (col, row)
        if h != -1:
            h_aug = row * BOARD_SIZE+col
        self.add(s_aug,pi_aug,h_aug,z_t)
        
        # 좌로 90도 회전
        s_aug = s_aug.copy()
        pi_aug = pi_aug.copy()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                s_aug[i][j] = s_t[BOARD_SIZE-j-1][i]
                pi_aug[i][j] = pi_t[BOARD_SIZE-j-1][i]
        (row, col) = (h//BOARD_SIZE,h%BOARD_SIZE)
        (row, col) = (BOARD_SIZE - col - 1, row)
        if h != -1:
            h_aug = row * BOARD_SIZE+col
        self.add(s_aug,pi_aug,h_aug,z_t)
        
        # 우로 90도 회전
        s_aug = s_aug.copy()
        pi_aug = pi_aug.copy()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                s_aug[i][j] = s_t[j][BOARD_SIZE-1-i]
                pi_aug[i][j] = pi_t[j][BOARD_SIZE-1-i]
        (row, col) = (h//BOARD_SIZE,h%BOARD_SIZE)
        (row, col) = (col, BOARD_SIZE-row-1)
        if h != -1:
            h_aug = row * BOARD_SIZE+col
        self.add(s_aug,pi_aug,h_aug,z_t)
        
        # 우로 90도 회전 후 대칭
        s_aug = s_aug.copy()
        pi_aug = pi_aug.copy()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                s_aug[i][j] = s_t[BOARD_SIZE-1-j][BOARD_SIZE-1-i]
                pi_aug[i][j] = pi_t[BOARD_SIZE-1-j][BOARD_SIZE-1-i]
        (row, col) = (h//BOARD_SIZE,h%BOARD_SIZE)
        (row, col) = (BOARD_SIZE - col - 1, BOARD_SIZE-row-1)
        if h != -1:
            h_aug = row * BOARD_SIZE+col
        self.add(s_aug,pi_aug,h_aug,z_t)