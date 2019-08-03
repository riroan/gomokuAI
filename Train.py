from Tree import Tree
from Replay import Replay
from Model import Model
from keras.model import load_model
from param import *

# if you don't have file
model = Model()
#else
#model = load_model('model.h5')
new_board = np.zeros((BOARD_SIZE,BOARD_SIZE))
player = BLACK

Tree = Tree(player, new_board)
