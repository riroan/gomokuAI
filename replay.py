from queue import Queue


class Replay:
    def __init__(self, cfg):
        self.replays = Queue()
        self.maxlen = cfg.maxlen

    def append_replay(self, re):
        self.replays.put(re)

    def remove_replay(self):
        if len(self.replays) > self.maxlen:
            self.replays.get()
