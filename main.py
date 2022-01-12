import pygame
import time
from config import Config
from game import Game

pygame.init()
cfg = Config()
LEFT = 1
size = [2*cfg.MARGIN+cfg.SPACE*(cfg.BOARD_SIZE-1),2*cfg.MARGIN+cfg.SPACE*(cfg.BOARD_SIZE-1)+100]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Omok")
sf = pygame.font.SysFont("Arial",15,True)


game = Game(sf)

clock = pygame.time.Clock()

game.draw_board(screen)
s = 1

#while not game.gameOver:
while True:
    clock.tick(cfg.FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT and not game.gameOver:
            action = game.update_board(event.pos)
            game.add_action(action)
            game.update_screen(screen)
            game.check_winner()
            pygame.display.flip()

                
    if game.gameOver and game.winner == cfg.BLACK:
        msg = sf.render('Black player win!',True,(0,0,0))
        screen.blit(msg,(20,630))
        pygame.display.flip()
        break
    elif game.gameOver and game.winner == cfg.WHITE:
        msg = sf.render('White player win!',True,(0,0,0))
        screen.blit(msg,(20,630))
        pygame.display.flip()
        break
    pygame.display.flip()

time.sleep(30)
pygame.quit()