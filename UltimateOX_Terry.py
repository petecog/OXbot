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
from bots import isBotsValid
from random import shuffle
from bots import Bot
from bots import RandomBot

class OXboard:
    """ A standard OX board"""
    
    #winning combos based on move just played 
    winning_lines={
        0:((1,2),(3,6),(4,8)),
        1:((0,2),(4,7)),
        2:((0,1),(5,8),(4,6)),
        3:((4,5),(0,6)),
        4:((3,5),(1,7),(0,8),(2,6)),
        5:((3,4),(2,8)),
        6:((7,8),(0,3),(2,4)),
        7:((6,8),(1,4)),
        8:((6,7),(2,5),(0,4))
    }
    win_x=[
        1,None,None,None,1,
        None,1,None,1,None,
        None,None,1,None,None,
        None,1,None,1,None,
        1,None,None,None,1
        ]
    win_o=[
        None,None,1,None,None,
        None,1,None,1,None,
        1,None,None,None,1,
        None,1,None,1,None,
        None,None,1,None,None
        ]
    draw=[
        None,None,0,None,None,
        None,None,0,None,None,
        0,0,0,0,0,
        None,None,0,None,None,
        None,None,0,None,None,
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
        assert square in self.actions, "Not a valid choice of square"
        assert self.score==None, "Attempting to play on a finished board"
        assert player in {1,-1}, "Not a player"
        self.state[square]= player
        self._updateScore(square,player)

    def _updateScore(self,square,player):
        """ Score current board state
         (None for ongoing, 1 for X win, -1 for O win, 0 for draw)
        Does some tricks to speed it up faster than Nick's set based effort.
        Parameters
        ----------
        square : int
            the  square just played from 0 to 8
        player : int 
            either 1 (X) or -1(O)

        """
        if self.state[square]==player: #this is always true for the XO board but not necessarily for the super XO board
            win= any(all(self.state[i]== player for i in line) for line in self.winning_lines[square])
            if win:
                self.score=player
        elif len(self.actions)==0: #draw
            self.score=0
        else:
            self.score=None
        
    @property
    def actions(self):
        """ list of possible moves on board. No moves possible if board has been scored"""
        return [i for i,s in enumerate(self.state) if s is None] if self.score is None else []
    
    def __str__(self):
        """ Returns the current gameState and possible actions in a human-friendly format"""
        rows=[self._printRow(i) for i in range(5)]
        return "\n".join(rows)+"\n"

    def _printRow(self,n):
        """prints the nth row of the board"""
        if self.score is None:
            if n in [1,3]:
                return self._printHorizontalDivide()
            else:
                m=int(n/2 *3)
                row=[self._representation(self.state[i]) for i in range(m,m+3)]
                return "|".join(row)
        elif self.score is 1:
            row=[self._representation(self.win_x[i]) for i in range(5*n,5*n+5)]
            return "".join(row)
        elif self.score is -1:
            row=[self._representation(self.win_o[i]) for i in range(5*n,5*n+5)]
            return "".join(row)
        else:
            row=[self._representation(self.draw[i]) for i in range(5*n,5*n+5)]
            return "".join(row)

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
print("hello")
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
        assert board in self.actions, "Not a valid choice of board"
        assert self.score==None, "Attempting to play in a finished game"
        self.boards[board].play(square,player)
        self.state[board]=self.boards[board].score
        self._updateScore(board,player)

    def _printRow(self,n):
        """prints the nth row of the superboard """
        if n in [1,3]:
            return self._printHorizontalDivide()
        else:
            m=int(n//2*3)
            boards=[self.boards[i] for i in range(m,m+3)]
            rows=[" "+ " || ".join(board._printRow(i) for board in boards) + " " for i in range(5)]
            return "\n".join(rows)

    @staticmethod
    def _printHorizontalDivide():
        blank = "||".join([" "*7]*3)
        divide = "-"*25
        return "\n".join([blank,divide,divide,blank])

class Game:
    """ A SuperOX game with board and 2 players. Player 0 is X, and goes first. """
    numberofPlayers=2

    def __init__(self,bots):
        """checks bots valid and assigns to players (objects within the game) """
        if not isBotsValid(self.numberofPlayers,bots):
            raise ValueError
        self.players=[Player(self,index,bot) for index,bot in enumerate(bots)]
    
    def _shufflePlayers(self):
        """reassign bots to players """
        bots = [player.bot for player in self.players]
        shuffle(bots)
        for i,bot in enumerate (bots):
            self.players[i].bot = bot 

    def _nextPlayer(self):
        """cycles through list of players """
        m = self.currentPlayer.index
        n = (m+1) % len(self.players)
        return self.players[n]

    def playGame(self):
        """ plays the game, repeatedly prompting the current player for their action """
        self._shufflePlayers()
        self._setupGame()    
        
        while(self.board.score is None):
            board,square = self.currentPlayer.prompt() #action is a pair e.g. (2,3) representing square number on superboard and then square number on OX board.
            assert (self.nextBoard is None) or self.nextBoard==board, "Breaking the next board rule"
            self.board.play((board,square),1 if self.currentPlayer.index==0 else -1)
            self.nextBoard = square if self.board.state[square] is None else None
            self.currentPlayer=self._nextPlayer() 
        
        #print(self.board)
        #print(self.board.score)
        return self.board.score
   
    def _setupGame(self):
        """ initialises the game with a board, a starting player and a variable which limits the next board to be played in. """
        self.board = superOXboard()
        self.currentPlayer=self.players[0]
        self.nextBoard = None

    def __str__(self):
        """ Returns the current gameState and possible actions in a human-friendly format"""
        
        player="X" if self.currentPlayer.index==0 else "O"
        move="can play in any board" if self.nextBoard is None else "must play in board "+str(self.nextBoard)
        return(self.board.__str__()+"\n"+"Current player is "+player+", and they "+move+"\n") 
         
class Player:
    """ these are players inside the game. Their bot attribute links to a bot which drives players decisions"""
    def __init__(self,game,index,bot):
        self.game=game
        self.bot=bot
        self.index=index
        
    def __str__(self):
        """ Returns the current game in a human-friendly format"""
        return  self.game.__str__()
    
    @property
    def state(self):
        """ a bot-friendly format of the gameState from the point of view of current player"""
        #currently only returning the overall state - need to decide representation to give to bot.
        return self.game.board.state

    @property
    def openBoards(self):
        """ a list of open boards for current player"""
        return self.game.board.actions if self.game.nextBoard is None else [self.game.nextBoard]
     
    @property
    def actions(self):
        """ a bot-friendly list of possible (board,action) tuples for current player"""
        return [(b,s) for b in self.openBoards for s in self.game.board.boards[b].actions]   
  
    def prompt(self):
        assert len(self.actions)>0, "Playing when there are no possible moves"
        action = self.bot.promptBot(self)
        if action not in self.actions:
            raise IOError("Invalid action passed to game by" + self)
        return action

game=Game([RandomBot("1"),RandomBot("2")])


results=[]
for i in range(1000):
    results.append(game.playGame())
print(results)