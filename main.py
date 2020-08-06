#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 07:23:14 2020

@author: terrylines
"""

from UltimateOX_Terry import Game
from UltimateOX_Terry import XOHuman
from bots import RandomBot

player1=XOHuman("Terry")
player2=XOHuman("Mikey")
player3=RandomBot("Peter")
player4=RandomBot("Nick")

t=Game([player1,player3])
t.playGame()

# # show that two random players get a zero avg scroe
# scores2=player2.play(Game = OX_short.OX,reward = bots.marginReward, opponents = [player1],repeats = 1)
# sum(scores2)/10000

# # a simple tactic of taking centre gets an 0.2 avg score
# scores3=player3.play(Game = OX_short.OX,reward = bots.marginReward, opponents = [player1],repeats = 10000)
# sum(scores3)/10000

# #0.95 win rate against a random
# scores4=player4.play(Game = OX_short.OX,reward = bots.marginReward, opponents = [player1],repeats = 10000)
# sum(scores4)/10000

# #0.85 against centre taker bot. note that policy for starting state is always centre for our trained bot
# scores4_3=player4.play(Game = OX_short.OX,reward = bots.marginReward, opponents = [player3],repeats = 10000)
# sum(scores4_3)/10000


# scores5=player5.play(Game = OX_short.OX,reward = bots.marginReward, opponents = [player4],repeats = 10000)
# sum(scores5)/10000
# scores5.count(0) #all 10000 ended as draws


# game=OX_short.OX([bots.Human("Terry"),player5])
# game.playGame()

# list(player4.stateValues.items())[0:9]
# #high win value except for when the opoonent bot has taken the centre

# player4.ExpectedReturn((0,0,0,0,0,0,0,0,0),0) #higher expected return by taking corner
# player4.ExpectedReturn((0,0,0,0,0,0,0,0,0),4)
# player4.ExpectedReturn((0,0,0,0,0,0,0,0,0),2) #matches other corner

# player6=MonteCarloEpsilonGreedy_bot.OXMonteCarloEpsGreedyBot("Titus",0.1)

# scoresA=player6.train(Game = OX_short.OX,rewardFn = bots.marginReward, opponents = [player1],repeats = 100000)
# sum(scoresA)/100000

# import matplotlib.pyplot as plt

# X = range(99000)
# plt.plot(X,[sum(scoresA[x:x+1000])/1000 for x in X])
# plt.show()

# player7=MonteCarloEpsilonGreedy_bot.OXMonteCarloEpsGreedyBot("Titus",0.05)

# scoresB=player7.train(Game = OX_short.OX,rewardFn = bots.marginReward, opponents = [player1],repeats = 100000)
# sum(scoresB)/100000

# import matplotlib.pyplot as plt

# plt.plot(X,[sum(scoresB[x:x+1000])/1000 for x in X])
# plt.show()

# player8=MonteCarloEpsilonGreedy_bot.OXMonteCarloEpsGreedyBot("Titus",0.01)

# scoresC=player8.train(Game = OX_short.OX,rewardFn = bots.marginReward, opponents = [player1],repeats = 100000)
# sum(scoresC)/100000

# import matplotlib.pyplot as plt


# plt.plot(X,[sum(scoresC[x:x+1000])/1000 for x in X])
# plt.show()
