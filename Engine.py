'''from keras.engine.topology import Input
from keras.engine.training import Model
from keras.layers import add
from keras.layers.convolutional import Conv2D
from keras.layers.core import Activation, Dense, Flatten
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l2
from keras.optimizers import SGD'''
from keras import layers
from keras import Input
from keras.models import Model
from keras import regularizers
from keras.models import load_model
import numpy as np
from param import *

class Engine:    
    def __init__(self, color):
        self.inputs = []
        self.targets = []
        self.model = None
        self.color = color
    
    def load(self,filename):
        self.model = load_model(filename)
        print('model loaded',filename)
    
    def generate_model(self):
        board_input = Input(shape=(3,BOARD_SIZE,BOARD_SIZE),dtype = 'float32',name = 'input')
        x=board_input
        residual = layers.Conv2D(32,(1,1),padding = "same", kernel_regularizer=regularizers.l2(0.001),data_format = 'channels_first')(board_input)
        x = layers.Conv2D(32,(3,3),strides = (1,1),padding = "same", kernel_regularizer=regularizers.l2(0.001),data_format = 'channels_first')(board_input)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        x = layers.Conv2D(32,(3,3),strides = (1,1),padding = "same", kernel_regularizer=regularizers.l2(0.001),data_format = 'channels_first')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        x = layers.Conv2D(32,(3,3),strides = (1,1),padding = "same", kernel_regularizer=regularizers.l2(0.001),data_format = 'channels_first')(x)
        x = layers.BatchNormalization()(x)
        x = layers.add([residual,x])
        short_cut = x
        x = layers.Activation('relu')(x)
        x = layers.Conv2D(32,(3,3),strides = (1,1),padding = 'same', kernel_regularizer=regularizers.l2(0.001),data_format = 'channels_first')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        x = layers.Conv2D(32,(3,3),strides = (1,1),padding = 'same', kernel_regularizer=regularizers.l2(0.001),data_format = 'channels_first')(x)
        x = layers.BatchNormalization()(x)
        x = layers.add([short_cut,x])
        x = layers.Activation('relu')(x)

        value = layers.Conv2D(1,(1,1),strides = (1,1),padding = "same", kernel_regularizer=regularizers.l2(0.001),data_format = 'channels_first')(x)
        value = layers.BatchNormalization()(value)
        value = layers.Activation('relu')(value)
        value = layers.Flatten()(value)
        value = layers.Dense(32, activation = 'relu', kernel_regularizer=regularizers.l2(0.001))(value)
        value = layers.Dense(1,activation = 'tanh', name = 'value', kernel_regularizer=regularizers.l2(0.001))(value)

        policy = layers.Conv2D(2,(1,1),strides = (1,1),padding = "same", kernel_regularizer=regularizers.l2(0.001),data_format = 'channels_first')(x)
        policy = layers.BatchNormalization()(policy)
        policy = layers.Activation('relu')(policy)
        policy = layers.Flatten()(policy)
        policy = layers.Dense(BOARD_SIZE*BOARD_SIZE,activation = 'softmax', name = 'policy', kernel_regularizer=regularizers.l2(0.001))(policy)

        self.model = Model(board_input,[value,policy])
        self.model.compile(optimizer = 'rmsprop',loss = ['mse', 'categorical_crossentropy'])
    
    def save_model(self,filename):
        self.model.save(filename)
        print('model saved',filename)
        
    def get_data(self,replay):
        self.inputs = np.array([state2input(replay.s[i],self.color,replay.h[i]) for i in range(replay.end)])
        #self.targets = [np.array(replay.z),np.array(replay.pi)]
        self.targets = np.array([[replay.z[i], np.array(replay.pi[i])] for i in range(replay.end)])
        print(self.targets[0])
        
    def train(self, _batch_size = 32, _epochs = 10):
        self.model.fit(self.inputs,self.targets, batch_size = _batch_size, epochs = _epochs)
        
    def train2(self, replay):
        inputs = np.array([state2input(replay.s[i],self.color,replay.h[i]) for i in range(replay.end)])
        target_z = np.array(replay.z)
        target_pi = np.array(replay.pi)
        self.model.fit(inputs, [target_z,target_pi],batch_size = 64, epochs = 10)
