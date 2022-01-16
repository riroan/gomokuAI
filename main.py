import pygame
import time
from config import Config
from game import Game
from renderer import Renderer
from rule import Rule


# init configuration
done = False
cfg = Config()
rule = Rule(cfg)
game = Game(cfg, rule)

# init pygame
pygame.init()
screen = pygame.display.set_mode(cfg.size)
sf = pygame.font.SysFont("Arial",15,True)
clock = pygame.time.Clock()
pygame.display.set_caption("Omok")
renderer = Renderer(sf, cfg)

renderer.render_base(screen)
while not game.over:
    clock.tick(cfg.FPS)
    
    # get mouse click event
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and event.button == cfg.LEFT:
            action = renderer.get_action(event.pos)
            if game.action(action):
                renderer.render_dol(screen, action, -game.color, game.num)
                done, player = rule.end_check(game.board)

    pygame.display.flip()

time.sleep(30)
pygame.quit()