from environment import *
from ai import ai
from Tree import Tree
from param import *
from Engine import *
import time

game = env()

pygame.init()

LEFT = 1
size = [2*MARGIN+SPACE*(BOARD_SIZE-1)+500,2*MARGIN+SPACE*(BOARD_SIZE-1)+500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Omok")
sf = pygame.font.SysFont("Monospace",20)

clock = pygame.time.Clock()

game.draw_board(screen)
s = 1

tree = Tree(BLACK,game.board)
engine = Engine(WHITE)
#engine.load('weights_w.h5')

#while not game.gameOver:
while True:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT and not game.gameOver:
            action = game.update_board(event.pos)
            game.update_screen(screen)
            game.check_winner()
            if game.player == WHITE and not game.gameOver:
                #---------------------------------Naive AI----------------------------------
                #engine = ai(game)
                #action = engine.get_action()
                #game.board[action[0]][action[1]] = game.player
                
                
                #----------------------------------MCTS AI----------------------------------
                #engine = Node(game.board,game.player,game.player)
                #action,_ = engine.rollout()
                #text = sf.render(str(_),True,(0,0,0))
                #pygame.draw.rect(screen,(255,255,255),[30,10,400,20])
                #screen.blit(text,(30,10))
                #game.board[action//BOARD_SIZE][action%BOARD_SIZE] = game.player
                
                #----------------------------------better MCTS AI----------------------------------    
                #engine = Node(game.board,game.player,game.player)
                #action = engine.rollout()
                
                #print('=================================')
                #engine.traverse()
                #print('=================================')
                
                #----------------------------------neural network AI-------------------------------
                _,_,action = tree.rollout(engine,engine)
                
                text = sf.render(str(action),True,(0,0,0))
                pygame.draw.rect(screen,(255,255,255),[30,10,400,20])
                screen.blit(text,(30,10))
                game.board[action//BOARD_SIZE][action%BOARD_SIZE] = game.player
                
                game.check_winner()
                game.player = BLACK
                game.update_screen(screen)

                
    if game.gameOver and game.winner == BLACK:
        msg = sf.render('Black player win!',True,(0,0,0))
        screen.blit(msg,(20,630))
        pygame.display.flip()
        break
    elif game.gameOver and game.winner == WHITE:
        msg = sf.render('White player win!',True,(0,0,0))
        screen.blit(msg,(20,630))
        pygame.display.flip()
        break
    pygame.display.flip()

time.sleep(30)
pygame.quit()