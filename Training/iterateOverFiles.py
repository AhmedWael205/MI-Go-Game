import os
from SGFReader import readSGF

filesInfo = []

def iterateOverFiles(directorypath):

    i=0

    for filename in os.listdir(directorypath):
        i+=1
        filepath = directorypath + "/" + filename
        # fileReader = open(filepath, "r")
        # fileContents = fileReader.read()
        # fileReader.close()

        invalidFile, whitePlayerRank, blackPlayerRank, playersMoves, winner = readSGF.readSGF(filepath)
        #readSGF.CopyValidSGF(filepath, directorypath,i)
        if not invalidFile:
            if winner == "W":
                winner = 1
            elif winner == "B":
                winner = -1
            else:
                print("hello")
            filesInfo.append((whitePlayerRank, blackPlayerRank, playersMoves, filename, winner))
    return filesInfo

