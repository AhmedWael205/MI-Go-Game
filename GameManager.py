import numpy as np
from Stones import stones
import copy


def AdjustBoardPrespective(matrixboard: np.ndarray, colour):
    board = matrixboard.reshape(361)

    return (board == colour).astype(int)


class GameManager:
    statesCount = 0

    def __init__(self, prevGame: stones = None, actor=0, action=361, simulate=True):

        self.id = GameManager.statesCount
        GameManager.statesCount += 1

        if prevGame is None:
            prevGame = stones()

        if simulate:
            self.game = copy.deepcopy(prevGame)
        else:
            self.game = prevGame

        self.move = action
        if action != 361:
            position = (action // 19, action % 19)
            self.game.AddStone(position, int(actor == 1))

        if actor == 0:
            self.turn = -1
        else:
            self.turn = -actor

        previousBoard = self.game.getBoard()

        self.prevWhites = np.zeros((361, 8), dtype=int)
        self.prevBlacks = np.zeros((361, 8), dtype=int)
        self.prevWhites[:, 0] = AdjustBoardPrespective(previousBoard, 1)
        self.prevBlacks[:, 0] = AdjustBoardPrespective(previousBoard, -1)

        memorySize = min((len(self.game._WPreviousBoardStates) + len(self.game._BPreviousBoardStates) + 1) // 2, 5)

        for i in range(1, memorySize):
            self.prevWhites[:, i] = AdjustBoardPrespective(self.game._PreviousBoardStates[int(self.turn == 1)][-i], 1)
            self.prevBlacks[:, i] = AdjustBoardPrespective(self.game._PreviousBoardStates[int(self.turn == 1)][-i], -1)

            if i != memorySize - 1:
                self.prevWhites[:, i] = AdjustBoardPrespective(
                    self.game._PreviousBoardStates[int((1 - self.turn) == 1)][-i], 1)
                self.prevBlacks[:, i] = AdjustBoardPrespective(
                    self.game._PreviousBoardStates[int((1 - self.turn) == 1)][-i], -1)

        truthOfMoves = np.zeros(362,dtype=bool)
        truthOfMoves[-1]=True
        dummy=copy.deepcopy(prevGame)
        truthOfMoves[:-1]=np.asarray([dummy.AddStone((i,j), int(actor == 1)) for i in range(19) for j in range(19)])
        self.possibleMoves=np.where(truthOfMoves)

    def MakeMove(self):
        return GameManager(self.game, self.turn, self.move, False)


