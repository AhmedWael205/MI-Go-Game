from Stones import stones
from keras.models import load_model
from FeatureExtractor.Agent import Agent
import numpy as np
from FeatureExtractor import extractorFunctions as ef


def getInput(game, turn, border, positionMask, whitePlayerRank, blackPlayerRank):
    inputState = []

    gameBoard = game.getBoard()
    stoneAge = game.stoneAge
    opponentRank = whitePlayerRank if turn == -1 else blackPlayerRank
    _, terrBoard = game.getScoreAndTerrBoard()

    my1Lib, my2Lib, my3Lib, opp1Lib, opp2Lib, opp3Lib = ef.getLiberties(gameBoard, turn)
    # myKo = ef.getKo(gameBoard, turn, game)

    ourStones, opponentStones, emptyPositions = ef.getStoneOwnership(gameBoard, turn)
    ourStoneHistory, opponentStoneHistory = ef.getStoneHistory(stoneAge, ourStones, opponentStones)
    rank1, rank2, rank3, rank4, rank5, rank6, rank7, rank8, rank9 = ef.getOpponentRank(opponentRank)
    # border and position mask are calculated once before iterating over matches
    ourTerritories, opponentTerritories = ef.getTerriroties(terrBoard, turn)

    inputState.extend([my1Lib, my2Lib, my3Lib, opp1Lib, opp2Lib, opp3Lib])
    # inputState.extend([myKo])
    inputState.extend([ourStones, opponentStones, emptyPositions])
    inputState.extend([ourStoneHistory, opponentStoneHistory])
    inputState.extend([rank1, rank2, rank3, rank4, rank5, rank6, rank7, rank8, rank9])
    inputState.extend([border, positionMask])
    inputState.extend([ourTerritories, opponentTerritories])

    inputState = np.asarray([inputState])
    return inputState


def CheckValid(game, action, turn, nBest, i):
    score = game.getScoreAndTerrBoard()[0]

    if action == 361:
        if score[turn] <= score[1 - turn]:

            if i == -361:
                return 361
            else:
                action = CheckValid(game, nBest[i - 2], turn, nBest, i - 1)
                return action
        else:
            return 361

    if not game.checkKo((action // 19, action % 19), turn):
        return action
    else:
        if i == -361:
            return 361
        else:
            action = CheckValid(game, nBest[i - 2], turn, nBest, i - 1)
            return action


class AIplayer:
    def __init__(self, modelName, MCTS=0, mctSims=1):
        self.whitePlayerRank = 0
        self.blackPlayerRank = 0
        self.border = ef.getBorder()
        self.positionMask = ef.getPositionMask()

        self.pmodel = load_model(modelName)
        self.MCTS = MCTS

        if self.MCTS != 0:
            self.vmodel = load_model("FeatureExtractor/ValueNoKoModel12.h5")
            self.TreeAgent = Agent(MCTS, self.pmodel, self.vmodel, mctSims)

    def getMove(self, game: stones, turn, prevMove=(-2, -2)):

        if prevMove == (-1, -1):
            if game.getScoreAndTerrBoard()[0][turn] > game.getScoreAndTerrBoard()[0][1 - turn]:
                return [(-1, -1)]

        if turn == 0:
            Mturn = 1
        else:
            Mturn = -1

        if self.MCTS == 0:
            state = getInput(game, Mturn, self.border, self.positionMask, self.whitePlayerRank, self.blackPlayerRank)
            actions = self.pmodel.predict(state)
            action = np.argmax(actions[0])
            nBest = np.argsort(actions[0])[0]

            action = CheckValid(game, action, turn, nBest, 0)

            if action == 361:
                return [(-1, -1)]
            else:
                return [(action // 19, action % 19)]

        else:
            if prevMove == (-2,-2):
                AprevMove = -1
            else:
                AprevMove = 19 * prevMove[0] + prevMove[1]

            action = self.TreeAgent.makeMove(game, AprevMove)
            if action == 361:
                return [(-1, -1)]
            else:
                return [(action // 19, action % 19)]
