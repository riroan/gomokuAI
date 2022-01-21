class Replay:
    def __init__(self, cfg):
        # replays: 두기전 오목판, 이번에 착수할 돌 색깔, 행동, 가치, 마지막으로 둔 돌의 위치
        self.replays = []
        self.cfg = cfg
        # self.maxlen = cfg.maxlen

    def put_replay(self, re):
        self.replays.append(re)

    def remove_replay(self):
        # if len(self.replays) > self.maxlen:
        del self.replays[0]

    def clear(self):
        self.replays = []

    def update_replay(self):
        l = len(self.replays)
        if self.replays[l-1][3] != 0:  # 게임이 끝났다면 앞에 있는 리플레이들의 value도 업데이트
            for i in range(l-1):
                self.replays[i][3] = self.replays[l-1][3]

