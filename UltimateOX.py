#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 20:15:00 2020
Ultimate OX Game class pseudo code

Summary of game structure
An OX game object has:
1. a board of 9 squares
   (1 for X, -1 for O, None for blank (None is specific python datatype))
2. A score (None for ongoing, 1 for X win, -1 for O win, 0 for draw)
3. A play method to update the board and score
4. A view method to view the board etc.


An ultimate OX game object has:
1. A set of 9 OX game objects
2 A superboard of 9 squares containing the score from each OX game.
3. A score for the overall game
   (None for ongoing, 1 for X win, -1 for O win, 0 for draw)
4. A nextsquare attribute which limits the choice of square for the next player
5. Play and view methods that call the methods from the OX board.
6. 2 player objects

Player objects are prompted for actions, can view gamestate and return actions

The interface uses the normal format for reinforcement learning:
- A game has a series of states S, and sets of actions A_s available in
  each state.
- A player has a policy P (P_s for all s in S) which defines the probability
  of choosing each action in A_s.
- Upon choosing an action A, the game returns a reward R(S,A) and a new state.

Background notes on RL (not needed to code the game)
- A state value V_s is the expected value of all rewards from this state
  forwards. This is for a given policy.
- An optimal policy is a policy which maximises the state value.
- RL iteratively improves policy by estimating values through repeatedly
  playing games, and changing the policy to pick the actions which lead to
  the highest reward + next state value.

Ultimate OX rules
X goes first
3x3 superBoard. each square containing a standard 3x3 OX board.
A player chooses a square on the superBoard, then makes a standard
  move on that XO board.
If the OX board is won, it is marked for that player on the superBoard
If available, the next player must choose the square on the superBoard that has
  the same position as the prior player's move on the XO board. If that square
  is not available, the next player can choose from any available square
A square is not available if it has been marked for either player,
  or it has no remaining moves (it is still available if there are
  no winning moves for either player). Note: some variants allow further
  moves even if a square has already been marked.
Available: None
Not available: 0
Marked for X: 1
Marked for O: -1
A player wins by having 3 in a row on the superboard.
If there are no available squares, the game is a draw.

Notes for ultimate XO RL learning
- reward function is 1 for winning the game, 0 for a draw,
  -1 for losing. 0 for all interim states.


