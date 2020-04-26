from copy import copy

import numpy as np
from Stones import stones

class GameState:
    ID = 0
    WhiteBoards = []
    BlackBoards = []
    Turn = -1 # 0 equal White turn ,  1 equal Black turn
    State = 0 # 0 Running, 1 White wins, -1 Black Wins
    Board = []
    Pass = [False, False]
    _Game = stones([],[])
    def __init__(self, Paramters = False, Turn = None,CurrState = None,Board = None,PrevGameState = None):
        GameState.ID += 1
        if not Paramters:
            for i in range(8):
                self.WhiteBoards.append(np.zeros((19, 19), dtype=int))
                self.BlackBoards.append(np.zeros((19, 19), dtype=int))
                self.Turn = 1
                self.State =0
                self.Board = np.copy(self._Game.getBoard())
        else:
            for i in range(7):
                self.WhiteBoards[i] = np.copy(PrevGameState.WhiteBoards[i])
                self.BlackBoards[i] = np.copy(PrevGameState.BlackBoards[i])

            self.WhiteBoards.insert(0,np.zeros((19, 19), dtype=int))
            self.BlackBoards.insert(0, np.zeros((19, 19), dtype=int))
            for i,j in range (19,19):
                if Board[i][j] == 1:
                    self.WhiteBoards[0][i][j] = 1
                elif Board[i][j] == -1:
                    self.BlackBoards[0][i][j] = 1
            self.Turn = Turn
            self.State = CurrState
            self.Board = np.copy(Board)

    def getAllowedAction(self):
        TryGame = copy(self._Game)
        AllowedActions = []
        for i in range(19):
            for j in range(19):
                if self.Board[i][j] == 0:
                    if TryGame.tryAction((i,j),self.Turn):
                        AllowedActions.append(i*19 + j)
        AllowedActions.append(361) # 361 = pass
        return AllowedActions

    def simulateaction(self,action):
        TryGame = copy(self._Game)
        i = action // 19
        j = action % 19
        TryGame.AddStone((str(i),str(j)), self.Turn)
        newGameState = copy(self)
        newGameState.Board = TryGame.getBoard()
        newGameState.ID = self.ID + 1

        newGameState.WhiteBoards.pop(7)
        newGameState.BlackBoards.pop(7)

        newGameState.WhiteBoards.insert(0, np.zeros((19, 19), dtype=int))
        newGameState.BlackBoards.insert(0, np.zeros((19, 19), dtype=int))

        for i in range(19):
            for j in range(19):
                if newGameState.Board[i][j] == 1:
                    newGameState.WhiteBoards[0][i][j] = 1
                elif newGameState.Board[i][j] == -1:
                    newGameState.BlackBoards[0][i][j] = 1
        return newGameState

    def makeMove(self,action):
        i = action // 19
        j = action % 19

        if action == 361:
            newGameState = copy(self)
            newGameState.ID = self.ID + 1
            newGameState.Pass[self.Turn] = True
            newGameState.Turn = 1 - self.Turn
            if False not in self.Pass:
                score, _ = self._Game.getScoreAndTerrBoard()
                if score [0] > score [1]:
                    newGameState.State = 1
                else:
                    newGameState.State = -1
            return newGameState

        else:
            self.Pass[self.Turn] = False
            self._Game.AddStone((str(i), str(j)), self.Turn)
            self.Turn = 1 - self.Turn
            newGameState = copy(self)
            newGameState.Board = self._Game.getBoard()

            newGameState.ID = self.ID + 1
            newGameState.WhiteBoards.pop(7)
            newGameState.BlackBoards.pop(7)

            newGameState.WhiteBoards.insert(0, np.zeros((19, 19), dtype=int))
            newGameState.BlackBoards.insert(0, np.zeros((19, 19), dtype=int))

            for i in range(19):
                for j in range(19):
                    if newGameState.Board[i][j] == 1:
                        newGameState.WhiteBoards[0][i][j] = 1
                    elif newGameState.Board[i][j] == -1:
                        newGameState.BlackBoards[0][i][j] = 1
            return newGameState

Game = GameState()
print(Game.makeMove(1).makeMove(361).makeMove(19).makeMove(361).makeMove(361).State)