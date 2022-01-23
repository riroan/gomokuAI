from config import Config
from game import Game
from rule import Rule
from replay import Replay
from network import RL_player

def self_play_train():
    cfg = Config()
    rule = Rule(cfg)
    replay = Replay(cfg)
    game = Game(cfg, rule, replay)
    network = RL_player(cfg)
    for epoch in range(cfg.SELF_PLAY_EPOCH):
        game.init()
        game.self_play()
        network.train(game.replay)
        if epoch % 100 == 0:
            print(f">> train epoch : {epoch}")

    

if __name__ == "__main__":
    self_play_train()