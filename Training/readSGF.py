import shutil

def readSGF(filepath):

    #Read .sgf file
    file = open(filepath, "r")
    rawFileContents = file.read()[2:-2]
    file.close()

    #Split file contents into setup info and moves
    gameSetupInfo = rawFileContents.split(";")[0].split("\n")
    gameMoves = rawFileContents.split(";")[1:]

    whitePlayerRank = 0
    blackPlayerRank = 0
    winner = "NA"
    playersMoves = []
    invalidFile = False

    for index, info in enumerate(gameSetupInfo):
        if "WR" == info[0:2]:
            whitePlayerRank = ord(info[3]) - ord('0')
        elif "BR" == info[0:2]:
            blackPlayerRank = ord(info[3]) - ord('0')
        elif "RU" == info[0:2]:
            if not ("Chinese" in info):
                invalidFile = True
                return (invalidFile, whitePlayerRank, blackPlayerRank, playersMoves, winner)
        elif "AB" == info[0:2]:
            invalidFile = True
            return (invalidFile, whitePlayerRank, blackPlayerRank, playersMoves, winner)
        elif "RE" == info[0:2]:
            winner = info[3]

    if winner == "NA":
        invalidFile = True
        return (invalidFile, whitePlayerRank, blackPlayerRank, playersMoves, winner)

    for move in gameMoves:
        if "W" == move[0] or "B" == move[0]:
            if move[2] == "]":
                playersMoves.append("pass")
            else:
                column = ord(move[2]) - ord('a')
                row = ord(move[3]) - ord('a')
                playersMoves.append((row, column))

    return (invalidFile, whitePlayerRank, blackPlayerRank, playersMoves, winner)


def CopyValidSGF(filepath, directorypath, i):

    #Read .sgf file
    file = open(filepath, "r")
    rawFileContents = file.read()[2:-2]
    file.close()

    #Split file contents into setup info and moves
    gameSetupInfo = rawFileContents.split(";")[0].split("\n")
    gameMoves = rawFileContents.split(";")[1:]

    whitePlayerRank = 0
    blackPlayerRank = 0
    playersMoves = []
    invalidFile = False

    for index, info in enumerate(gameSetupInfo):
        if "WR" == info[0:2]:
            whitePlayerRank = ord(info[3]) - ord('0')
        elif "BR" == info[0:2]:
            blackPlayerRank = ord(info[3]) - ord('0')
        elif "RU" == info[0:2]:
            if not ("Chinese" in info):
                return
        elif "AB" == info[0:2]:
            return

    shutil.move(filepath, directorypath+"/valid")

    return