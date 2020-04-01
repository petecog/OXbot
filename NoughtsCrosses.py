#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 20:49:00 2020

@author: terrylines
"""

class Board:
 
    def __init__(self,state=[0,0,0,0,0,0,0,0,0],playerX=True):
        self.state=state     #board is a 9-list with 1 for own pieces, 0 for blank squares, and -1 for opponent pieces
        self.playerX=playerX  #player 
    
    def __str__(self):
        def row(values):
            tile_image = ('O',' ','X') if self.playerX else ('X',' ','O')
            tiles = [tile_image[i+1] for i in values] 
            return '|'.join(tiles) + '\n'
        blankrow = '-----\n'
        grid = blankrow.join( [row(self.state[3*i:3*i+3]) for i in range(0,3) ] )
        player = "Current Player is " + ('X' if self.playerX else 'O') + '\n'
        return  grid + player
    
    def actions(self):
        return [i for i, x in enumerate(self.state) if x == 0]
    
    def play(self,value):
        if value in self.actions():
            self.state[value] = 1
            return True
        else:
            return False
    
    def nextTurn(self):
        self.state = [-i for i in self.state]
        self.playerX = not self.playerX
        return

class Game:
        
    def __init__(self):
        self.board=Board(state=[0,0,0,0,0,0,0,0,0],playerX=True)
      
    def __str__(self):
        return self.board.__str__()
    
    def playGame(self):
        while(True):
            action=int(self.promptPlayer())
            if self.board.play(action):
                if self.isDone():
                    break
                else: self.board.nextTurn() 
            else:
                print("invalid move\n")
        
        return self.getWinner()
        
        
    
    def promptPlayer(self):
        print(self)       
        return input('Choose your move from ' + ','.join([str (i) for i in self.board.actions()]) + '\n')
    
    def isDone(self):
        return not self.board.actions or self.hasWon()
        
    def hasWon(self):
        #only checks for current player who has just moved.
        winningLines=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        return any ( [all([self.board.state[i]==1 for i in line]) for line in winningLines] )

    
    def getWinner(self):
        if self.hasWon():
            result =  "X wins" if self.board.playerX else "O wins"
        else:
            result = "draw"
        return result

Game().playGame()

