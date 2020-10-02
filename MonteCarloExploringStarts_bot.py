#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 21:32:25 2020
Monte Carlo with exploring starts approach to OX with random next player . Calculates the afterstate value (value of state having made an action)
We wish to estimate V_pi the value of afterstate V if following policy pi thereafter.

1. Choose a random after state and initialise an episode. Folloy policy thereafter. 
2. For all afterstates visited, update value
3. policy updated


@author: terrylines
"""

from bots import Bot
from bots import RandomBot
from OX_explorer import Game
from json import dump,load


class OXMonteCarloESBot(Bot):
    def __init__(self,name):
        self.name=name
        self.values={}
        self.sampleSize={}
        self.recordActions=False
        self.game=Game((self,RandomBot("random")),randomTurn=True)
          
    def promptBot(self,game):
        return self.policy(tuple(game.state))
    
    def policy(self,state):
        """Return the action with highest valued afterstate"""
        actions = (i for i,s in enumerate(state) if s is None)
        def play(state,k):
            a=list(state)
            a[k]=1 #always from X perspective
            return (tuple(a))
        action = max(actions, key = lambda k: self.values.get(play(state,k),0))
        afterstate = play(state,action)
            
        if self.recordActions:
            self.record.append(afterstate)

        return (action)
    
    def train(self,repeats):
        for _ in range(repeats):
            self.recordActions=True
            self.record=[]
            reward=self.game.playGame()
            self.updateValues(reward)
        
    def updateValues(self,reward):
        for afterstate in self.record:
            self.sampleSize[afterstate]=1+self.sampleSize.get(afterstate,0)
            prior=self.values.get(afterstate,0)
            self.values[afterstate]=prior + 1/self.sampleSize[afterstate] * (reward-prior)

# terry=OXMonteCarloESBot("terry")
# terry.train(1000000)
# terry2=OXMonteCarloESBot("terry2")
# terry2.game=Game((terry2,terry),randomTurn=True)
# terry2.train(1000000)
# terry.game=Game((terry,terry2),randomTurn=True)
# terry.train(1000000)

# with open('XOValues.txt', 'w') as outfile:
#     dump({str(k): v for k, v in terry.values.items()}, outfile)

import ast
with open('XOValues.txt') as json_file:
    data = load(json_file)
dic={ast.literal_eval(k):v for k,v in data.items()}
terry=OXMonteCarloESBot("terry")
terry.values= dic
terry2=OXMonteCarloESBot("terry2")
terry2.game=Game((terry2,terry),randomTurn=True)
terry2.values= dic
terry2.train(4000000)
terry.game=Game((terry,terry2),randomTurn=True)
terry.train(4000000)

with open('XOValues.txt', 'w') as outfile:
    dump({str(k): v for k, v in terry.values.items()}, outfile)


a=sum(terry.game.playGame() for _ in range(10000))
b=sum(terry2.game.playGame() for _ in range(10000))
print(a)
print(b)
a=sum(terry.game.playGame(board=[None]*9) for _ in range(10000))
b=sum(terry2.game.playGame(board=[None]*9) for _ in range(10000))
print(a)
print(b)
    
    


    