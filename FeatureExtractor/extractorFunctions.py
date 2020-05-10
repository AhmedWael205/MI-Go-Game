import numpy as np
import copy
import concurrent.futures
from Stones import stones
import time


def getKo(board, turn, game: stones):
    start = time.perf_counter()
    ko = np.zeros((19, 19), dtype=int)
    # ko = np.asarray([[game.checkKo((i, j), int(turn == -1)) if board[i][j] == 0 else 0 for i in range(19)] for j in range(19)])
    results = []
    with concurrent.futures.ProcessPoolExecutor() as ex:
        for i in range(19):
            for j in range(19):
                results.append([ex.submit(game.checkKo, (i, j), int(turn == -1))])
    k = 0
    for i in range(19):
        for j in range(19):
            ko[i][j] = int(results[k][0].result())
            k += 1
    # print(time.perf_counter()- start)

    return ko


def getLiberties(board, turn):
    bLiberties = np.zeros((19, 19), dtype=int)
    wLiberties = np.zeros((19, 19), dtype=int)

    b1Liberties = np.zeros((19, 19), dtype=int)
    w1Liberties = np.zeros((19, 19), dtype=int)

    b2Liberties = np.zeros((19, 19), dtype=int)
    w2Liberties = np.zeros((19, 19), dtype=int)

    b3Liberties = np.zeros((19, 19), dtype=int)
    w3Liberties = np.zeros((19, 19), dtype=int)

    for i in range(19):
        for j in range(19):

            if board[i][j] == 1:

                if i - 1 >= 0:
                    above = int(board[i - 1][j] == 0)
                else:
                    above = 0
                if i + 1 < 19:
                    below = int(board[i + 1][j] == 0)
                else:
                    below = 0
                if j + 1 < 19:
                    right = int(board[i][j + 1] == 0)
                else:
                    right = 0
                if j - 1 >= 0:
                    left = int(board[i][j - 1] == 0)
                else:
                    left = 0

                wLiberties[i][j] = above + below + right + left

            if board[i][j] == -1:

                if i - 1 >= 0:
                    above = int(board[i - 1][j] == 0)
                else:
                    above = 0
                if i + 1 < 19:
                    below = int(board[i + 1][j] == 0)
                else:
                    below = 0
                if j + 1 < 19:
                    right = int(board[i][j + 1] == 0)
                else:
                    right = 0
                if j - 1 >= 0:
                    left = int(board[i][j - 1] == 0)
                else:
                    left = 0

                bLiberties[i][j] = above + below + right + left

    w1Liberties = (wLiberties == 1).astype(int)
    w2Liberties = (wLiberties == 2).astype(int)
    w3Liberties = (wLiberties >= 3).astype(int)

    b1Liberties = (bLiberties == 1).astype(int)
    b2Liberties = (bLiberties == 2).astype(int)
    b3Liberties = (bLiberties >= 3).astype(int)

    if turn == -1:
        return b1Liberties, b2Liberties, b3Liberties, w1Liberties, w2Liberties, w3Liberties
    else:
        return w1Liberties, w2Liberties, w3Liberties, b1Liberties, b2Liberties, b3Liberties


def getStoneOwnership(gameBoard, turn):
    ourStones = (np.asarray(gameBoard) == turn).astype(int)
    opponentStones = (np.asarray(gameBoard) == -turn).astype(int)
    emptyPositions = (np.asarray(gameBoard) == 0).astype(int)
    return ourStones, opponentStones, emptyPositions


def getStoneHistory(stoneAge, ourStones, opponentStones):
    ourStoneHistory = stoneAge * ourStones
    Empty = (ourStoneHistory == 0)
    ourStoneHistory[Empty] = 10000
    ourStoneHistory -= 1

    opponentStonHistory = stoneAge * opponentStones
    Empty = (opponentStonHistory == 0)
    opponentStonHistory[Empty] = 10000
    opponentStonHistory -= 1


    ourStoneHistory = np.exp(-ourStoneHistory * 0.1)
    opponentStonHistory = np.exp(-opponentStonHistory * 0.1)
    return ourStoneHistory, opponentStonHistory


def getOpponentRank(opponentRank):
    rank1 = np.ones((19, 19), dtype=int) * int(opponentRank == 1 or opponentRank == 9)
    rank2 = np.ones((19, 19), dtype=int) * int(opponentRank == 2 or opponentRank == 9)
    rank3 = np.ones((19, 19), dtype=int) * int(opponentRank == 3 or opponentRank == 9)
    rank4 = np.ones((19, 19), dtype=int) * int(opponentRank == 4 or opponentRank == 9)
    rank5 = np.ones((19, 19), dtype=int) * int(opponentRank == 5 or opponentRank == 9)
    rank6 = np.ones((19, 19), dtype=int) * int(opponentRank == 6 or opponentRank == 9)
    rank7 = np.ones((19, 19), dtype=int) * int(opponentRank == 7 or opponentRank == 9)
    rank8 = np.ones((19, 19), dtype=int) * int(opponentRank == 8 or opponentRank == 9)
    rank9 = np.ones((19, 19), dtype=int) * int(opponentRank == 9 or opponentRank == 9)
    return rank1, rank2, rank3, rank4, rank5, rank6, rank7, rank8, rank9


def getBorder():
    border = np.ones((19, 19), dtype=int)
    border[1:-1, 1:-1] = 0
    return border


def getPositionMask():
    positionMask = np.asarray(
        [[np.linalg.norm(np.array((i, j)) - np.array((9, 9))) for i in range(19)] for j in range(19)])

    positionMask = np.exp((positionMask ** 2) * -.5)

    return positionMask


def getTerriroties(terrBoard, turn):
    ourTerritories = (np.asarray(terrBoard) == turn).astype(int)
    opponentTerritories = (np.asarray(terrBoard) == -turn).astype(int)
    return ourTerritories, opponentTerritories


def getMoveMade(moveIndex, moves):
    ourMove = np.zeros((19, 19))
    opponentNextMove = np.zeros((19, 19))
    ourNextMove = np.zeros((19, 19))

    if moves[moveIndex] != "pass":
        ourMove[moves[moveIndex][0], moves[moveIndex][1]] = 1

    if moveIndex + 1 <= len(moves) - 1:
        if moves[moveIndex + 1] != "pass":
            opponentNextMove[moves[moveIndex + 1][0], moves[moveIndex + 1][1]] = 1

    if moveIndex + 2 <= len(moves) - 1:
        if moves[moveIndex + 2] != "pass":
            ourNextMove[moves[moveIndex + 2][0], moves[moveIndex + 2][1]] = 1

    return ourMove, opponentNextMove, ourNextMove
