from Stones import stones
from Stones import Turn
import os
clear = lambda: os.system('cls') #on Windows System

InitialWhiteLocations = []
InitialBlackLocations = []
turn = Turn.black
Pass = [False,False]

Board = stones(InitialWhiteLocations, InitialBlackLocations)

while False in Pass:
    Pass[turn] = False
    Move = input("Enter you move (Resign = 0,Pass = 1, Place a Stone = 2): ")
    clear()
    if Move == "2":
        while not Board.AddStone((input("Enter Stone x-cord:"),input("Enter Stone y-cord:")),turn):
            pass
    elif Move == "1":
        Pass[turn] = True
    else:
        break

    turn = 1 - turn

score = Board.Score()
print("Score [White,Black]:",score)
if score[0] > score[1]:
    print("White wins")
else:
    print("Black wins")