#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 20:49:00 2020
A Game class which separates the bot-linking concepts from game-specific implementation. 
Not sure whether this is worthwhile given the relatively light saving and the unclear subclass function, but it may make debugging easier. 
@author: terrylines
"""
from bots import isBot
from random import shuffle

class Game:
    numberOfPlayers=NotImplementedError
    
    def _isValid(self,bots):
        """ Checks the bots are the correct class and number for the game"""
        if all([isBot(bot) for bot in bots]) and self._isCorrectNumberOfBots(len(bots)):
            return True
        return False

    def _isCorrectNumberOfBots(self,numberOfBots):
        """ returns whether the number of bots is valid for the game"""
        return numberOfBots==self.numberOfPlayers
        
    def __init__(self,bots):
        """checks bots valid and assigns to players (objects within the game) """
        if not self._isValid(bots):
            raise ValueError
        self.players=[self.Player(self,index,bot) for index,bot in enumerate(bots)]
    
    def _shufflePlayers(self):
        """reassign bots  to players """
        bots = [player.bot for player in self.players]
        shuffle(bots)
        for i,bot in enumerate (bots):
            self.players[i].bot = bot 
    
    def _setupGame(self):
        """ initialises the game"""
        raise  NotImplementedError
    
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
                raise IOError("Invalid action passed to game by" + self)
            return action