# from keras.engine.topology import Input
# from keras.engine.training import Model
# from keras.layers import add
# from keras.layers.convolutional import Conv2D
# from keras.layers.core import Activation, Dense, Flatten
# from keras.layers.normalization import BatchNormalization

from keras.layers import Input, Add, Conv2D, Activation, Dense, Flatten, BatchNormalization
from keras.models import Model
from keras.regularizers import l2
# from keras.optimizers import SGD
import numpy as np
from keras.models import load_model
from replay import ReplayData

class RL_player:

    def __init__(self, cfg):
        self.name = "RL_player"
        self.cfg = cfg

        self.model = self.make_network()

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

        # opt = SGD(lr=2e-3, momentum=1e-1, nesterov=True)  # stochastic gradient descend with momentum
        losses_type = ['categorical_crossentropy', 'mean_squared_error']  # cross-entrophy and MSE are weighted equally
        m.compile(optimizer="rmsprop", loss=losses_type)
        return m

    def predict(self, board):
        return self.model.predict(board)

    def residual_block(self, x):
        x_shortcut = x
        x = Conv2D(filters=32, kernel_size=(3, 3), padding="same",
                   data_format="channels_first", kernel_regularizer=l2(self.cfg.coef))(x)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)
        x = Conv2D(filters=32, kernel_size=(3, 3), padding="same",
                   data_format="channels_first", kernel_regularizer=l2(self.cfg.coef))(x)
        x = BatchNormalization()(x)
        x = Add()([x, x_shortcut])
        x = Activation("relu")(x)
        return x

    def save_network(self, name):
        filename = name + "_network.h5"
        self.model.save(filename)
        self.model.summary()
        print("save network")

    def load_network(self, filename):
        self.model = load_model(filename)
        print("load network")

    def board_preprocessing(self, board, last_action):
        # 보드에 놓아진 돌 개수 count
        cnt = 0
        for i in range(self.cfg.BOARD_SIZE):
            for j in range(self.cfg.BOARD_SIZE):
                if board[i][j] != 0:
                    cnt += 1

        # 이번에 둘 돌 색깔 -> X로 저장(why? X:현재플레이어의 돌, Y:상대플레이어의 돌)
        if cnt % 2 == 0:
            current_color = self.cfg.BLACK
        else:
            current_color = self.cfg.WHITE

        # S preprocess
        S_element = np.zeros([3, self.cfg.BOARD_SIZE, self.cfg.BOARD_SIZE])
        for i in range(self.cfg.BOARD_SIZE):
            for j in range(self.cfg.BOARD_SIZE):
                if board[i][j] == current_color:
                    S_element[0][i][j] = current_color  # X 저장
                if board[i][j] == current_color * -1:
                    S_element[1][i][j] = current_color * -1  # Y 저장

        # 첫수가 아닐 때만 L값 저장
        if last_action is not None:
            xi, yi = self.cfg.index2coordinate(last_action)
            S_element[2][xi][yi] = 1  # L저장

        return S_element

    def convert_replay(self, replays):
        conv_replays = []
        # 7가지 방법으로 리플레이를 변환한 후 리턴
        for type in range(7):
            tmp = []
            for re in replays:
                # 변환 후 tmp에 추가
                new_board = self.board_transform(re.board, type)
                new_action = self.action_transform(re.action, type)
                tmp.append(ReplayData(new_board, new_action, re.value))
            
            conv_replays.append(tmp)
        return conv_replays

    def board_transform(self, board, num):
        if num == 0:
            return np.rot90(board, 1)  # 90도 회전

        elif num == 1:
            return np.rot90(board, 2)  # 180도 회전

        elif num == 2:
            return np.rot90(board, 3)  # 270도 회전

        elif num == 3:
            return np.fliplr(board)  # 좌우반전

        elif num == 4:
            return np.rot90(np.fliplr(board), 2)  # 상하반전

        elif num == 5:
            return np.rot90(np.fliplr(board), 1)  # 위로 90도 반전
        else:  # num == 6
            return np.rot90(np.fliplr(board), 3)  # 아래로 90도 반전

    def action_transform(self, action, num):
        x, y = action//self.cfg.BOARD_SIZE, action%self.cfg.BOARD_SIZE

        board = np.zeros((self.cfg.BOARD_SIZE, self.cfg.BOARD_SIZE))
        board[x][y] = 1
        t_board = self.board_transform(board, num)
        temp = np.where(t_board == 1)
        new_action = (temp[0][0], temp[1][0])
        return new_action

    def preprocess(self, replay):
        replays = replay.replays
        S = []
        P = []
        V = []

        self.preprocess_replays(replays, S, P, V)
        converted_replays = self.convert_replay(replays)
        for r in converted_replays:
            self.preprocess_replays(r, S, P, V)

        return np.array(S), np.array(P), np.array(V)
    
    def preprocess_replays(self, replays, S, P, V):
        for k, re in enumerate(replays):
            board = re.board

            # 보드에 놓아진 돌 개수 count
            cnt = 0
            for i in range(self.cfg.BOARD_SIZE):
                for j in range(self.cfg.BOARD_SIZE):
                    if board[i][j] != 0:
                        cnt += 1

            # 이번에 둘 돌 색깔 -> X로 저장(why? X:현재플레이어의 돌, Y:상대플레이어의 돌)
            if cnt % 2 == 0:
                current_color = self.cfg.BLACK
            else:
                current_color = self.cfg.WHITE

            # S preprocess
            S_element = np.zeros([3, self.cfg.BOARD_SIZE, self.cfg.BOARD_SIZE])
            for i in range(self.cfg.BOARD_SIZE):
                for j in range(self.cfg.BOARD_SIZE):
                    if board[i][j] == current_color:
                        S_element[0][i][j] = current_color  # X 저장
                    if board[i][j] == current_color * -1:
                        S_element[1][i][j] = current_color * -1  # Y 저장

            # 첫 리플레이이면 그냥 빈 칸, 그게 아니면 이전의 action을 last_move로 저장한다.
            if cnt != 0 and k != 0:
                last_move = replays[k-1].action
                xi, yi = self.cfg.index2coordinate(last_move)
                S_element[2][xi][yi] = 1  # L저장

            S.append(S_element)  # S에 추가

            # P preprocess
            action = re.action
            p_element = np.eye(self.cfg.BOARD_SIZE ** 2)[action]
            P.append(p_element)  # P에 추가

            # V preprocess
            v_element = re.value
            V.append(v_element)  # V에 추가

    def data_split(self, data):
        size = data.shape[0]
        return data[:int(size * self.cfg.split_rate)], data[int(size * self.cfg.split_rate):]

    def train(self, replay):
        # 작동하는지는 모름
        X, P, V = self.preprocess(replay)
        s = np.arange(X.shape[0])
        np.random.shuffle(s)
        X, P, V = X[s], P[s], V[s] # data shuffle
        X, X_val = self.data_split(X)
        P, P_val = self.data_split(P)
        V, V_val = self.data_split(V)
        self.model.fit(X, (P, V), epochs = self.cfg.TRAIN_EPOCH, batch_size = self.cfg.BATCH_SIZE, validation_data=(X_val, (P_val, V_val)), verbose = 2)
