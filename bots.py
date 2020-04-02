#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 20:49:00 2020

@author: terrylines
"""
from random import choice

def isBot(x):
    return isinstance(x, Bot)
    
def marginReward(score,player):
    opponents = {key:value for key,value in score.items() if key != player.name }
    return score[player.name] - max(opponents.values())

class Bot:
    def __init__(self,name):
        self.name=name
        
    def promptBot(self,game):
        raise NotImplementedError
        
    def play(self,Game,reward,opponents,repeats):
        """Repeatedly plays a game and returns a list of reward values"""
        bots=[self] + opponents
        game=Game(bots)
        scores = [game.playGame() for _ in range(repeats)]     
        rewards= [reward(score,self) for score in scores]
        return rewards
    
    
class Human(Bot):
    def promptBot(self,game):
        print(game)
        while True:
            action=int(input())
            if action in game.actions:
                break
        return action

class RandomBot(Bot):
    def promptBot(self,game):
        return choice(game.actions)

class OXMasterBot(Bot):
    def promptBot(self,game):
        return 4 if (4 in game.actions) else choice(game.actions)


