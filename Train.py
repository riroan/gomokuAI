# 문제점 : 게임이 끝났는데도 불구하고 rollout에 들어가서 68번째줄에서 오류가 난다.   => 해결

# 2019-08-23 11:03 시작
# 2019-08-23 11:47 끝 152회 착수

# 2019-08-23 12:30 시작
# 2019-08-23 12:59 오류

# 2019-08-23 13:33 시작
# 2019-08-23 22:00 no error

from Engine import *
from Tree import *
from Replay import *
from param import *
import numpy as np
import os
import time

print('hello alphagomoku')

#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#board = np.zeros((BOARD_SIZE,BOARD_SIZE),dtype = int)
#player = BLACK

engine_b = Engine(BLACK)
engine_w = Engine(WHITE)
#tree = Tree(player, board)
replay_b = Replay()
replay_w = Replay()

#engine_b.generate_model()
#engine_w.generate_model()
#engine_b.model.summary()
engine_b.load('weights_b3.h5')
engine_w.load('weights_w3.h5')

epoch = 100
print("train start")

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
        s_t, pi_t, h = tree.rollout(engine_b,engine_w)
        
        if player == BLACK:
            replay_b.data_augmentation(s_t, pi_t, h = history)
            #replay_b.add(s_t,pi_t,history)
        else:
            replay_w.data_augmentation(s_t, pi_t, h = history)
            #replay_w.add(s_t,pi_t,history)
        #print(replay_b.end)
        gameOver = tree.check_winner(tree.root_state,player)
        #print(s_t)
        #print(tree.root_state)
        if gameOver:
            winner = player
            break
        history = h
        c+=1
        player = -player
        if c%50 == 10:
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
    #replay_b.new_game()
    #replay_w.new_game()
    
    print(_,'th game elapse',time.time()-start, 'total step : ',c)
    if winner == BLACK:
        print('black win')
    else:
        print('white win')
    #print(time.time()-start)
    engine_b.save_model('weights_b3.h5')
    engine_w.save_model('weights_w3.h5')
    print(board)

print('//==========================================================================//')
print('끝')