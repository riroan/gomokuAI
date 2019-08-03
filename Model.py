from keras import layers
from keras import Input
from keras.models import Model
from keras import regularizers
from param import *

def generate_model():
    board_input = Input(shape=(BOARD_SIZE,BOARD_SIZE,3),dtype = 'float32',name = 'input')

    x = layers.Conv2D(32,(3,3),strides = (1,1), kernel_regularizer=regularizers.l2(0.001))(board_input)
    x = layers.BatchNormalization()(x)
    x = layers.Activation('relu')(x)
    x = layers.Conv2D(32,(3,3),strides = (1,1), kernel_regularizer=regularizers.l2(0.001))(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation('relu')(x)
    x = layers.Conv2D(32,(3,3),strides = (1,1), kernel_regularizer=regularizers.l2(0.001))(x)
    x = layers.BatchNormalization()(x)
    short_cut = x
    x = layers.Activation('relu')(x)
    x = layers.Conv2D(32,(3,3),strides = (1,1),padding = 'same', kernel_regularizer=regularizers.l2(0.001))(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation('relu')(x)
    x = layers.Conv2D(32,(3,3),strides = (1,1),padding = 'same', kernel_regularizer=regularizers.l2(0.001))(x)
    x = layers.BatchNormalization()(x)
    x = layers.add([short_cut,x])
    x = layers.Activation('relu')(x)

    value = layers.Conv2D(1,(1,1),strides = (1,1), kernel_regularizer=regularizers.l2(0.001))(x)
    value = layers.BatchNormalization()(value)
    value = layers.Activation('relu')(value)
    value = layers.Flatten()(value)
    value = layers.Dense(32, activation = 'relu', kernel_regularizer=regularizers.l2(0.001))(value)
    value = layers.Dense(1,activation = 'tanh', name = 'value', kernel_regularizer=regularizers.l2(0.001))(value)

    policy = layers.Conv2D(2,(1,1),strides = (1,1), kernel_regularizer=regularizers.l2(0.001))(x)
    policy = layers.BatchNormalization()(policy)
    policy = layers.Activation('relu')(policy)
    policy = layers.Flatten()(policy)
    policy = layers.Dense(BOARD_SIZE*BOARD_SIZE,activation = 'softmax', name = 'policy', kernel_regularizer=regularizers.l2(0.001))(policy)

    model = Model(board_input,[value,policy])
    model.compile(optimizer = 'rmsprop',loss = ['mse', 'categorical_crossentropy'])
    
    return model