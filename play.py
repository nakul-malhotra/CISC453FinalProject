import os
import sys
import numpy as np
import matplotlib.pylab as plt
from agent import Qlearner, SARSAlearner
from environment import Game


'''
Plots the rewards
'''
def plot_agent_reward(rewards):
    plt.plot(np.cumsum(rewards))
    plt.title('Agent Cumulative Reward vs. Iteration')
    plt.ylabel('Reward')
    plt.xlabel('Episode')
    plt.show()

class PlayGame():
    def __init__(self, agentType, numOfEpisodes, alpha=0.5, gamma=0.9, epsilon=0.1):
        self.numOfEpisodes = numOfEpisodes
        if agentType == "q":
            self.agent = Qlearner(alpha,gamma,epsilon)
        else:
            self.agent = SARSAlearner(alpha,gamma,epsilon)



    def userPlayAgent(self):
        while True:
            game = Game(self.agent)
            game.start()
            playAgain = input("Would you like to play again? ('y', 'n'): ")
            if playAgain=='n':
                print("See you later!")
                break;
            print()
            print("Okay lets play again!")
            print()

    '''
    Teach agent - intelligence depends on number of games
    '''
    def teachAgent(self):
        iteration = 0
        while iteration < self.numOfEpisodes:
            game = Game(self.agent)
            game.start(training=True)
            iteration += 1
            if iteration % 10000 == 0:
                print("Training round: " + str(iteration))
        plot_agent_reward(self.agent.rewards)

'''
Gets Specification on training iterations and agent type from user
'''
def getUserValues():
    print("Welcome to Tic-Tac-Toe")
    #get agentType
    while True:
        print()
        agentType = input("Please input Agent Type (qlearning or sarsa) 'q' or 's': ")
        if agentType == 'q' or agentType == 's':
            print()
            if agentType == 'q':
                print('You entered Q-learning!')
            else:
                print('You entered Sarsa!')
            break
        print("Invalid agent type: " + agentType)


    #getEpisodes
    print()
    print("For smart agent enter four hundred thousand (400000): ")
    print()
    numOfEpisodes = int(input("Please enter the number of episodes you want to train agent: "))
    game = PlayGame(agentType, numOfEpisodes)
    game.teachAgent()
    print("Done Teaching!")
    game.userPlayAgent()



if __name__=="__main__":
    getUserValues()
