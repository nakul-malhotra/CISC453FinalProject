import random


class Game:
    def __init__(self, agent):
        self.agent = agent
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]


    '''
    Saves agent move
    '''
    def agentMove(self, action):
        self.board[action[0]][action[1]] = 'O'


    '''
    Picks a random empty space
    '''
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
    Gets 1-d list representation of board
    '''

    def get1DBoard(self):
        newList = []
        for row in self.board:
            for col in row:
                newList.append(col)
        return newList

    '''
    Checks for draw
    '''
    def checkDraw(self):
        boardList = self.get1DBoard()
        if '-' not in boardList:
            return True
        return False

    '''
    Updates Q: state action pairs
    '''

    def updateAgent(self, prev_state, prev_action):
        new_state = self.flattenBoard()
        new_action =  self.agent.get_action(new_state)
        self.agent.update(prev_state, new_state, prev_action,new_action, 0)
        return new_state,new_action


    '''
    Places X at random (free) location
    '''
    def trainMove(self):
        action = self.randomMove()
        self.board[action[0]][action[1]] = 'X'


    '''
    When agent plays against compute computer makes random moves
    '''

    def playGameTrain(self, opponentFirst):
        if opponentFirst:
            self.trainMove()
        state =None
        currentAction = None
        while True:
            if not currentAction:
                state = self.flattenBoard()
                currentAction = self.agent.get_action(state)
            #agent move
            self.agentMove(currentAction)
            #check if game done
            if self.checkWin():
                reward = 1 #reward 1 if agent wins
                break;
            if self.checkDraw():
                reward = 0 #reward 0 if draw
                break;
            #player move
            self.trainMove()
            #check if game done
            if self.checkWin():
                reward = -1 #reward -1 if player wins
                break;
            if self.checkDraw():
                reward = 0 #reward 0 if draw
                break;

            #update agent after every move
            state,currentAction = self.updateAgent(state,currentAction)


        self.agent.update(state, None, currentAction, None, reward)

    '''
    Show player move
    '''

    def personMove(self):
        self.printBoard()
        while True:
            move = input(" Select (row,col) 0-2: ")
            print()
            try:
                row, col = int(move[0]), int(move[2])
            except ValueError:
                print("Invalid, please try again")
                continue
            if row not in range(3) or col not in range(3) or not self.board[row][col] == '-':
                print("Already taken, try again")
                continue
            self.board[row][col] = 'X'
            break


    '''
    Accepts user moves rather than random agent
    '''

    def playGamePerson(self,opponentFirst):
        if opponentFirst:
            self.personMove()
        state =None
        currentAction = None
        while True:
            if not currentAction:
                state = self.flattenBoard()
                currentAction = self.agent.get_action(state)
            #agent move
            self.agentMove(currentAction)
            #check if game done
            if self.checkWin():
                reward = 1 #reward 1 if agent wins
                break;
            if self.checkDraw():
                reward = 0 #reward 0 if draw
                break;
            #player move
            self.personMove()
            #check if game done
            if self.checkWin():
                reward = -1 #reward -1 if player wins
                break;
            if self.checkDraw():
                reward = 0 #reward 0 if draw
                break;

            #update agent after every move
            state,currentAction = self.updateAgent(state,currentAction)


        self.printBoard() #print final board
        if reward == 0:
            print()
            print("It was a draw!")
        elif reward == -1:
            print()
            print("You won!")
            print()
        else:
            print()
            print("You lost!")
            print()

        self.agent.update(state, None, currentAction, None, reward)




    def start(self,training=False):
        #Then real player is playing
        if not training:
            print()
            print("Do you wish to go first?")

            while True:
                option = input("Options: 'y', 'n' or 'quit': ")
                if option =='y':
                    self.playGamePerson(opponentFirst=True)
                    break
                elif option =='n':
                    self.playGamePerson(opponentFirst=False)
                    break
                elif option == 'quit':
                    print("See you later!")
                    exit()
                print("Invalid option: " + option)
        #Still in training
        else:
            if random.random() < 0.5:
                self.playGameTrain(opponentFirst=False)
            else:
                self.playGameTrain(opponentFirst=True)

    '''
    flattens board to string
    '''
    def flattenBoard(self):
        tempString = ''
        for row in self.board:
            for value in row:
                tempString = tempString + value

        return tempString


    def printBoard(self):
        # "board" is a list of 10 strings representing the board (ignore index 0)
        print('   |   |')
        print(' ' + self.board[0][0] + ' | ' + self.board[0][1] + ' | ' + self.board[0][2])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + self.board[1][0] + ' | ' + self.board[1][1] + ' | ' + self.board[1][2])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + self.board[2][0] + ' | ' + self.board[2][1] + ' | ' + self.board[2][2])
        print('   |   |')
