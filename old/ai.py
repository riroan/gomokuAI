import numpy as np

SIZE = 19

class ai:
    def __init__(self, game):
        self.value = np.zeros((SIZE,SIZE))
        self.game = game
        
    def value_init(self):
        for i in range(SIZE):
            for j in range(SIZE):
                if self.game.board[i][j] != 0:
                    self.value[i][j] = -999
        
    def value_four(self):
        for i in range(SIZE):
            for j in range(SIZE - 3):
                if self.game.board[i][j] == self.game.board[i][j+1] and self.game.board[i][j+1] == self.game.board[i][j+2] and self.game.board[i][j+2] == self.game.board[i][j+3] and self.game.board[i][j+3] == -1:
                    if j==0:
                        self.value[i][j+4] += 100
                    elif j == SIZE - 4:
                        self.value[i][j-1] += 100
                    else:
                        self.value[i][j-1] += 100
                        self.value[i][j+4] += 100
                        
                elif self.game.board[i][j] == self.game.board[i][j+1] and self.game.board[i][j+1] == self.game.board[i][j+2] and self.game.board[i][j+2] == self.game.board[i][j+3] and self.game.board[i][j+3] == 1:
                    if j==0:
                        self.value[i][j+4] += 95
                    elif j == SIZE - 4:
                        self.value[i][j-1] += 95
                    else:
                        self.value[i][j-1] += 95
                        self.value[i][j+4] += 95
                        
        for i in range(SIZE-3):
            for j in range(SIZE-3):
                if self.game.board[i][j] == self.game.board[i+1][j+1] and self.game.board[i+1][j+1] == self.game.board[i+2][j+2] and self.game.board[i+2][j+2] == self.game.board[i+3][j+3] and self.game.board[i+3][j+3] == -1:
                    if j==0:
                        self.value[i+4][j+4]+=100
                    elif j==SIZE-4:
                        self.value[i-1][j-1]+=100
                    else:
                        self.value[i-1][j-1]+=100
                        self.value[i+4][j+4]+=100
                if self.game.board[i][j] == self.game.board[i+1][j+1] and self.game.board[i+1][j+1] == self.game.board[i+2][j+2] and self.game.board[i+2][j+2] == self.game.board[i+3][j+3] and self.game.board[i+3][j+3] == 1:
                    if j==0:
                        self.value[i+4][j+4]+=95
                    elif j==SIZE-4:
                        self.value[i-1][j-1]+=95
                    else:
                        self.value[i-1][j-1]+=95
                        self.value[i+4][j+4]+=95
        
        for j in range(SIZE):
            for i in range(SIZE-3):
                if self.game.board[i][j] == self.game.board[i+1][j] and self.game.board[i+1][j] == self.game.board[i+2][j] and self.game.board[i+2][j] == self.game.board[i+3][j] and self.game.board[i+3][j] == -1:
                    if i==0:
                        self.value[i+4][j]+=100
                    elif i==SIZE-4:
                        self.value[i-1][j]+=100
                    else:
                        self.value[i-1][j]+=100
                        self.value[i+4][j]+=100
                if self.game.board[i][j] == self.game.board[i+1][j] and self.game.board[i+1][j] == self.game.board[i+2][j] and self.game.board[i+2][j] == self.game.board[i+3][j] and self.game.board[i+3][j] == 1:
                    if i==0:
                        self.value[i+4][j]+=95
                    elif i==SIZE-4:
                        self.value[i-1][j]+=95
                    else:
                        self.value[i-1][j]+=95
                        self.value[i+4][j]+=95
                        
        for i in range(3,SIZE):
            for j in range(SIZE-3):
                if self.game.board[i][j] == self.game.board[i-1][j+1] and self.game.board[i-1][j+1] == self.game.board[i-2][j+2] and self.game.board[i-2][j+2] == self.game.board[i-3][j+3] and self.game.board[i-3][j+3] == -1:
                    if j==0:
                        self.value[i-4][j+4]+=100
                    elif j==SIZE-4:
                        self.value[i+1][j-1]+=100
                    else:
                        self.value[i+1][j-1]+=100
                        self.value[i-4][j+4]+=100
                if self.game.board[i][j] == self.game.board[i-1][j+1] and self.game.board[i-1][j+1] == self.game.board[i-2][j+2] and self.game.board[i-2][j+2] == self.game.board[i-3][j+3] and self.game.board[i-3][j+3] == 1:
                    if j==0:
                        self.value[i-4][j+4]+=95
                    elif j==SIZE-4:
                        self.value[i+1][j-1]+=95
                    else:
                        self.value[i+1][j-1]+=95
                        self.value[i-4][j+4]+=95
                        
    def value_three(self):
        for i in range(SIZE):
            for j in range(SIZE - 2):
                if self.game.board[i][j]==self.game.board[i][j+1] and self.game.board[i][j+1] == self.game.board[i][j+2] and self.game.board[i][j+2] == -1:
                    if j == 0:
                        self.value[i][j+3] +=80
                    elif j==SIZE-3:
                        self.value[i][j-1]+=80
                    else:
                        self.value[i][j+3]+=80
                        self.value[i][j-1]+=80
                        
                if self.game.board[i][j]==self.game.board[i][j+1] and self.game.board[i][j+1] == self.game.board[i][j+2] and self.game.board[i][j+2] == 1:
                    if j == 0:
                        self.value[i][j+3] += 70
                    elif j==SIZE-3:
                        self.value[i][j-1]+=70
                    else:
                        self.value[i][j+3]+=70  
                        self.value[i][j-1]+=70
                            
        for i in range(SIZE - 2):
            for j in range(SIZE - 2):
                if self.game.board[i][j]==self.game.board[i+1][j+1] and self.game.board[i+1][j+1] == self.game.board[i+2][j+2] and self.game.board[i+2][j+2] == -1:
                    if j == 0:
                        self.value[i+3][j+3] +=80
                    elif j==SIZE-3:
                        self.value[i-1][j-1]+=80
                    else:
                        self.value[i+3][j+3]+=80
                        self.value[i-1][j-1]+=80
                            
                if self.game.board[i][j]==self.game.board[i+1][j+1] and self.game.board[i+1][j+1] == self.game.board[i+2][j+2] and self.game.board[i+2][j+2] == 1:
                    if j == 0:
                        self.value[i+3][j+3] += 70
                    elif j==SIZE-3:
                        self.value[i-1][j-1]+=70
                    else:
                        self.value[i+3][j+3]+=70
                        self.value[i-1][j-1]+=70
                            
        for j in range(SIZE):
            for i in range(SIZE - 2):
                if self.game.board[i][j]==self.game.board[i+1][j] and self.game.board[i+1][j] == self.game.board[i+2][j] and self.game.board[i+2][j] == -1:
                    if i == 0:
                        self.value[i+3][j] +=80
                    elif i==SIZE-3:
                        self.value[i-1][j]+=80
                    else:
                        self.value[i+3][j]+=80
                        self.value[i-1][j]+=80
                            
                if self.game.board[i][j]==self.game.board[i+1][j] and self.game.board[i+1][j] == self.game.board[i+2][j] and self.game.board[i+2][j] == 1:
                    if i == 0:
                        self.value[i+3][j] += 70
                    elif i==SIZE-3:
                        self.value[i-1][j]+=70
                    else:
                        self.value[i+3][j]+=70
                        self.value[i-1][j]+=70
                            
        for i in range(2,SIZE):
            for j in range(SIZE - 2):
                if self.game.board[i][j]==self.game.board[i-1][j+1] and self.game.board[i-1][j+1] == self.game.board[i-2][j+2] and self.game.board[i-2][j+2] == -1:
                    if j == 0:
                        self.value[i-3][j+3] +=80
                    elif j==SIZE-3:
                        self.value[i+1][j-1]+=80
                    else:
                        self.value[i-3][j+3]+=80
                        self.value[i+1][j-1]+=80
                            
                if self.game.board[i][j]==self.game.board[i-1][j+1] and self.game.board[i-1][j+1] == self.game.board[i-2][j+2] and self.game.board[i-2][j+2] == 1:
                    if j == 0:
                        self.value[i-3][j+3] += 70
                    elif j==SIZE-3:
                        self.value[i+1][j-1]+=70
                    else:
                        self.value[i-3][j+3]+=70
                        self.value[i+1][j-1]+=70
                            
    def value_two(self):
        for i in range(SIZE):
            for j in range(SIZE -1):
                if self.game.board[i][j] == self.game.board[i][j+1] and self.game.board[i][j+1] == -1:
                    if j==0:
                        self.value[i][j+2]+=60
                    elif j==SIZE -2:
                        self.value[i][j-1]+=60
                    else:
                        self.value[i][j+2]+=60
                        self.value[i][j-1]+=60
                if self.game.board[i][j] == self.game.board[i][j+1] and self.game.board[i][j+1] == 1:
                    if j==0:
                        self.value[i][j+2]+=55
                    elif j==SIZE -2:
                        self.value[i][j-1]+=55
                    else:
                        self.value[i][j+2]+=55
                        self.value[i][j-1]+=55
                            
        for i in range(SIZE-1):
            for j in range(SIZE -1):
                if self.game.board[i][j] == self.game.board[i+1][j+1] and self.game.board[i+1][j+1] == -1:
                    if j==0:
                        self.value[i+2][j+2]+=60
                    elif j==SIZE -2:
                        self.value[i-1][j-1]+=60
                    else:
                        self.value[i+2][j+2]+=60
                        self.value[i-1][j-1]+=60
                if self.game.board[i][j] == self.game.board[i+1][j+1] and self.game.board[i+1][j+1] == 1:
                    if j==0:
                        self.value[i+2][j+2]+=55
                    elif j==SIZE -2:
                        self.value[i-1][j-1]+=55
                    else:
                        self.value[i+2][j+2]+=55
                        self.value[i-1][j-1]+=55
                        
        for j in range(SIZE):
            for i in range(SIZE -1):
                if self.game.board[i][j] == self.game.board[i+1][j] and self.game.board[i+1][j] == -1:
                    if i==0:
                        self.value[i+2][j]+=60
                    elif i==SIZE -2:
                        self.value[i-1][j]+=60
                    else:
                        self.value[i+2][j]+=60
                        self.value[i-1][j]+=60
                if self.game.board[i][j] == self.game.board[i+1][j] and self.game.board[i+1][j] == 1:
                    if i==0:
                        self.value[i+2][j]+=55
                    elif i==SIZE -2:
                        self.value[i-1][j]+=55
                    else:
                        self.value[i+2][j]+=55
                        self.value[i-1][j]+=55
                            
        for i in range(SIZE):
            for j in range(SIZE -1):
                if self.game.board[i][j] == self.game.board[i-1][j+1] and self.game.board[i-1][j+1] == -1:
                    if j==0:
                        self.value[i-2][j+2]+=60
                    elif j==SIZE -2:
                        self.value[i+1][j-1]+=60
                    else:
                        self.value[i-2][j+2]+=60
                        self.value[i+1][j-1]+=60
                if self.game.board[i][j] == self.game.board[i-1][j+1] and self.game.board[i-1][j+1] == 1:
                    if j==0:
                        self.value[i-2][j+2]+=55
                    elif j==SIZE -2:
                        self.value[i+1][j-1]+=55
                    else:
                        self.value[i-2][j+2]+=55
                        self.value[i+1][j-1]+=55
                            
    def value_one(self):
        for i in range(SIZE):
            for j in range(SIZE):
                if self.game.board[i][j] == -1:
                    if j!=SIZE -1:
                        self.value[i][j+1]+=20
                    if j != 0:
                        self.value[i][j-1]+=20
                    if i != SIZE-1:
                        self.value[i+1][j]+=20
                    if i != 0:
                        self.value[i-1][j]+=20
                if self.game.board[i][j] == 1:
                    if j!=SIZE -1:
                        self.value[i][j+1]+=15
                    if j != 0:
                        self.value[i][j-1]+=15
                    if i != SIZE-1:
                        self.value[i+1][j]+=15
                    if i != 0:
                        self.value[i-1][j]+=15
        
    def value_update(self):
        self.value_one()
        self.value_two()
        self.value_three()
        self.value_four()
        
    def get_action(self):
        self.value_init()
        self.value_update()
        max = np.max(self.value)
        cnt = 0
        actions = []
        for i in range(SIZE):
            for j in range(SIZE):
                if self.value[i][j]==max:
                    actions.append((i,j))
        return actions[np.random.choice(len(actions),1)[0]]
            
                            