#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  9 15:44:19 2020

@author: terrylines
"""

from bots import isBot
from random import shuffle
import numpy as np
import random

class Mastermind: 
    numberOfPlayers=1
    
    def _isValid(self,bots):
        """ Checks the bots are the correct class and number for the game"""
        if all([isBot(bot) for bot in bots]) and self._isCorrectNumberOfBots(len(bots)):
            return True
        return False

    def _isCorrectNumberOfBots(self,numberOfBots):
        """ returns whether the number of bots is valid for the game"""
        return numberOfBots==self.numberOfPlayers
        
    def __init__(self,bots,colnum,pegnum):
        """checks bots valid and assigns to players (objects within the game) """
        if not self._isValid(bots):
            raise ValueError
        self.players=[self.Player(self,index,bot) for index,bot in enumerate(bots)]
        self.colnum = colnum
        self.pegnum = pegnum
    
    def _shufflePlayers(self):
        """reassign bots  to players """
        bots = [player.bot for player in self.players]
        shuffle(bots)
        for i,bot in enumerate (bots):
            self.players[i].bot = bot 
    
    def _setupGame(self):
        """ initialises the game"""
        self.gesses = [] #This will contain a list of guesses; each guess will itself be a list of '[index of guess, [red pegs, white pegs]]'
        self.possibilities={_intToBaseN(i) for i in range(colnum**pegnum) } #set of all possible answers
        self.answer=
    
    @staticmethod
    def _intToBaseN(i):
        result=""
        while i>0
        i,r = divmod(i,colnum)
        result+=r
        return()
        
    def _play(self,action):
        """ applies the action to the current game"""
        raise  NotImplementedError
   
    def __str__(self):
        """ Returns the current game in a human-friendly format"""
        raise  NotImplementedError
  
    def _getScores(self):
        """Returns the final outcome for all bots"""
        raise  NotImplementedError
        
    def _isFinished(self):
        """Indicates the games is finished"""
        raise  NotImplementedError

    @property
    def save(self):
        """ Saves all game attributes"""
        raise NotImplementedError

    @property
    def load(self,savedGame):
        """ Loads all game attributes"""
        raise NotImplementedError  

    def _nextPlayer(self):
        """cycles through list of players """
        m = self.currentPlayer.index
        n = (m+1) % len(self.players)
        return self.players[n]
        
    def playGame(self):
        """ plays the game, prompting the current player for their action """
        self._shufflePlayers()
        self._setupGame()    
        self.currentPlayer=self.players[0]
    
        while(True):
            action = self.currentPlayer.prompt()
            self._play(action)
            self.currentPlayer=self._nextPlayer() 
            if self._isFinished():
                break          
        
        playerScores= self._getScores()
        botScores = {player.bot.name: playerScores[i] for i,player in enumerate(self.players) }
        return  botScores
    
    class Player:
        """ these are players inside the game. Their bot attribute links to a bot which drives players decisions"""
        def __init__(self,game,index,bot):
            self.game=game
            self.bot=bot
            self.index=index
            self._setup()
            
        def _setup(self):
            """sets up the player with game specific attributes"""
            pass
                   
        def __str__(self):
            """ Returns the current game in a human-friendly format"""
            raise  NotImplementedError
        
        @property
        def state(self):
            """ a bot-friendly format of the gameState from the point of view of current player"""
            raise NotImplementedError
    
        @property
        def actions(self):
            """ a bot-friendly list of possible actions from the point of view of current player"""
            raise NotImplementedError    
      
        def prompt(self):
            action = self.bot.promptBot(self)
            if action not in self.actions:
                raise IOError("Invalid action passed to game by " + self.bot.name)
            return action

  def decompose(self, index0): #turn an index number into a list of specific pegs
   return [(int(index0 / self.colnum**i) % self.colnum) for i in range(self.pegnum)]

  def evaluate(self, answer, guess0): #returns the result that WOULD be obtained if guess0 was the guess, and answer was the answer
    a = self.decompose(answer)
    g = self.decompose(guess0)
    #find matches in correct position
    r = len([i for i in range(self.pegnum) if a[i]==g[i]])
    #find all matches
    m = list()
    for i in a:
      if i in g:
        g.remove(i)
        m.append(i)
    w = len(m)-r # white pegs are total matches less exact matches
    return [r, w] 

  def find_possibs(self, x): #works out which potential answers are still possible, based on the guesses passed to it as x (same format as self.gesses)
    posibs = np.ones(self.colnum**self.pegnum) #sets up an index of possible answers, all with 1s as they are still possible
    for i in x: #checks each guess that's been made
      for j in range(len(posibs)): #checks each possible answer
        if self.evaluate(i[0], j) != i[1]: #checks if the result from that guess is compatible with j being the answer
          posibs[j] = 0 #sets posib to 0 for that potential answer
    return posibs #sends back a vector of 1s / 0s for whether that answer is feasible given the guesses / results

  def guess(self): #identify a guess to make given current state, and elicit score from user
    #this implementation currently just picks a random possible guess from those that are feasible
    p = self.find_possibs(self.gesses)
    options = [i for i in range(len(p)) if p[i]==1]
   
    if len(p)==0: #no answers are feasible
      print("You're a lying scumbag, no answer is possible.")
      self.endedz=1
      return
    
    c = random.choice(options)
    
    if len(p)==1: #there's only one possible answer
      print("The answer is...")
      print(self.render(self.decompose(c)))
      print("I win in")
      print(len(self.gesses))
      print("guesses")
      self.endedz=1
      return
    
    #there are more than one possibility - game is still live

    print("My  next guess is...")
    print(self.render(self.decompose(c)))
    r=int(input("How many red pegs do I get?\n"))
    if r==3 or r==4:
      w=0
    else:    
      w=int(input("And how many white pegs?\n"))
    self.gesses.append([c, [r, w]])
    if r == self.pegnum:
      print("I win in")
      print(len(self.gesses))
      print("guesses")
      self.endedz=1
    return

  def render(self, guess): #depict a guess
    colnames = ["white", "red", "orange", "yellow", "green", "blue", "purple", "pink", "black"]
    cols = []
    for i in guess:
      cols.append(colnames[i])
    return cols

  def rungame(self): #runs itself as a game of MasterMind
    while self.endedz==0:
      self.guess()

x = GameState(8, 4)
x.rungame()



