#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 20:49:00 2020
Game class filled in with OX specific stuff
@author: terrylines
"""
from bots import isBot
from random import shuffle

class Game:

    def _isValid(self,bots):
        """ Checks the bots are the correct class and number for the game"""
        if all([isBot(bot) for bot in bots]) and self._isCorrectNumberOfBots(len(bots)):
            return True
        return False

    def _isCorrectNumberOfBots(self,numberOfBots):
        """ returns whether the number of bots is valid for the game"""    
        return numberOfBots==2
        
    def __init__(self,bots):
        """checks bots valid and assigns to players (objects within the game) """
        if not self._isValid(bots):
            raise ValueError
        self.players=[Player(self,index,bot) for index,bot in enumerate(bots)]
    
    def _shufflePlayers(self):
        """reassign bots  to players """
        bots = [player.bot for player in self.players]
        shuffle(bots)
        for i,bot in enumerate (bots):
            self.players[i].bot = bot 
    
    def _setupGame(self):
        """ initialises the game"""
        self._board=[0,0,0,0,0,0,0,0,0] #board is a 9-list with 1 for player 1 (X) pieces, 0 for blank squares, and -1 for opponent pieces
  
    def _play(self,action):
        """ applies the action to the current game"""
        self._board[action] = 1 if self.currentPlayer._playerX else -1
        return
    
    def __str__(self):
        """ Returns the current gameState and possible actions in a human-friendly format"""
        def row(values):
            tile_image = ('O',' ','X')
            tiles = [tile_image[i+1] for i in values] 
            return '|'.join(tiles) + '\n'
        blankrow = '-----\n'
        grid = blankrow.join( [row(self._board[3*i:3*i+3]) for i in range(0,3) ] )
        player = "Current Player is " + ('X' if self._playerX else 'O') + '\n'
        bot = "Input required from " + self.bot.name + '\n'
        actions = 'Actions are ' + ','.join([str (i) for i in self.actions]) + '\n'
        return  grid + player +bot + actions
    
    def _getScores(self):
        
        """Returns the final outcome for all players"""
        winningLines=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        def match(n):
            return any ( [all([self._board[i]==n for i in line]) for line in winningLines])
        
        return [int(match(n)) for n in [1,-1] ]
        
    def _isFinished(self):
        """Indicates the games is finished"""
        return not self.currentPlayer.actions or any(self._getScores())

    @property
    def save(self):
        return self.__dict__

    @property
    def load(self,savedGame):
        self.__dict__=savedGame

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
        self._playerX=self.index==0
        pass
        
    def __str__(self):
        """ Returns the current game in a human-friendly format"""
        return  self.game.__str__
    
    @property
    def state(self):
        """ a bot-friendly format of the gameState from the point of view of current player"""
        return self.game._board if self._playerX else [-i for i in self.game._board] 

    @property
    def actions(self):
        """ a bot-friendly list of possible actions from the point of view of current player"""
        return [i for i, x in enumerate(self.state) if x == 0]   
  
    def prompt(self):
        action = self.bot.promptBot(self)
        if action not in self.actions:
            raise IOError("Invalid action passed to game by" + self)
        return action
