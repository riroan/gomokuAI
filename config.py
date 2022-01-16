class Config:
    def __init__(self):
        self.BLACK = 1
        self.WHITE = -1
        self.BOARD_SIZE = 15
        self.NUM_SIMULATION = 400

        self.tau = 10
        self.c_puct = 0
        self.decay = 0

        self.SPACE = 30
        self.STONE_SIZE = 15
        self.IN_MARGIN = 20
        self.OUT_MARGIN = 30
        self.MARGIN = self.IN_MARGIN+self.OUT_MARGIN
        self.size = [2*self.MARGIN+self.SPACE*(self.BOARD_SIZE-1),2*self.MARGIN+self.SPACE*(self.BOARD_SIZE-1)]
        self.BLACK_COLOR = (  0,  0,  0)
        self.WHITE_COLOR = (255,255,255)
        self.BOARD_COLOR = (252,191,146)
        self.FPS = 10
        self.BOARD_SIZE = 15
        self.STONE_MAX = 5
        self.NONE = 0
        self.BLACK = 1
        self.WHITE = -1

        self.coef = 1e-4

    def index2coordinate(self, index):
        row = index // self.BOARD_SIZE
        col = index % self.BOARD_SIZE
        return int(row), int(col)
        self.LEFT = 1
    
    def text_pos(self, ix, x, y):
        if ix < 10:
            return (self.MARGIN + y*self.SPACE - 3, self.MARGIN + x*self.SPACE - 3)
        else:
            return (self.MARGIN + y*self.SPACE - 6, self.MARGIN + x*self.SPACE - 3)
