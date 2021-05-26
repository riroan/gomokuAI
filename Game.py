class Game:
    def __init__(self, size):
        self.size = size
        self.board = [[0] * self.size for _ in range(self.size)]
        self.player = 1      # 1 : black, -1 : white
        self.STONE_MAX = 5
        self.gameOver = False
        self.winner = 0

    def getState(self):
        return self.board

    def getAbleAction(self):
        actions = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    actions.append(i*self.size + j)
        return actions

    def action2Pos(self, action):
        return action // self.size, action % self.size

    def pos2Action(self, pos):
        return pos[0] * self.size + pos[1]

    def doAction(self, action):
        if action in self.getAbleAction():
            pos = self.action2Pos(action)
            self.board[pos[0]][pos[1]] = self.player
            self.isWin()
            self.player *= -1
            return True
        else:
            return False

    def isWin(self):
        for y in range(self.size):
            for x in range(self.size):
                match = 0
                for i in range(self.STONE_MAX):
                    if x + i >= self.size:
                        break
                    if self.board[y][x + i] == self.player:
                        match += 1
                    else:
                        break
                    if match >= self.STONE_MAX:
                        self.gameOver = True
                        self.winner = self.player
                        return

                match = 0
                for i in range(self.STONE_MAX):
                    if y + i >= self.size:
                        break
                    if self.board[y + i][x] == self.player:
                        match += 1
                    else:
                        break
                    if match >= self.STONE_MAX:
                        self.gameOver = True
                        self.winner = self.player
                        return

                match = 0
                for i in range(self.STONE_MAX):
                    if x + i >= self.size or y + i >= self.size:
                        break
                    if self.board[y + i][x + i] == self.player:
                        match += 1
                    else:
                        break
                    if match >= self.STONE_MAX:
                        self.gameOver = True
                        self.winner = self.player
                        return

                match = 0
                for i in range(self.STONE_MAX):
                    if x - i < 0 or y + i >= self.size:
                        break
                    if self.board[y + i][x - i] == self.player:
                        match += 1
                    else:
                        break
                    if match >= self.STONE_MAX:
                        self.gameOver = True
                        self.winner = self.player
                        return