from Stones import stones
from Stones import Turn
import os
clear = lambda: os.system('cls') #on Windows System

InitialWhiteLocations = []
InitialBlackLocations = []
turn = Turn.black
Pass = [False,False]

Board = stones(InitialWhiteLocations, InitialBlackLocations)
Resign = False
while False in Pass:
    Pass[turn] = False
    Move = input("Enter you move (Resign = 0,Pass = 1, Place a Stone = 2): ")
    clear()
    if Move == "2":
        x = input("Enter Stone x-cord:")
        y = input("Enter Stone y-cord:")
        # btab2a bel 3aks(y,x) mesh (x,y)
        while not Board.AddStone((y,x),turn):
            x = input("Enter Stone x-cord:")
            y = input("Enter Stone y-cord:")
            pass
    elif Move == "1":
        Pass[turn] = True
    else:
        Resign = True
        break
    LastPlay = (x, y,turn) # White turn = 0 , Black Turn = 0
    turn = 1 - turn
    score, TerrBoard = Board.getScoreAndTerrBoard()
    gameBoard = Board.getBoard()
    print(gameBoard)
    print(TerrBoard)
    print("Score [White,Black]:",score)


if score[0] > score[1] or (Resign and turn == 1):
    winner = "White"
else:
    winner = "Black"

print(winner,"wins")
