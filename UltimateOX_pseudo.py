#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 20:15:00 2020
This module implements an ultimate OX game for use in reinforcement learning.

Summary of game structure
An OX game object has:
1. a board of 9 squares (X, O, None for blank)
2. A score (None for ongoing, 1 for X win, -1 for O win, 0 for draw)
3. A play method to update the board and score
4. A view method to view the board etc.


An ultimate OX game object has:
1. A set of 9 OX game objects
2 A superboard of 9 squares containing the score from each OX game. 
3. A score for the overall game
4. A nextsquare attribute which limits the choice of square for the next player
5. Play and view methods that call the methods from the OX board.
6. 2 player objects

Player objects are prompted for actions, can view gamestate and return actions



The interface uses the normal format for reinforcement learning: 
- A game has a series of states S, and sets of actions A_s available in each state. 
- A player has a policy P (P_s for all s in S) which defines the probability of choosing each action in A_s. 
- Upon choosing an action A, the game returns a reward R(S,A) and a new state.

Background notes on RL (not needed to code the game)
- A state value V_s is the expected value of all rewards from this state forwards. This is for a given policy.
- An optimal policy is a policy which maximises the state value.
- RL iteratively improves policy by estimating values through repeatedly playing games, and changing the policy to pick the actions which lead to the highest reward + next state value. 

Ultimate OX rules
X goes first
3x3 superBoard. each square containing a standard 3x3 OX board.
A player chooses a square on the superBoard, then makes a standard move on that XO board.
If the OX board is won, it is marked for that player on the superBoard
If available, the next player must choose the square on the superBoard that has the same position as the prior player's move on the XO board. If that square is not available, the next player can choose from any available square
A square is not available if it has been marked for either player, or it has no remaining moves (it is still available if there are no winning moves for either player). Note: some variants allow further moves even if a square has already been marked.
A player wins by having 3 in a row on the superboard.
If there are no available squares, the game is a draw.

Notes for ultimate XO RL learning
- reward function is 1 for winning the game, 0 for a draw, -1 for losing. 0 for all interim states.


@author: terrylines
"""
from bots import isBot
from random import shuffle

class OXboard:
    """ A standard OX board"""
    
    #combinations which win a game of OX 
    winning_lines=[
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
        ] 
    
    def __init__(self):
        """ Initialises a blank board """
        self.state=[None]*9
        self.score=None
    
    def play(self,square,player):
        """ Plays a move, updating the board and score 
        
        Parameters
        ----------
        square : int
            the chosen square from 0 to 8
        player : int 
            either 1 (X) or -1(O)
        """
        assert 0 <= square <=8 and self.state[square] is None, "Not a valid choice of square"
        assert self.score==None, "Attempting to play on a finished board"
        assert player in {1,-1}, "Not a player"
        self.state[square]= player
        self._updateScore()

    def _updateScore(self):
        """ Score current board state
         (None for ongoing, 1 for X win, -1 for O win, 0 for draw)
        """
        x_win= any(all(self.state[i]== 1 for i in line) for line in self.winning_lines)
        o_win= any(all(self.state[i]== -1 for i in line) for line in self.winning_lines)
        assert not (x_win and o_win), "Somehow both players have won the board"
        draw= not x_win and not o_win and not any (square is None for square in self.state) 
        if x_win:
            self.score=1
        elif o_win:
            self.score=-1
        elif draw:
            self.score=0
        else:
            self.score=None

    def __str__(self):
        """ Returns the current gameState and possible actions in a human-friendly format"""
        rows=[
            self._printRow(0),
            self._printHorizontalDivide(),
            self._printRow(1),
            self._printHorizontalDivide(),
            self._printRow(2)
            ]
        return "\n".join(rows)+"\n"

    def _printRow(self,n):
        """prints the nth row of the board"""
        
        row=[self._representation(self.state[i]) for i in self.winning_lines[n]]
        return "|".join(row)
    
    @staticmethod
    def _representation(i):
        """  Turns int representation into characters for viewing"""
        if i==None: return " "
        if i==1: return "X"
        if i==-1: return "O"
        return "-" 

    @staticmethod
    def _printHorizontalDivide():
        return "-----"

class superOXboard(OXboard):
    "A board made up of boards"
    def __init__(self):
        """ Initialises blank boards """
        self.boards=[OXboard() for _ in range(9)]
        self.state=[None]*9
        self.score=None
    
    def play(self,move,player):
        """ Plays a move, updating the board and score 
        
        Parameters
        ----------
        move : tuple (int,int)
            (the chosen board from 0 to 8,the chosen board from 0 to 8)
        player : int
            either 1(X) or -1(O
        """
        board,square = move
        assert 0 <= board <=8 and self.state[board] is None, "Not a valid choice of board"
        assert self.score==None, "Attempting to play in a finished game"
        self.boards[board].play(square,player)
        self.state[board]=self.boards[board].score
        self._updateScore()

    def _printRow(self,n):
        """prints the nth row of the superboard """
        boards=[self.boards[i] for i in self.winning_lines[n]]
        rows=[" "+ " || ".join(board._printRow(i) for board in boards) + " " for i in range(3)]
        gap="\n "+ " || ".join([OXboard._printHorizontalDivide() for _ in range(3)])+ " \n"
        return gap.join(rows)
    
    @staticmethod
    def _printHorizontalDivide():
        blank = "||".join([" "*7]*3)
        divide = "-"*25
        return "\n".join([blank,divide,divide,blank])

class Game:
    """ A SuperOX game with board and 2 players. Player 0 is X, and goes first. """

# The next 4 methods are housekeeping to allow bots (decision making entities external to the game) to be associated with players (objects within the game).
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
        """reassign bots to players """
        bots = [player.bot for player in self.players]
        shuffle(bots)
        for i,bot in enumerate (bots):
            self.players[i].bot = bot 
 
    def playGame(self):
        """ plays the game, prompting the current player for their action """
        self._shufflePlayers()
        self._setupGame()    
        
        while(self.board.score is None):
            board,square = self.currentPlayer.prompt() #action is a pair e.g. (2,3) representing square number on superboard and then square number on OX board.
            self.board.play((board,square),1 if self.currentPlayer.index==0 else -1)
            self.nextBoard = square if self.board.state[square] is None else None
            self.currentPlayer=self._nextPlayer() 
        
        print (self.board)
        print (self.board.score)
   
    def _setupGame(self):
        """ initialises the game with a board, a starting player and a variable which limits the next board to be played in. """
        self.board = superOXboard()
        self.currentPlayer=self.players[0]
	    self.nextBoard = None

    
    def __str__(self):
        """ Returns the current gameState and possible actions in a human-friendly format"""
	    print(self.board)
        player="X" if self.currentPlayer.index==0 else "O"
        move="can play in any board" if self.nextBoard is none else "must play in board "+self.nextBoard
        print("Current player is "+player+", and they "+move+"\n") 


    def _nextPlayer(self):
        """cycles through list of players """
        m = self.currentPlayer.index
        n = (m+1) % len(self.players)
        return self.players[n]
         

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
        #currently only returning the overall state - need to decide represnetatino to give to bot.
        return self.game.board.state if self._playerX else [-i for i in self.game.board.state] 

    @property
    def actions(self):
        """ a bot-friendly list of possible actions from the point of view of current player"""
        
        return [(b,s) for s, state in enumerate(board.state) if state is None for b,board in enumerate(self.game.board.boards)]   
  
    def prompt(self):
        action = self.bot.promptBot(self)
        if action not in self.actions:
            raise IOError("Invalid action passed to game by" + self)
        return action
