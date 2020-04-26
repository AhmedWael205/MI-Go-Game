import numpy as np
from Stones import stones
import copy

"""

data members:
    game: an instance of stones holding the current game
    id: a unique id for each game state
    previousMove: the last move made by the other player
    move: the move to be made by the manager 
    turn: the player that will make the suggested move
    prevWhites: the last 8 boards from white's perspective in the format agreed on
    prevBlacks: the last 8 boards from blacks's perspective in the format agreed on
    isEnded: a flag indicating whether the suggested move ends the game
    winner: integer indicating the current winner (-1 black, 1 white, 0 tie)
    
member functions:
    MakeMove: called from the object that you simulated this move from and you want to make
    SimulateMove: takes the move to be simulated and tries it without changing the game
    GetPossibleMoves: return an array of positions you can play in (vector format not matrix)
    
"""

def AdjustBoardPrespective(matrixboard: np.ndarray, colour):
    board = matrixboard.reshape(361)

    return (board == colour).astype(int)


class GameManager:
    statesCount = 0

    def __init__(self, prevGame: stones = None, actor=0, action=361, simulate=True, prevMove=-1):

        self.id = GameManager.statesCount
        GameManager.statesCount += 1

        if prevGame is None:
            prevGame = stones()

        if simulate:
            self.game = copy.deepcopy(prevGame)
        else:
            self.game = prevGame
        self.previousMove = prevMove
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

        score = self.game.getScoreAndTerrBoard()[0]

        noMoreMoves = len(self.GetPossibleMoves(True)) + len(self.GetPossibleMoves(False)) == 0
        doublepass = action == 361 and self.previousMove == 361

        self.isEnded = noMoreMoves or doublepass

        self.winner = int(score[0] > score[1])
        self.winner -= int(score[1] < score[0])

    def MakeMove(self):
        return GameManager(self.game, self.turn, self.move, False, self.previousMove)

    def SimulateMove(self, action):
        return GameManager(self.game, self.turn, action, True, self.move)

    def GetPossibleMoves(self, forMe):
        if forMe:
            actor = self.turn
        else:
            actor = -self.turn

        truthOfMoves = np.zeros(362, dtype=bool)
        truthOfMoves[-1] = True
        buffer = []
        for i in range(19):
            for j in range(19):
                dummy = copy.deepcopy(self.game.getBoard())
                buffer.append(dummy.AddStone((i, j), int(actor == 1)))

        truthOfMoves[:-1] = np.asarray(buffer)
        return np.where(truthOfMoves)
