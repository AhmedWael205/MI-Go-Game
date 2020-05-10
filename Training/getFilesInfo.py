from SGFReader import iterateOverFiles
from Game.Stones import stones
from FeatureExtractor import extractorFunctions as ef
import numpy as np
import time
import pickle


if __name__ == '__main__':

    i = 7000
    directoryPath = "../SGFReader/SGF2"
    filesInfo = iterateOverFiles.iterateOverFiles(directoryPath)
    modelInput = []  # rows = number of total moves, columns = 2 where col.1 = input state and col.2 = truth value

    border = ef.getBorder()
    positionMask = ef.getPositionMask()

    for match in filesInfo:
        i += 1
        whitePlayerRank = match[0]
        blackPlayerRank = match[1]
        moves = match[2]

        game = stones()

        turn = -1  # Starting turn is black
        start = time.perf_counter()

        for moveIndex, move in enumerate(moves):
            inputState = []

            gameBoard = game.getBoard()
            stoneAge = game.stoneAge
            opponentRank = whitePlayerRank if turn == -1 else blackPlayerRank
            _, terrBoard = game.getScoreAndTerrBoard()

            my1Lib, my2Lib, my3Lib, opp1Lib, opp2Lib, opp3Lib = ef.getLiberties(gameBoard, turn)
            #myKo = ef.getKo(gameBoard, turn, game)

            ourStones, opponentStones, emptyPositions = ef.getStoneOwnership(gameBoard, turn)
            ourStoneHistory, opponentStoneHistory = ef.getStoneHistory(stoneAge, ourStones, opponentStones)
            rank1, rank2, rank3, rank4, rank5, rank6, rank7, rank8, rank9 = ef.getOpponentRank(opponentRank)
            # border and position mask are calculated once before iterating over matches
            ourTerritories, opponentTerritories = ef.getTerriroties(terrBoard, turn)

            inputState.extend([my1Lib, my2Lib, my3Lib, opp1Lib, opp2Lib, opp3Lib])
            #inputState.extend([myKo])
            inputState.extend([ourStones, opponentStones, emptyPositions])
            inputState.extend([ourStoneHistory, opponentStoneHistory])
            inputState.extend([rank1, rank2, rank3, rank4, rank5, rank6, rank7, rank8, rank9])
            inputState.extend([border, positionMask])
            inputState.extend([ourTerritories, opponentTerritories])

            inputState = np.asarray(inputState)

            ourMove, opponentNextMove, ourNextMove = ef.getMoveMade(moveIndex, moves)
            truthValues = [ourMove, opponentNextMove, ourNextMove]
            winner = match[4] * turn

            modelInput.append([inputState, truthValues, winner])

            if move != "pass":
                game.AddStone(move, int(turn == -1))
            turn = -turn
        if i % 300 == 0:
            modelInput = np.asarray(modelInput)
            pickle.dump(modelInput, open("VtrainigData/NoKoTrainingData_"+str(i)+".pkl", "wb"))
            modelInput = []
            print("Saved 50 games")

        if i % 50 == 0:
            print("Game Complete")
            print(match[3])

    i += 1
    modelInput = np.asarray(modelInput)
    pickle.dump(modelInput, open("VtrainigData/NoKoTrainingData_"+str(i)+".pkl", "wb"))
