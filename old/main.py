from Game import Game
from Node import Node
import numpy as np

game = Game(15)

while not game.gameOver:
    if game.player == 1:
        #while action not in game.getAbleAction():
            #action = int(input("your action? "))
        action = 0
        game.doAction(action)
        print()
        print(np.array(game.board))
    else:
        node = Node(game.getState(), -game.player)
        action = node.getAction()
        game.doAction(action)
        print()
        print(np.array(game.board))
        assert 0


