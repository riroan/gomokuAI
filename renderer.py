import pygame

class Renderer:
    def __init__(self, font, cfg):
        self.sf = font
        self.cfg = cfg

    def get_action(self, pos):
        if not (pos[0] > 35 and pos[1] > 35 and pos[0] < 605 and pos[1] < 605):
            return
        return (pos[1]+15-self.cfg.MARGIN)//self.cfg.SPACE * self.cfg.BOARD_SIZE + (pos[0]+15-self.cfg.MARGIN) // self.cfg.SPACE

    def render_base(self, screen):
        screen.fill(self.cfg.WHITE_COLOR)

        pygame.draw.rect(screen,self.cfg.BOARD_COLOR,[self.cfg.OUT_MARGIN,self.cfg.OUT_MARGIN,2*self.cfg.IN_MARGIN+self.cfg.SPACE*(self.cfg.BOARD_SIZE-1),2*self.cfg.IN_MARGIN+self.cfg.SPACE*(self.cfg.BOARD_SIZE-1)])
        for i in range(self.cfg.BOARD_SIZE):
            pygame.draw.line(screen,self.cfg.BLACK_COLOR,[self.cfg.MARGIN+i*self.cfg.SPACE,self.cfg.MARGIN],[self.cfg.MARGIN+i*self.cfg.SPACE,self.cfg.MARGIN+self.cfg.SPACE*(self.cfg.BOARD_SIZE-1)])
            pygame.draw.line(screen,self.cfg.BLACK_COLOR,[self.cfg.MARGIN,self.cfg.MARGIN+i*self.cfg.SPACE],[self.cfg.MARGIN+self.cfg.SPACE*(self.cfg.BOARD_SIZE-1),self.cfg.MARGIN+i*self.cfg.SPACE])
    
    def render_dol(self, screen, action, color):
        x, y = action // self.cfg.BOARD_SIZE, action % self.cfg.BOARD_SIZE
        pygame.draw.circle(screen, color, [self.cfg.MARGIN + y*self.cfg.SPACE,self.cfg.MARGIN + x*self.cfg.SPACE],self.cfg.STONE_SIZE)