@author: terrylines
"""
from bots import isBot, Bot, Human, RandomBot
from random import shuffle


class Game:
    """Everything to do with Mega Noughts and Crosses."""

    def __init__(self, bots):
        """Check bots are valid and assigns to Players
        (objects within the game).
        """
        if not self._isValid(bots):
            raise ValueError
        self.players = [Player(self, index, bot)
                        for index, bot in enumerate(bots)]
        self._setupGame()

    def _setupGame(self):
        """Initialise the game."""
        self.boards = [Board() for i in range(9)]
        # list length 9 with
        #   1 for squares marked for player 1 (X)
        #   0 for unmarked unavailable squares,
        #   -1 for square marked for player 2 (O),
        #   None for available squares
        self._superboard = [board.score for board in self.boards]
        self.currentPlayer = self.players[0]
        # square number that must be played in, or None if can be freely chosen
        self.nextSquare = None
        # score is None if ongoing, 1 for player 1, 0 for draw -1 for player 2
        self.score = None
        self.actions = self._legalMoves()
        self.botActions = self._legalBotMoves()

    def _isValid(self, bots):
        """Check the bots are the correct class and number for the game."""
        if all([isBot(bot) for bot in bots])\
                    and self._isCorrectNumberOfBots(len(bots)):
            return True
        return False

    def _isCorrectNumberOfBots(self, numberOfBots):
        """Return whether the number of bots is valid for the game."""
        return numberOfBots == 2

    def _shufflePlayers(self):
        """Reassign bots  to players."""
        bots = [player.bot for player in self.players]
        shuffle(bots)
        for i, bot in enumerate(bots):
            self.players[i].bot = bot

    def playGame(self):
        """Play the game, prompting the current player for their action."""
        self._shufflePlayers()
        self._setupGame()

        while(self.score == None):
            action = self.currentPlayer.prompt()
            # action is a pair e.g. (2,3)
            # representing square number on superboard
            # and then square number on OX board.
            self._play(action)
            self.currentPlayer = self._nextPlayer()
        print(self)
        

    def _play(self, action):
        """Apply the action to the current game

        Argument: action is a tuple (n,m) n is position on superboard
                                          m is position on miniboard
        """
        superboardMove, oxboardMove = action

        if superboardMove not in self.actions:
            raise "That can't be played on the superboard"
        oxboard = self.boards[superboardMove]
        if oxboardMove not in oxboard.actions:
            raise "That can't be played on the OX board"

        # update the relevant OX board to mark the move
        oxboard.play(oxboardMove, self.currentPlayer)

        # update that board status on the superboard
        #   1 if won by X
        #   -1 if won by O
        #   0 if drawn
        #   None if available
        self._superboard[superboardMove] = oxboard.score

        # update the game score
        self.score = self._score()

        # update the nextSquare that must be played in.
        if self.boards[oxboardMove].actions:
            self.nextSquare = oxboardMove
        else:
            self.nextSquare = None

        # update actions
        self.actions = self._legalMoves()
        self.botActions = self._legalBotMoves()

    def _legalMoves(self):
        """Return available actions for superboard."""
        if self.nextSquare is not None:
            return [self.nextSquare]
        else:
            return [i for i, x in enumerate(self._superboard) if x is None]

    def _legalBotMoves(self):
        """Return available actions as a bot would need them.
        
        In the form (m, n) where m is the superboard move
        and n is the OX board move.
        """
        botMoves = []
        for superAction in self.actions:
            for oxAction in self.boards[superAction].actions:
                botMoves.append((superAction, oxAction))
        return botMoves

    def __str__(self):
        """Return text string of the superboard, summary of superboard
        and possible actions."""
        def singleLine(row, bigRow):
            return " || ".join(
                [board.line(row) for board in self.boards
                 [3 * bigRow: 3 * bigRow + 3]])

        def threeLines(bigRow):
            return "\n----- || ----- || -----\n".join(
                [singleLine(i, bigRow) for i in range(3)])

        superboard = "\n======≠≠=======≠≠======\n".join(
            [threeLines(j) for j in range(3)])

        def overviewText(score, size):
            return {-1: "O",
                    0: "#",
                    1: "X",
                    None: " "}[score] * size

        def singleLineOverview(bigRow, size):
            return "  " + " | ".join(
                [overviewText(score, size) for score in self._superboard
                 [3 * bigRow: 3 * bigRow + 3]])

        def bigLineOverview(bigRow, size):
            return "\n".join(
                [singleLineOverview(bigRow, size)] * size)

        size = 2
        delimiter = "\n" + " " * size + "-" * 3 * (size + 2) + "\n"
        overview = delimiter.join([bigLineOverview(j, size) for j in range(3)])

        availableBoards = ", ".join([str(action) for action in self.actions])
        availableBoards = "\n\nAvailable boards: " + availableBoards
        finished = ""
        if self.score == 1:
            finished = "\n\nGame is over. Player X won"
        elif self.score == -1:
            finished = "\n\nGame is over. Player O won"
        elif self.score == 0:
            finished = "\n\nGame is over. Draw"

        return overview + "\n\n" + superboard + availableBoards + finished

    def _score(self):
        """Return the final outcome as below.

                1       -   X wins,
                -1      -   O,
                0       -   draw,
                None    -   unfinshed
                """
        winningLines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
                        (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

        def match(n):
            return any([all([self._superboard[i] == n for i in line])
                       for line in winningLines])
        if match(1):
            return 1
        elif match(-1):
            return -1
        elif len(self._legalMoves()) == 0:
            return 0
        else:
            return None

    def _isFinished(self):
        """Indicate if the games is finished."""
        return not self.currentPlayer.actions or any(self._getScores())

    def _nextPlayer(self):
        """Cycle through list of players."""
        m = self.currentPlayer.index
        n = (m+1) % len(self.players)
        return self.players[n]


class Board:
    """
    This is a standard Noughts and Crosses board.

    Board is a 9-list with 1 for X, -1 for O and False for neither.
    """

    def __init__(self):
        """Initialise board."""
        self.board = [None] * 9  # board is a 9-list
        self.score = None  # 1 means X has won, -1 means O has won
        self._visualiser = {-1: "O",
                            None: " ",
                            1: "X"}  # dictionary for translating to readable
        self.actions = self._legalMoves()

    def _makeString(self, inp):
        """Return a list of readable strings from a list of game states.

        Turns -1 to X, 1 to 0 and None to " "
        """
        return [self._visualiser[x] for x in inp]

    def __str__(self):
        """Return visual representation of board."""
        a = ["|".join(self._makeString(self.board[i * 3: i * 3 + 3]))
             for i in range(3)]
        return "\n-----\n".join(a)

    def line(self, num):
        """Return a string of letters representing the
        num'th line of the board for the main board to print.
        """
        return "|".join(self._makeString(self.board[num * 3: num * 3 + 3]))

    def play(self, action, player):
        """
        Mark the board in square 'action' with 'player'
        and update the board score.
        """
        if action not in self.actions:
            raise "Illegal Move"
        if self.score is not None:
            raise "Game finished"
        if player._playerX:
            self.board[action] = 1
        else:
            self.board[action] = -1
        self.score = self._score()
        self.actions = self._legalMoves()

    def _score(self):
        """
        Check if there is a winning line and update score to
        1 if X has won or -1 if O.
        If the grid is full, update score to 0
        """
        winningLines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
                        (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

        def match(n):
            return any([all([self.board[i] == n for i in line])
                       for line in winningLines])

        if match(1):
            return 1
        elif match(-1):
            return -1
        elif len(self._legalMoves()) == 0:
            return 0
        else:
            return None

    def _legalMoves(self):
        """Return a list of available squares which can be used as actions."""
        if self.score is None:
            return [i for i, x in enumerate(self.board) if x is None]
        else:
            return []


class Player:
    """These are players inside the game. Their bot attribute links
    to a bot which drives players decisions
    """

    def __init__(self, game, index, bot):
        """Set up player."""
        self.game = game
        self.bot = bot
        self.index = index  # 0 is first player, 1 is second etc
        self._setup()

    def _setup(self):
        """Set up the player with game specific attributes."""
        self._playerX = self.index == 0
        pass

    def __str__(self):
        # Ask Terry about this
        """Return the current game in a human-friendly format."""
        return self.game.__str__

    @property  # Ask Terry what this means
    def state(self):
        """Return a bot-friendly format of the gameState
        from the point of view of current player playing as X.
        """
        # Ask Terry what the point of this whole bit is
        return self.game.board if self._playerX else [-i for
                                                      i in self.game.boards]

    @property
    def actions(self):
        """Return a bot-friendly list of possible actions from
        the point of view of current player.
        """
        # Needs to be written
        # return [i for i, x in enumerate(self.game.boards) if x == 0]

    def prompt(self):
        """Send game to bot for action. Bot returns action. Return action."""
        action = self.bot.promptBot(self.game)
        print(self.bot.name + " just played at")
        print(action)
        if action[0] not in self.game.actions:
            raise IOError("Invalid action passed to game by" + self)
        return action


mikey = Human("Mikey")
enemy = RandomBot("Enemy")
g = Game((mikey, enemy))
g._superboard = [1,0,None,-1,-1,-1,None,None, None]
g.playGame()
