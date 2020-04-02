#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 07:23:14 2020

@author: terrylines
"""

import games
import bots

player1=bots.RandomBot("Terry")
player2=bots.RandomBot("Mikey")
player3=bots.OXMasterBot("Nick")

scores1=player1.play(Game = games.OX,reward = bots.marginReward, opponents = [player2],repeats = 1)
sum(scores1)/10000

scores2=player3.play(Game = games.OX,reward = bots.marginReward, opponents = [player2],repeats = 10000)
sum(scores2)/10000
