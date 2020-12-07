from abc import ABC, abstractmethod
import os
import collections
import numpy as np
import random


class Learner(ABC):
    def __init__(self, alpha, gamma, eps=0.1):
        # parameters
        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps

        # possible actions
        self.actions = self.get_possible_actions(None)

        # Initialize all a/s values to 0
        self.Q = self.initialize_Q()

        # record all rewards
        self.rewards = []

    #return moves available from current state
    def get_possible_actions(self, state):

        if state is None:
            possible_actions = [(j,i) for i in range(3) for j in range(3)]
        else:
            possible_actions = [a for a in self.actions if state[a[0]*3 + a[1]] == '-']

        return possible_actions

    #initialize all state action pairs
    def initialize_Q(self):
        Q = {}
        for action in self.actions:
            Q[action] = collections.defaultdict(int)
        return Q

    #go with best action
    def max_Q(self, Q, state):
        max_value = -99999
        max_action = (0,1)
        possible_actions = self.get_possible_actions(state)

        for action in possible_actions:

            value = Q[action][state]
            if value > max_value:
                max_value = value
                max_action = action

        return max_action

    #get epsilon greedy move
    def get_action_epsilon_greedy(self, state):
        possible_actions = self.get_possible_actions(state)
        rand = np.random.rand()
        #if rand number 0-1 is bigger or equal to epsilon then go with best policy
        if (rand < self.eps):
            action = possible_actions[np.random.choice(len(possible_actions))]
        else:
            action = self.max_Q(self.Q, state)
        return action

    #gets greedy move ie the best policy
    def get_action_greedy(self, state):
        move = self.max_Q(self.Q, state)
        return move

    #get e-greedy or greedy action
    def get_action(self, state, epsilon=False):
        action = self.get_action_epsilon_greedy(state) \
            if epsilon else self.get_action_greedy(state)
        return action



class Qlearner(Learner):
    def __init__(self, alpha, gamma, eps):
        super().__init__(alpha, gamma, eps)

    def update(self, state, sPrime, action, aPrime, r):
        if sPrime is not None:
            possible_actions = super().get_possible_actions(sPrime)

            # get the action for the next state
            aPrime = super().get_action_epsilon_greedy(sPrime)

            # update
            self.Q[action][state] = self.Q[action][state] + self.alpha \
                * (r + self.gamma * self.Q[aPrime][sPrime] - self.Q[action][state])
        else:
            self.Q[action][state] += self.alpha*(r - self.Q[action][state])

        self.rewards.append(r)

class SARSAlearner(Learner):
    def __init__(self, alpha, gamma, eps):
        super().__init__(alpha, gamma, eps)

    def update(self, state, sPrime, action, aPrime, r):
        # Update Q(state,a)
        if sPrime is not None:
            possible_actions = super().get_possible_actions(sPrime)

            # get the action for the next state
            aPrime = super().get_action_epsilon_greedy(sPrime)

            # update
            self.Q[action][state] = self.Q[action][state] + self.alpha \
                * (r + self.gamma * self.Q[aPrime][sPrime] - self.Q[action][state])
        else:
            self.Q[action][state] += self.alpha*(r - self.Q[action][state])

        self.rewards.append(r)
