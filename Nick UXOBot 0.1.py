# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 10:28:29 2020

@author: NickHare
"""


# Nick's UXOBot Program

# This approach uses sets of numbers to represent a game of UXOBot.
# Each number in a particular game can be interpreted as a square in a game
# of noughts-and-crosses. The moves a player has taken correspond to a set of 
# numbers that belong to that player. For example, if I take the centre 
# square in a game (square 0), the number 0 is removed from the 'available'
# set to my personal set for that game.

# The mapping of numbers to squares is as follows:
# 
#    3 | -4 |  1
#  --------------
#   -2 |  0 |  2
#  --------------
#   -1 |  4 | -3

# This has the particular property that if you have a set of three numbers in
# your set that sum to 0, this is a winning line. All and only sets of three
# numbers that sum to 0 are winning positions in noughts-and-crosses. 

# Imports
import itertools # Used for generating subsets
import numpy as np # Used for the product function and maybe other things
# import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator # Used for tickmarks, grid etc.
import random # Used to shuffle board and to make random moves
import math # For various things
# %matplotlib inline

# matplotlib.use('TkAgg') # Needed to make it show plots maybe?
random.seed() # Set random seed to system time

# Functions
def victory_check(numbers):
    # Takes a set of numbers and returns True / False depending on whether it's a 
    # winning set, by multiplying together all the sums of the size-3 subsets
    # and checking whether they're equal to 0.
    return np.prod([sum(i) for i in itertools.combinations(numbers, 3)]) == 0

def printx(x, y, scale): #prints a red 'X' at the appropriate scale
    ax = plt.gcf().gca() # Try removing this later - gets current axis, but might not need
    plt.plot([x - 0.35 * scale, x + 0.35 * scale], [y - 0.35 * scale, y + 0.35 * scale], color = 'r', lw = 3 * scale)
    plt.plot([x - 0.35 * scale, x + 0.35 * scale], [y + 0.35 * scale, y - 0.35 * scale], color = 'r', lw = 3 * scale)
    return 

def printo(x, y, scale): #prints a blue 'O' at the appropriate scale
    ax = plt.gcf().gca() # Try removing this later - gets current axis, but might not need
    circle = plt.Circle((x, y), 0.4 * scale, color = 'b') # Blue circle
    ax.add_artist(circle) 
    circle = plt.Circle((x, y), 0.3 * scale, color = 'w') # Smaller white circle
    ax.add_artist(circle)        
    return 

def xcoord(n): #returns x co-ord (0, 1, 2) of number
    return [1, 2, 0, 0, 1, 2, 2, 0, 1][n + 4]

def ycoord(n): #returns y co-ord (0, 1, 2) of number
    return [2, 0, 1, 0, 1, 2, 1, 2, 0][n + 4]

def setnumber(x, y): #returns a square index from an x and y co-ord
    return [[-1, 4, -3], [-2, 0, 2], [3, -4, 1]][y][x]


# Classes
class Gamestate: # Describes the state of the 'board', and whose turn it is
    
    def __init__(self):
        # Initialises the sets - 10 sets (one master, 9 sub-boards) for available, X, and O
        setlist = [] # An empty list that will be three sets: remaining, X and O
        setlist.append([set(range(-4, 5)) for i in range(10)]) # All numbers are in the available set to begin with
        for i in range(2):
            setlist.append([set() for j in range(10)]) #Two sets of 10 empty sets for each player
        self.player = 0 # X to take the first move
        self.board = setlist
        return
               
        
    def render(self):
        # Draws a picture of the board; say whose turn it is
        
        # First draw the empty board
        x = self.board[1]
        o = self.board[2]
        fig = plt.figure(figsize = [.5, .5])
        ax = plt.axes([-0.5, -0.5, 8.5, 8.5])
        ax.set_xlim([0.5, 9.5])
        ax.set_ylim([0.5, 9.5])
        ax.set_xticks(range(1, 10))
        ax.set_yticks(range(1, 10))
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.xaxis.set_minor_locator(MultipleLocator(0.5))
        ax.yaxis.set_minor_locator(MultipleLocator(0.5))
        plt.grid(which = 'minor', axis = 'both')
        plt.axvline(x = 3.5, color='grey')
        plt.axvline(x = 6.5, color='grey')
        plt.axhline(y = 3.5, color='grey')
        plt.axhline(y = 6.5, color='grey')
        
        # Now add the xs and os
        for i in enumerate(x[1:], start = -4): #This is a list of the 9 sub-games
            for j in i[1]: #This iterates over each set
                printx(3 * xcoord(i[0]) + xcoord(j) + 1, 3 * ycoord(i[0]) + ycoord(j) + 1, 1)
        
        for i in enumerate(o[1:], start = -4): #This is a list of the 9 sub-games
            for j in i[1]: #This iterates over each set
                printo(3 * xcoord(i[0]) + xcoord(j) + 1, 3 * ycoord(i[0]) + ycoord(j) + 1, 1)
    
        for j in x[0]: #The big boards - scale 3
            printx(3 * xcoord(j) + 2, 3 * ycoord(j) + 2, 3)
        
        for j in o[0]:
            printo(3 * xcoord(j) + 2, 3 * ycoord(j) + 2, 3)
        
        plt.show()
        
        return
    
    def shuffle_board(self): # Temporary function to test rendering
        a = self.board
        for i in enumerate(a[0]): # A list of the subsets including the big game
            for j in i[1].copy(): # Each item (number) in turn; i[1] is set number i[0]  
                r = random.random()
                if r < (1/3):
                    i[1].remove(j)
                    a[1][i[0]].add(j)
                if r > (2/3):
                    i[1].remove(j)
                    a[2][i[0]].add(j)
        return
    
    def printout(self):
        print(self.board)
        return
    
    def update(self, which_set, which_number): #processes a new proposed move (set, number) by the active player and updates the gamestate
        # Returns: -1 = illegal move, 0 = process is fine (gamestate updated correctly), 1 = victory for the active player
        a = self.board[0] # The sets with the available numbers in them; set 0 is the master board
        b = self.board[self.player + 1] # The set belonging to the active player
        
        # Check for errors: #TIDY THIS UP
        if which_set < -4 or which_set > 4: # illegal set
            return -1
        if not (which_number in a[which_set + 5]): # move already taken
            return -1
        if not (which_set in a[0]): # the move is in a sub-board that's already been won
            return -1
        
        # Change the relevant set
        a[which_set + 5].remove(which_number) # Take the number out of the available set
        b[which_set + 5].add(which_number) # Add the number into the player's set
        
        # Check for victory using the relevant set
        if victory_check(b[which_set + 5]): # Check for victory in the set that's just been changed
            a[0].remove(which_set) # Take that big square out of available
            b[0].add(which_set) # Add that big square to the active player's set
        
        # Check for whole-game victory
        if victory_check(b[0]): # Check for victory in the big set
            return 1
        
        # Remove big board if small set is full (i.e. draw) completed
        if a[which_set + 5] == set() and which_set in a[0]:
            a[0].remove(which_set)
        
        # Check for a draw
        if a[0] == set():
            return 0.5 
        
        self.player = 1 - self.player # Change active player
        return 0

class Moses: # A referee that sets up and can run a game; 

    def __init__(self, players, render): # Players is a list of 2 player IDs; 
    # Normally the UIDs of bots; an index of 0 indicates a human
    # Temporarily, bot ID 1 returns a random move    
    # render = 1 / 0 depending on whether the game should be rendered for debugging etc.    
        self.game = Gamestate() # Sets up a gamestate
        self.players = players # List of 2 player IDs
        self.rend = render # Whether or not it is supposed to render
        self.winner = self.rungame()
        self.hello = 'hello'
           
    def rungame(self): # Administers the game until victory achieved; returns 0 / 1 for winning player, or -1 for a draw
        
        if self.players[self.game.player] == 0: #human player
            move = self.askhuman()
        
        if self.players[self.game.player] == 1: #random player
            move = self.random_move()

        if self.players[self.game.player] > 2:
            move = self.askbot(self.game.player)
        
        result = self.game.update(move[0], move[1])
        
        if self.rend == 1:
                print(move)
                self.game.render()
        
        if result == 1: # Game has ended with a victory 
            return self.game.player
        
        if result == 0.5: # Game has ended with a draw
            return -1
        
        if result == -1:
            print('Illegal move')
        
        return self.rungame() # If not, carries on playing
                    
    def askhuman(self): # Asks a human for input
        self.game.render()
        m = input("Please enter move for " + ['X', 'O'][self.game.player] + " as a 2-digit number xy: ")
        if m == 'exit':
            return
        x = int(m[0])
        y = int(m[1])
        bigx = math.floor((x - 1) / 3)
        bigy = math.floor((y - 1) / 3)
        smx = x - 3 * bigx - 1
        smy = y - 3 * bigy - 1
        return (setnumber(bigx, bigy), setnumber(smx, smy)) # Returns a set and a number reference        
    
    def askbot(self, botid): # Asks a bot for a move
        move = Bot(botid).respond(a)
        return move
        
    def random_move(self): # Picks a move at random
        # pick a random object from the first set
        a = random.choice(list(self.game.board[0][0])) # picks an available master board
        b = random.choice(list(self.game.board[0][a + 5])) # picks a number on that board
        return (a, b)
    
    
# class Bot(): # A machine that takes a gamestate, and returns a set / number combination
    # def respond(): # Provide a move for a given gamestate

# resulto = []
# for i in range(1000):
#     resulto.append(Moses([1, 1], 0).winner)
    
# print(resulto)
# print('X ' + sum([int(i) == 0 for i in resulto]))
# print('O ' + sum([int(i) == 1 for i in resulto]))
    
print(Moses([1, 1], 1).winner)










