import numpy as np
SPACE = 30
STONE_SIZE = 15
IN_MARGIN = 20
OUT_MARGIN = 30
MARGIN = IN_MARGIN+OUT_MARGIN
BLACK_COLOR = (  0,  0,  0)
WHITE_COLOR = (255,255,255)
BOARD_COLOR = (252,191,146)
FPS = 10
BOARD_SIZE = 19
STONE_MAX = 5
NONE = 0
BLACK = 1
WHITE = -1
EPOCH = 3000

def getAction(action):
    return action//BOARD_SIZE, action%BOARD_SIZE

def state2input(state, player):
    ret1 = []
    ret2 = []
    ret3 = np.full((BOARD_SIZE,BOARD_SIZE),player)
    for i in range(BOARD_SIZE):
        ret1.append(1 if state[i,j] == BLACK else 0 for j in range(BOARD_SIZE))
        ret2.append(1 if state[i,j] == WHITE else 0 for j in range(BOARD_SIZE))
    ret1 = np.array(ret1)
    ret2 = np.array(ret2)
    ret = np.vstack((ret1,ret2,ret3))
    return ret.reshape((3,BOARD_SIZE,BOARD_SIZE))
    