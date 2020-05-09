from Stones import stones
from Stones import Turn


def go():
    InitialWhiteLocations = []
    InitialBlackLocations = []
    turn = Turn.black
    Pass = [False,False]
    score = [6.5,0]
    Board = stones(InitialWhiteLocations, InitialBlackLocations)
    Resign = False
    while False in Pass:
        Pass[turn] = False
        Move = input("Enter you move (Resign = 0,Pass = 1, Place a Stone = 2): ")

        if Move == "2":
            row = input("Enter Stone row:")
            column = input("Enter Stone column:")
            while not Board.AddStone((row,column),turn):
                row = input("Enter Stone row:")
                column = input("Enter Stone column:")
                pass
        elif Move == "1":
            Pass[turn] = True
        elif Move == "0":
            Resign = True
            break
        else:
            print("Wrong Input")
            continue
        LastPlay = (x, y,turn) # White turn = 0 , Black Turn = 0
        turn = 1 - turn
        score, TerrBoard = Board.getScoreAndTerrBoard()
        Board.Drawboard()
        # print(TerrBoard)
        print("Score [White,Black]:",score)

    if score[0] > score[1] or (Resign and turn == 1):
        winner = "White"
    else:
        winner = "Black"

    print(winner,"wins")

    if (Resign):
        return winner

    return score


if __name__ == "__main__":
    go()