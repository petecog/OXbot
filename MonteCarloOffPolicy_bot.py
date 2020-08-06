#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 21:32:25 2020
Monte Carlo with off-policy weighted importance sampling. Only takes into account terminal score
Greedy deterministic target policy
Epsilon-greedy behaviour policy

@author: terrylines
"""

from bots import Bot
from random import choices

class OXMonteCarloOffPolicyBot(Bot):
    def __init__(self,name,epsilon):
        self.name=name
        self.epsilon=epsilon
        self.states={}
        self.actionValues={}
        self.sampleSize={}
        self.targetPolicy={}
        self.behaviourPolicy={}
        self.actions={}
        self.recordActions=False
        self.record=[]
#        self.initialStates()
       
    def promptBot(self,game):
        state=tuple(game.state)
        actions=self.obtain(self.actions,state)
        policy=self.policy[state]
        action=choices(population=actions,weights=policy,k=1)[0]
#        print(str(action)+" chosen action\n")
        if self.recordActions:
            self.record.append((state,action))
        return action
    
    def initialiseState(self,state):
#        print("1st visit to "+str(state))
        self.actions[state]= [i for i, x in enumerate(state) if x == 0]
        n=len(self.actions[state])
#        print(", "+str(n)+ "possible actions\n")
        self.policy[state]=[1/n] * n
        for action in self.actions[state]:
            self.actionValues[(state,action)]=0
            self.sampleSize[(state,action)]=0
        
#    def initialStates(self):
#        start=(0,0,0,0,0,0,0,0,0)
#        self.initialiseState(start)
#        for i in range(9):
#            move=list(start)
#            move[i]=-1
#            self.initialiseState(tuple(move))
    
    def train(self,Game,rewardFn,opponents,repeats):
        """Repeatedly plays a game and uses the reward values ( terminal) to train the policy"""
        bots=[self] + opponents
        game=Game(bots)
        self.recordActions=True
        rewards=[]
        for _ in range(repeats):
            self.record=[]
#            print("about to record training game "+str(_))
            score = game.playGame()     
            reward = rewardFn(score,self)
#            print("reward: "+str(reward))
            rewards.append(reward)
            self.updateBot(reward)
        return rewards
    
    def updateBot(self,reward):
        states=[]
        for state,action in self.record:
            self.sampleSize[(state,action)]+=1
            prior=self.actionValues[(state,action)]
            self.actionValues[(state,action)]=prior + 1/self.sampleSize[(state,action)] * (reward-prior)
            states.append(state)
        
        for state in set(states):
            greedyAction=max(self.actions[state],key=lambda x:self.actionValues[(state,x)])
            n=len(self.actions[state])
            self.policy[state]=[(1-self.epsilon +self.epsilon/n) if action==greedyAction else self.epsilon/n for action in self.actions[state]]

            

    def obtain(self,dic,state):
        if state not in dic.keys():
            self.initialiseState(state)
        return dic[state]

        

    