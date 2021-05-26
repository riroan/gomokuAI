import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from Engine import *
from Tree import *
from Replay import *
from param import *
import numpy as np

import time


from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

print('hello alphagomoku')

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#board = np.zeros((BOARD_SIZE,BOARD_SIZE),dtype = int)
#player = BLACK

engine_b = Engine(BLACK)
engine_w = Engine(WHITE)
#tree = Tree(player, board)
replay_b = Replay()
replay_w = Replay()

engine_b.generate_model()
engine_w.generate_model()
engine_b.model.summary()

engine_b.load('weights_b2.h5')
engine_w.load('weights_w2.h5')

epoch = 10000
print("train start")

b_cnt = 0
w_cnt = 0

for _ in range(epoch):
    board = np.zeros((BOARD_SIZE,BOARD_SIZE),dtype = int)
    player = BLACK
    tree = Tree(player,board)
    
    start = time.time()
    gameOver = False
    winner = NONE
    start = time.time()
    history = -1
    c = 0
    while not gameOver:
        #print(c)
        s_t, pi_t, h = tree.rollout(engine_b,engine_w)
        
        if player == BLACK:
            replay_b.data_augmentation(s_t, pi_t, h = history)
            #replay_b.add(s_t,pi_t,history)
        else:
            replay_w.data_augmentation(s_t, pi_t, h = history)
            #replay_w.add(s_t,pi_t,history)
        gameOver = tree.check_winner(tree.root_state,player)
        if gameOver:
            winner = player
            break
        history = h
        c+=1
        player = -player
        if c%10 == 0:
            print('Epoch : ',_,' step : ',c,' time : ', time.time()-start)
    
    for i in range(replay_b.end - replay_b.start):
        if winner == BLACK:
            replay_b.z[i] = 1
        else:
            replay_b.z[i] = -1
    for i in range(replay_w.end - replay_w.start):
        if winner == BLACK:
            replay_w.z[i] = -1
        else:
            replay_w.z[i] = 1
    
    engine_b.train2(replay_b)
    engine_w.train2(replay_w)
    
    replay_b.initialize()
    replay_w.initialize()
    
    print(_,'th game elapse',time.time()-start, 'total step : ',c)
    if winner == BLACK:
        b_cnt+=1
        print('black win')
    else:
        w_cnt+=1
        print('white win')
    print("black : "+str(b_cnt)+" vs white : "+str(w_cnt))
    print("win rate(black) : "+str(b_cnt/(_ + 1))+", win rate(white) : "+str(w_cnt/(_+1)))
    engine_b.save_model('weights_b2.h5')
    engine_w.save_model('weights_w2.h5')
    print(board)
    f = open("1.txt","w")
    f.write(str(_))
    f.close()

print('//==========================================================================//')
print('끝')
