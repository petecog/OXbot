#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 20:15:00 2020
An OX "exploration" game. Initialised in any non-terminal state. Next player chosen randomly.

An OX game object has:
1. a board of 9 squares (X, O, None for blank)
2. A score (None for ongoing, 1 for X win, -1 for O win, 0 for draw)
3. A play method to update the board and score
4. A view method to view the board etc.

Player objects are prompted for actions, can view gamestate and return actions

The interface uses the normal format for reinforcement learning: 
- A game has a series of states S, and sets of actions A_s available in each state. 
- A player has a policy P (P_s for all s in S) which defines the probability of choosing each action in A_s. 
- Upon choosing an action A, the game returns a reward R(S,A) and a new state.

Background notes on RL (not needed to code the game)
- A state value V_s is the expected value of all rewards from this state forwards. This is for a given policy.
- An optimal policy is a policy which maximises the state value.
- RL iteratively improves policy by estimating values through repeatedly playing games, and changing the policy to pick the actions which lead to the highest reward + next state value. 


Notes for XO RL learning
- reward function is 1 for winning the game, -1 for losing or a draw. 0 for all interim states. The reason a draw is a zero is so the game representation can be denoted as (X state value, Y state value) to disitnguish open but equal boards from likely to draw boards


@author: terrylines
"""


# ##### 
# TO DO - GET STATE VALUES EVEN WHEN ITS NOT YOUR TURN.


from bots import isBotsValid
from random import shuffle
from random import choice
# from bots import Human
# from bots import RandomBot

class OXboard:
    """ A standard OX board"""
  
    winning_lines={
        (0,1,2),(3,4,5),(6,7,8),
         (0,3,6),(1,4,7),(2,5,8),
         (0,4,8),(2,4,6)
         }

    def __init__(self,state=[None]*9):
        """ Initialises a  board """
        self.state=state
        self.score=None
        self._updateScore()

    
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
        self._updateScore()

    def _updateScore(self):
        """ Score current board state
         (None for ongoing, 1 for X win, -1 for O win, 0 for draw)
        """
        x_win= any(all(self.state[i]== 1 for i in line) for line in self.winning_lines)
        o_win= any(all(self.state[i]== -1 for i in line) for line in self.winning_lines)
        # assert not (x_win and o_win), "Somehow both players have won the board"  #we don't want this as we are going to generate random boards that might trip this.
        draw= not x_win and not o_win and len(self.actions)==0
        if x_win:
            self.score=1
        elif o_win:
            self.score=-1
        elif draw:
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
        if n in [1,3]:
            return self._printHorizontalDivide()
        else:
            m=int(n/2 *3)
            row=[self._representation(self.state[i]) for i in range(m,m+3)]
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

class Game:
    """ A OX game with board and 2 players. Player 0 is X """
    numberofPlayers=2

    def __init__(self,bots,randomTurn=True):
        """checks bots valid and assigns to players (objects within the game) """
        if not isBotsValid(self.numberofPlayers,bots):
            raise ValueError
        self.players=[Player(self,index,bot) for index,bot in enumerate(bots)]
        self.randomTurn=randomTurn
    
    # def _shufflePlayers(self):
    #     """reassign bots to players """
    #     bots = [player.bot for player in self.players]
    #     shuffle(bots)
    #     for i,bot in enumerate (bots):
    #         self.players[i].bot = bot 

    def _nextPlayer(self):
        """cycles through list of players """
        if self.randomTurn:
            return choice(self.players)
        else:
            m = self.currentPlayer.index
            n = (m+1) % len(self.players)
            return self.players[n]

    def playGame(self,board=None,starting_player=None):
        """ plays the game, repeatedly prompting the current player for their action """
        # self._shufflePlayers()
        # allowing us to return score for bot 0 perspective
        self._setupGame(board,starting_player)    
        
        while(self.board.score is None):
            square = self.currentPlayer.prompt() #action is a square number on OX board.  #need to also get prompts and values when its not your turn.
            self.board.play(square,1 if self.currentPlayer.index==0 else -1)
            self.currentPlayer=self._nextPlayer() 
        
        #print(self.board)
        #print(self.board.score)
        return self.board.score
   
    def _setupGame(self,board=None,starting_player=None):
        """ initialises the game with a board and a starting player.
        Parameters
        ----------
        board : list
            the  starting state. randomly chosen if none
        player : int 
            either 0 (X) or 1(O) (refers to the player index)
        """
        valid=False
        if board is not None:
            self.board = OXboard(board)
            valid =self.board.score is None
            assert valid, "Invalid board given"

        while not valid:
            board = [choice([1,-1,None]) for square in range(9)]
            self.board = OXboard(board)
            valid = self.board.score is None
            
        self.currentPlayer=choice(self.players) if starting_player is None else self.players[starting_player]

    def __str__(self):
        """ Returns the current gameState and possible actions in a human-friendly format"""
        
        player="X" if self.currentPlayer.index==0 else "O"
        return(self.board.__str__()+"\n"+"Current player is "+player+"\n") 
         
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
        #currently returning the overall state and next player- need to decide representation to give to bot.
        state= self.game.board.state
        player = self.game.currentPlayer.index
        
        return state if player==0 else [- s if s is not None else s for s in state]


    @property
    def actions(self):
        """ a bot-friendly list of possible actions for current player"""
        return self.game.board.actions   
  
    def prompt(self):
        # assert len(self.actions)>0, "Playing when there are no possible moves"
        action = self.bot.promptBot(self)
        # if action not in self.actions:
        #     raise IOError("Invalid action passed to game by" + self)
        return action

# game=Game([RandomBot("1"),RandomBot("2")])


# results=[]
# for i in range(1000):
#     results.append(game.playGame())
# print(results)