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



    def makeMove(self,action):
        m = action // 19
        n = action % 19

        newGameState = copy(self)
        wloc = []
        bloc = []
        for i in range(19):
            for j in range(19):
                if self.Board[i][j] == 1:
                    wloc.append((i, j))
                elif self.Board[i][j] == -1:
                    bloc.append((i, j))
        newGameState._Game = stones(wloc, bloc)

        if action == 361:
            GameState.ID += 1
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
            newGameState.Pass[self.Turn] = False
            newGameState._Game.AddStone((str(m), str(n)), self.Turn)
            newGameState.Turn = 1 - self.Turn
            newGameState.Board = newGameState._Game.getBoard()

            GameState.ID += 1
            newGameState.WhiteBoards.pop(7)
            newGameState.BlackBoards.pop(7)

            newGameState.WhiteBoards.insert(0, np.copy(newGameState.WhiteBoards[1]))
            newGameState.BlackBoards.insert(0, np.copy(newGameState.BlackBoards[1]))

            if self.Turn == 0:
                newGameState.WhiteBoards[0][m][n] = 1
            else:
                newGameState.BlackBoards[0][m][n] = 1
            return newGameState

Game = GameState()
print(Game.makeMove(1).makeMove(361).BlackBoards[0])
print(Game.getAllowedAction())