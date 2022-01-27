import pygame
import time
from config import Config
from game import Game
from renderer import Renderer
from rule import Rule
from agent import Agent
from replay import Replay
import sys


def main():
    # init configuration
    done = False
    winner = 0
    cfg = Config()
    rule = Rule(cfg)
    replay = Replay(cfg)
    game = Game(cfg, rule, replay)

    # init pygame
    pygame.init()
    screen = pygame.display.set_mode(cfg.window_size)
    sf = pygame.font.SysFont("Arial",15,True)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Omok")
    renderer = Renderer(sf, cfg)
    renderer.render_base(screen)

    agent = Agent(cfg.BLACK, cfg)

    # main loop
    while not game.over:
        clock.tick(cfg.FPS)
        if game.color == cfg.BLACK:
            action = agent.get_action(game.board)
            if game.action(action):
                renderer.render_dol(screen, action, -game.color, game.num)
                done, winner = rule.end_check(game.board)
                game.over = done

        # get mouse click event
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == cfg.LEFT:
                action = renderer.get_action(event.pos)
                if game.action(action):
                    renderer.render_dol(screen, action, -game.color, game.num)
                    done, winner = rule.end_check(game.board)
                    game.over = done
            if event.type == pygame.QUIT:
                # game.over = done  # 종료버튼 누르면 게임과 상관없이 윈도우창 나가기
                pygame.quit()
                sys.exit()

        pygame.display.flip()

    time.sleep(30)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
