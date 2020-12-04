import random


class Game:
    def __init__(self, agent, teacher=None):
        self.agent = agent
        self.teacher = teacher
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]


    def agentMove(self, action):
        self.board[action[0]][action[1]] = 'O'


    def randomMove(self):
        possibles = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '-':
                    possibles += [(i, j)]
        return possibles[random.randint(0, len(possibles)-1)]


    '''

    Returns true if there is a win on the board otherwise false

    '''

    def checkWin(self):
        options = ['O','X']
        for i in range(0,3):
            #check rows
            if (self.board[i][0] == self.board[i][1] == self.board[i][2]) and self.board[i][0] in options:
                return True
            #check cols
            if (self.board[0][i] == self.board[1][i] == self.board[2][i]) and self.board[0][i] in options:
                return True

        #check downwards diagonal
        if (self.board[0][0] == self.board[1][1] == self.board[2][2]) and self.board[0][0] in options:
            return True

        #check upwards diagonal
        if (self.board[2][0] == self.board[1][1] == self.board[0][2]) and self.board[2][0] in options:
            return True

        return False


    '''
    Checks for draw
    '''

    def checkDraw(self):
        draw = True
        for row in self.board:
            for value in row:
                if value == '-':
                    draw = False
        return draw


    '''

    Updates Q: state action pairs

    '''

    def updateAgent(self, prev_state, prev_action):
        new_state = self.getStateKey()
        new_action =  self.agent.get_action(new_state)
        self.agent.update(prev_state, new_state, prev_action,new_action, 0)
        return new_state,new_action


    def trainMove(self):
        action = self.randomMove()
        self.board[action[0]][action[1]] = 'X'


    '''

    When agent plays against compute
    Computer makes random moves
    Will update moves

    '''

    def playGameTrain(self, player_first):
        if player_first:
            self.trainMove()
        state =None
        currentAction = None
        while True:
            if not currentAction:
                state = self.getStateKey()
                currentAction = self.agent.get_action(state)
            #agent move
            self.agentMove(currentAction)
            #check if game done
            if self.checkDraw():
                reward = 0 #reward 0 if draw
                break;
            if self.checkWin():
                reward = 1 #reward 1 if agent wins
                break;
            #player move
            self.trainMove()
            #check if game done
            if self.checkDraw():
                reward = 0 #reward 0 if draw
                break;
            if self.checkWin():
                reward = -1 #reward -1 if player wins
                break;

            state,currentAction = self.updateAgent(state,currentAction)

        self.agent.update(state, None, currentAction, None, reward)

    '''
    Show player move

    '''

    def personMove(self):
        printBoard(self.board)
        while True:
            move = input(" Select (row,col) 0-2: ")
            print()
            try:
                row, col = int(move[0]), int(move[2])
            except ValueError:
                print("Invalid")
                continue
            if row not in range(3) or col not in range(3) or not self.board[row][col] == '-':
                print("Already taken, try again")
                continue
            self.board[row][col] = 'X'
            break


    def playGamePerson(self,player_first):
        if player_first:
            self.personMove()
        state =None
        currentAction = None
        while True:
            if not currentAction:
                state = self.getStateKey()
                currentAction = self.agent.get_action(state)
            #agent move
            self.agentMove(currentAction)
            #check if game done
            if self.checkDraw():
                reward = 0 #reward 0 if draw
                break;
            if self.checkWin():
                reward = 1 #reward 1 if agent wins
                break;
            #player move
            self.personMove()
            #check if game done
            if self.checkDraw():
                reward = 0 #reward 0 if draw
                break;
            if self.checkWin():
                reward = -1 #reward -1 if player wins
                break;

            state,currentAction = self.updateAgent(state,currentAction)

        self.agent.update(state, None, currentAction, None, reward)



    def start(self):
        #Then real player is playing
        if self.teacher is None:
            print()
            print("Do you wish to go first?")
            print("Options: 'y', 'n', 'quit'")
            print()
            option = input("Input : ")
            if option =='y':
                self.playGamePerson(player_first=True)
            elif option =='n':
                self.playGamePerson(player_first=False)
            elif option == 'quit':
                return
        #Still in training
        else:
            if random.random() < 0.5:
                self.playGameTrain(player_first=False)
            else:
                self.playGameTrain(player_first=True)

    '''
    flattens board to string
    '''
    def getStateKey(self):
        tempString = ''
        for row in self.board:
            for value in row:
                tempString = tempString + value

        return tempString


def printBoard(board):
    # "board" is a list of 10 strings representing the board (ignore index 0)
    print('   |   |')
    print(' ' + board[0][0] + ' | ' + board[0][1] + ' | ' + board[0][2])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[1][0] + ' | ' + board[1][1] + ' | ' + board[1][2])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[2][0] + ' | ' + board[2][1] + ' | ' + board[2][2])
    print('   |   |')
