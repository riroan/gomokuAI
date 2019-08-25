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
EPOCH = 1000

def getAction(action):
    return action//BOARD_SIZE, action%BOARD_SIZE

def state2input(state, color, history = -1):
    state = np.array(state).flatten()
    ret1 = []
    ret2 = []
    ret3 = np.zeros(BOARD_SIZE*BOARD_SIZE)
    if history != -1:
        ret3[history] = 1
    '''for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if state[i,j] == BLACK:
                ret1.append(1)
                ret2.append(0)
            elif state[i,j] == WHITE:
                ret1.append(0)
                ret2.append(1)
            else:
                ret1.append(0)
                ret2.append(0)'''
    ret1 = np.array(state == color, dtype = np.int)
    ret2 = np.array(state == -color, dtype = np.int)
    ret = []
    ret = [[ret1[i],ret2[i],ret3[i]] for i in range(BOARD_SIZE*BOARD_SIZE)]
    #ret = [ret1,ret2,ret3]
    ret = np.array(ret)
    ret = ret.astype('float32')
    #return ret.reshape((3, BOARD_SIZE,BOARD_SIZE))
    return ret.reshape((BOARD_SIZE,BOARD_SIZE,3))