#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 21:32:25 2020
Monte Carlo with exploring starts approach to OX . Not implemented as i would need to create a new OX gmae that allows arbitrary starts
@author: terrylines
"""

from bots import Bot
from bots import RandomBot
from random import choice
import OX_short

class OXMonteCarloESBot(Bot):
    def __init__(self,name):
        self.name=name
        self.bound=0.1
        self.actionValues={}
        self.sampleSize={}
        self.policy={}
        self.actions={}
        self.initialStates()
        self.trainingGame=OX_short.OX(self,RandomBot("random"))
          
    def promptBot(self,game):
        return self.policy[tuple(game.state)]
    
    def initialiseState(self,state):
        self.actions[state]= [i for i, x in enumerate(state) if x == 0]
        self.policy[state]=self.actions[state][0]
        for action in self.actions[state]:
            self.actionValues[(state,action)]=0
            self.sampleSize[(state,action)]=0
        
    def initialStates(self):
        start=(0,0,0,0,0,0,0,0,0)
        self.initialiseState(start)
        for i in range(9):
            move=list(start)
            move[i]=-1
            self.initialiseState(tuple(move))
    
    def train(self):
        startState,startAction=choice(self.actionValues)
        
        self.policyEvaluation()
        i=0
        while not self.policyImprovement():
            print("improvement round "+str(i))
            i+=1
            self.policyEvaluation()
            

    def policyEvaluation(self):
        oldLength=len(self.stateValues)
        delta=0
        for state in list(self.stateValues.keys()):
            v=self.stateValues[state]
            self.stateValues[state]=self.ExpectedReturn(state,self.policy[state])
            delta=max(delta,abs(v-self.stateValues[state]))
        print(str(len(self.stateValues))+" states, delta of"+str(delta))
        if len(self.stateValues) > oldLength or delta>self.bound:
            self.policyEvaluation()
    
    def policyImprovement(self):    
        stable=True
        for state in list(self.policy):
            a=self.policy[state]
            possibilities={action: self.ExpectedReturn(state,action) for action in self.actions[state]}
            self.policy[state]=max(possibilities,key=lambda x: possibilities[x])
            if self.policy[state]!=a:
                stable=False
        return(stable)

    def obtain(self,dic,state):
        if state not in dic.keys():
            self.initialiseState(state)
        return dic[state]
        
    def match(self,board,n):
        winningLines=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        return any ( [all([board[i]==n for i in line]) for line in winningLines])  
   

    def ExpectedReturn(self,state,action):
        #if mymove is a win expected return is 1
        #else expected return =-1 for all losses, zero for all draws and state value for all other states
    
    
            
       
        if action not in self.obtain(self.actions,state):
            return -100
        myMove=list(state)
        myMove[action]=1
        myMove=tuple(myMove)
        
        if self.match(myMove,1):
            return 1
        
        oppActions = [i for i, x in enumerate(myMove) if x == 0]
        if len(oppActions)==0:
            return 0
        p=1/len(oppActions)
        r=0
        for action in oppActions:
           oppMove=list(myMove)
           oppMove[action]=-1
           oppMove=tuple(oppMove)
           if self.match(oppMove,-1):
               r+=p * -1
           elif len(oppActions)==1:
              r+=p * 0
           else:
               r+=p * self.obtain(self.stateValues,oppMove)
        return r


        

    