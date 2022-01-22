from keras.engine.topology import Input
from keras.engine.training import Model
from keras.layers import add
from keras.layers.convolutional import Conv2D
from keras.layers.core import Activation, Dense, Flatten
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l2
from keras.optimizers import SGD
import numpy as np

class RL_player:

    def __init__(self, cfg):
        self.name = "RL_player"
        self.model = self.make_network()
        self.cfg = cfg

    def make_network(self):
        board_input = Input((3, self.cfg.BOARD_SIZE, self.cfg.BOARD_SIZE))
        residual_model = board_input

        residual_model = Conv2D(filters=32, kernel_size=(3, 3), strides=(1, 1), padding="same",
                                data_format="channels_first", kernel_regularizer=l2(self.cfg.coef))(residual_model)
        residual_model = BatchNormalization()(residual_model)
        residual_model = Activation("relu")(residual_model)

        for _ in range(2):
            residual_model = self.residual_block(residual_model)

        # policy head
        policy_model = Conv2D(filters=2, kernel_size=(1, 1), strides=(1, 1), padding="same",
                              data_format="channels_first", kernel_regularizer=l2(self.cfg.coef))(residual_model)
        policy_model = BatchNormalization()(policy_model)
        policy_model = Activation("relu")(policy_model)
        policy_model = Flatten()(policy_model)
        policy_model = Dense(self.cfg.BOARD_SIZE*self.cfg.BOARD_SIZE, kernel_regularizer=l2(self.cfg.coef))(policy_model)
        policy_model = Activation("softmax")(policy_model)

        # value head
        value_model = Conv2D(filters=1, kernel_size=(1, 1), strides=(1, 1), padding="same",
                             data_format="channels_first", kernel_regularizer=l2(self.cfg.coef))(residual_model)
        value_model = BatchNormalization()(value_model)
        value_model = Activation("relu")(value_model)
        value_model = Flatten()(value_model)
        value_model = Dense(32, kernel_regularizer=l2(self.cfg.coef))(value_model)
        value_model = Activation("relu")(value_model)
        value_model = Dense(1, kernel_regularizer=l2(self.cfg.coef))(value_model)
        value_model = Activation("tanh")(value_model)

        m = Model(inputs=board_input, outputs=[policy_model, value_model])

        opt = SGD(lr=2e-3, momentum=1e-1, nesterov=True)  # stochastic gradient descend with momentum
        losses_type = ['categorical_crossentropy', 'mean_squared_error']  # cross-entrophy and MSE are weighted equally
        m.compile(optimizer=opt, loss=losses_type)
        return m

    def residual_block(self, x):
        x_shortcut = x
        x = Conv2D(filters=32, kernel_size=(3, 3), padding="same",
                   data_format="channels_first", kernel_regularizer=l2(self.cfg.coef))(x)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)
        x = Conv2D(filters=32, kernel_size=(3, 3), padding="same",
                   data_format="channels_first", kernel_regularizer=l2(self.cfg.coef))(x)
        x = BatchNormalization()(x)
        x = add([x, x_shortcut])
        x = Activation("relu")(x)
        return x

    def save_network(self, name):
        filename = name + "_network.h5"
        self.network.save(filename)
        self.network.summary()
        print("save network")

    def preprocess(self, replay):
        replays = replay.replays
        current_color = replay[1]  # 이번에 둘 돌 색깔 -> X로 저장(why? X:현재플레이어의 돌, Y:상대플레이어의 돌)
        S = []
        P = []
        V = []
        for re in replays:
            # S preprocess
            S_element = np.zeros([3, 15, 15])
            for i in range(self.cfg.BOARD_SIZE):
                for j in range(self.cfg.BOARD_SIZE):
                    board = re[0]
                    if board[i][j] == current_color:
                        S_element[0][i][j] = current_color  # X 저장
                    if board[i][j] == current_color * -1:
                        S_element[1][i][j] = current_color * -1  # Y 저장

            last_move = re[4]
            xi = last_move[0]
            yi = last_move[1]
            S_element[2][xi][yi] = 1  # L저장

            S.append(S_element)  # S에 추가

            # P preprocess
            action = re[2]
            p_element = np.eye(255)[action]
            P.append(p_element)  # P에 추가

            # V preprocess
            v_element = re[3]
            V.append(v_element)  # V에 추가

        return S, P, V

    def data_split(self, data):
        size = data.shape[0]
        return data[:int(size * self.cfg.split_rate)], data[int(size * self.cfg.split_rate):]

    def train(self, replay):
        # 작동하는지는 모름
        X, P, V = self.preprocess(replay)
        s = np.arange((X.shape[0],))
        np.random.shuffle(s)
        X, P, V = X[s], P[s], V[s] # data shuffle
        X, X_val = self.data_split(X)
        P, P_val = self.data_split(P)
        V, V_val = self.data_split(V)
        self.model.fit(X, (P, V), epochs = self.cfg.TRAIN_EPOCH, batch_size = self.cfg.BATCH_SIZE, validation_data=(X_val, (P_val, V_val)))
