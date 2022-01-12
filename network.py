from keras.engine.topology import Input
from keras.engine.training import Model
from keras.layers import add
from keras.layers.convolutional import Conv2D
from keras.layers.core import Activation, Dense, Flatten
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l2
from keras.optimizers import SGD


class RL_player:

    def __init__(self):
        self.name = "RL_player"
        self.network = self.make_network()

    def make_network(self):
        board_input = Input((3, 15, 15))
        residual_model = board_input

        residual_model = Conv2D(filters=32, kernel_size=(3, 3), strides=(1, 1), padding="same",
                                data_format="channels_first", kernel_regularizer=l2(1e-4))(residual_model)
        residual_model = BatchNormalization()(residual_model)
        residual_model = Activation("relu")(residual_model)

        for _ in range(2):
            residual_model = self.residual_block(residual_model)

        # policy head
        policy_model = Conv2D(filters=2, kernel_size=(1, 1), strides=(1, 1), padding="same",
                              data_format="channels_first", kernel_regularizer=l2(1e-4))(residual_model)
        policy_model = BatchNormalization()(policy_model)
        policy_model = Activation("relu")(policy_model)
        policy_model = Flatten()(policy_model)
        policy_model = Dense(15 * 15, kernel_regularizer=l2(1e-4))(policy_model)
        policy_model = Activation("softmax")(policy_model)

        # value head
        value_model = Conv2D(filters=1, kernel_size=(1, 1), strides=(1, 1), padding="same",
                             data_format="channels_first", kernel_regularizer=l2(1e-4))(residual_model)
        value_model = BatchNormalization()(value_model)
        value_model = Activation("relu")(value_model)
        value_model = Flatten()(value_model)
        value_model = Dense(32, kernel_regularizer=l2(1e-4))(value_model)
        value_model = Activation("relu")(value_model)
        value_model = Dense(1, kernel_regularizer=l2(1e-4))(value_model)
        value_model = Activation("tanh")(value_model)

        m = Model(inputs=board_input, outputs=[policy_model, value_model])

        opt = SGD(lr=2e-3, momentum=1e-1, nesterov=True)  # stochastic gradient descend with momentum
        losses_type = ['categorical_crossentropy', 'mean_squared_error']  # cross-entrophy and MSE are weighted equally
        m.compile(optimizer=opt, loss=losses_type)
        return m

    def residual_block(self, x):
        x_shortcut = x
        x = Conv2D(filters=32, kernel_size=(3, 3), strides=(1, 1), padding="same",
                   data_format="channels_first", kernel_regularizer=l2(1e-4))(x)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)
        x = Conv2D(filters=32, kernel_size=(3, 3), strides=(1, 1), padding="same",
                   data_format="channels_first", kernel_regularizer=l2(1e-4))(x)
        x = BatchNormalization()(x)
        x = add([x, x_shortcut])
        x = Activation("relu")(x)
        return x

    def save_network(self, name):
        filename = name + "_network.h5"
        self.network.save(filename)
        self.network.summary()
        print("save network")


#p1_RL = RL_player()
#p1_RL.save_network("p1_RL_220101")
