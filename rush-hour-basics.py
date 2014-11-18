#! /usr/bin/env python
"""
support code for the rush-hour game

ASSUMPTIONS
 1. game file is formatted correctly
 2. goal is always in the 3rd row
 3. empty positions are indicated by '0'

INITIALIZATION
  LOAD-GAME:  Load a game from a file, and create a game instance
  to record all of the information.  
"""

def load_game(filename):
    """Reads filename and returns a list representing the initial state of the game"""
    fin = open(filename)
    nextline = fin.readline()
    maxX, maxY = [int(token) for token in nextline.split()]
    gameArray = []
    for i in range(maxX):
        nextline = fin.readline()
        gameArray.append(nextline.split())
    fin.close()
    print gameArray
    return gameArray


# UTILITIES
# PRINT_BOARD: nicely formats a game board
def print_board(board):
    """pretty print the board"""
    for i in board:
        for j in i:
            print j.rjust(4),
        print

a = load_game("test2.txt")
print_board(a)

# COPY_GAME: lists are mutable in python. sometimes a full copy is needed of a board
def copy_game(alist):
    """alist should be a 2D matrix representing a game state. returns a copy of the game state"""
    newlist = []
    for row in range(len(alist)):
        newlist = newlist + [list(alist[row])]
    return newlist

# EQUAL_GAMES: returns True if two game boards have the same values at all the positions
def equal_games(game1, game2):
    """games are board states, returns True if two game boards have the same values at all the positions"""
    # do they have the same number of rows?
    if len(game1) == len(game2):
        for i in range(len(game1)):
            # do they have the same number of columns?
            if len(game1[i]) == len(game2[i]):
                for j in range(len(game1[i])):
                    # as soon as a position has a different value, they are not equal
                    if game1[i][j] != game2[i][j]:
                        return False
        return True
    else:
        return False

# LEGAL_POSITION: returns True if x y position on the board exists
def legal_position(board, x, y):
    """returns True if (x, y) is on the board""" 
    return x >= 0 and y >= 0 and x < len(board) and y < len(board[0])

# EMPTY: check to see if an x y position on the board exists and is empty
#        returns True or False
def empty(board, x, y):
    """returns True if the (x, y) position on the board is empty"""
    if legal_position(board, x, y):
        if board[x][y] == '0':
            return True
    return False

# AT_GOAL: checks whether a board is actually at the goal state
#          i.e., g is at the rightmost column
def at_goal(board):
    """returns True if goal is in the rightmost column"""
    return board[2][len(board[2]) - 1] == 'g'

## SEARCH CODE

# Top Level function is RushHour which takes a game file and a string indicating whether to use dfs or bfs
# def RushHour(filein, which):
#     game = load_game(filein)
#     if which == 'dfs':
#         <fill in here>
#     elif which == 'bfs':
#         <fill in here>

#if __name__ == '__main__' :
#     RushHour('test1.txt', 'dfs')
    
