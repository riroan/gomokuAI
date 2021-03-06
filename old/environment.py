import numpy as np
import pygame
from param import *

class env:
    def __init__(self, font):
        self.board = np.zeros((BOARD_SIZE,BOARD_SIZE))
        self.player = BLACK
        self.gameOver = False
        self.winner = NONE
        self.actions = []
        self.sf = font

    def draw_board(self,screen):
        screen.fill(WHITE_COLOR)

        pygame.draw.rect(screen,BOARD_COLOR,[OUT_MARGIN,OUT_MARGIN,2*IN_MARGIN+SPACE*(BOARD_SIZE-1),2*IN_MARGIN+SPACE*(BOARD_SIZE-1)])
        for i in range(BOARD_SIZE):
            pygame.draw.line(screen,BLACK_COLOR,[MARGIN+i*SPACE,MARGIN],[MARGIN+i*SPACE,MARGIN+SPACE*(BOARD_SIZE-1)])
            pygame.draw.line(screen,BLACK_COLOR,[MARGIN,MARGIN+i*SPACE],[MARGIN+SPACE*(BOARD_SIZE-1),MARGIN+i*SPACE])

    def update_screen(self,screen):
        '''for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == BLACK:
                    pygame.draw.circle(screen,BLACK,[MARGIN + j*SPACE,MARGIN + i*SPACE],STONE_SIZE)
                elif self.board[i][j] == WHITE:
                    pygame.draw.circle(screen,WHITE,[MARGIN + j*SPACE,MARGIN + i*SPACE],STONE_SIZE)'''
        for ix, action in enumerate(self.actions):
            i,j = getAction(action)
            if ix%2==0:
                text = self.sf.render(str(ix),True,(255,255,255))
                pygame.draw.circle(screen,BLACK,[MARGIN + j*SPACE,MARGIN + i*SPACE],STONE_SIZE)
            else:
                text = self.sf.render(str(ix),True,(0,0,0))
                pygame.draw.circle(screen,WHITE,[MARGIN + j*SPACE,MARGIN + i*SPACE],STONE_SIZE)
                
            if ix < 10:
                screen.blit(text,(MARGIN + j*SPACE - 3,MARGIN + i*SPACE - 3))
            else:
                screen.blit(text,(MARGIN + j*SPACE - 6,MARGIN + i*SPACE - 3))
                
                    
    # get click event
    def update_board(self,pos):
        if not (pos[0] > 35 and pos[1] > 35 and pos[0] < 605 and pos[1] < 605):
            return
        if self.board[(pos[1]+15-MARGIN)//SPACE][(pos[0]+15-MARGIN)//SPACE] != NONE:
            return
        self.board[(pos[1]+15-MARGIN)//SPACE][(pos[0]+15-MARGIN)//SPACE] = self.player
        self.check_winner()
        self.player *= WHITE
        return (pos[1]+15-MARGIN)//SPACE * BOARD_SIZE + (pos[0]+15-MARGIN) // SPACE
    
    def add_action(self, action):
        self.actions.append(action)
        
    def check_winner(self):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                match = 0
                for i in range(STONE_MAX):
                    if x+i>=BOARD_SIZE:
                        break
                    if self.board[y][x+i] == self.player:
                        match+=1
                    else:
                        break
                    if match >= STONE_MAX:
                        self.gameOver = True
                        self.winner = self.player
                        return
                    
                match = 0
                for i in range(STONE_MAX):
                    if y+i>=BOARD_SIZE:
                        break
                    if self.board[y+i][x] == self.player:
                        match+=1
                    else:
                        break
                    if match >= STONE_MAX:
                        self.gameOver = True
                        self.winner = self.player                        
                        return
                    
                match = 0
                for i in range(STONE_MAX):
                    if x+i>=BOARD_SIZE or y+i>=BOARD_SIZE:
                        break
                    if self.board[y+i][x+i] == self.player:
                        match+=1
                    else:
                        break
                    if match >= STONE_MAX:
                        self.gameOver = True
                        self.winner = self.player                        
                        return
                    
                match = 0
                for i in range(STONE_MAX):
                    if x-i<0 or y+i>=BOARD_SIZE:
                        break
                    if self.board[y+i][x-i] == self.player:
                        match+=1
                    else:
                        break
                    if match >= STONE_MAX:
                        self.gameOver = True
                        self.winner = self.player                        
                        return