from Stones import stones
from GUIcommunication import GuiComm
import random

class Game:
    _comm = GuiComm()
    def __init__(self, wloc = [], bloc = [], bCapturedStones = 0, wCapturedStones = 0,mode = 1):
        self.turn = 1
        self.Pass = [False, False]
        self.Resign = False
        self.game = stones(wloc,bloc,bCapturedStones,wCapturedStones)
        if mode == 1: # AI vs AI mode
            # TODO send to gui 7aga bat2oloh AI vs AI
            pass
        else: # Human vs AI mode
            # TODO send to gui 7aga bat2oloh Human vs AI
            pass

    def play(self,Move,Debugging = False):
        if Move == 0:
            self.Resign = True
            valid = True
        elif Move == 1:
            self.Pass[self.turn] = True
            valid = True
        else:
            lastPlay = Move
            valid = self.game.AddStone((int(Move[0]), int(Move[1])), int(Move[2]))
            self.turn = int(Move[2])
        if valid:
            self.turn = 1 - self.turn
            score, TerrBoard = self.game.getScoreAndTerrBoard()
            gameBoard = self.game.getBoard()

            # SENDING PACKET TO GUI
            # self._comm.send_gui_packet(gameBoard, TerrBoard, 'n', score, LastPlay)

            if Debugging:
                print("\n                           Board")
                self.game.Drawboard()
                print("\n                           Territory")
                self.game.Drawboard(TerrBoard)
                print("Score [White,Black]:", score)

            if self.Resign:
                if self.turn == 1:
                    winner = "White"
                    # SENDING PACKET TO GUI
                    # self._comm.send_gui_packet(gameBoard, TerrBoard, 'w', score, LastPlay)
                else:
                    winner = "Black"
                    # SENDING PACKET TO GUI
                    # self._comm.send_gui_packet(gameBoard, TerrBoard, 'b', score, LastPlay)
                return valid,True

            if False not in self.Pass:
                if score[0] > score[1]:
                    winner = "White"
                    # SENDING PACKET TO GUI
                    # self._comm.send_gui_packet(gameBoard, TerrBoard, 'w', score, LastPlay)
                else:
                    winner = "Black"
                    # SENDING PACKET TO GUI
                    # self._comm.send_gui_packet(gameBoard, TerrBoard, 'b', score, LastPlay)
                return valid,True
        return valid,False  # not Valid

    def getMove(self):
        x  = random.randint(0,362)
        if x == 361:
            return 1
        elif x == 362:
            return 0
        else:
            row = random.randint(0, 19)
            column = random.randint(0, 19)
            move = (row, column)
            return move

    def Drawboard(self):
        self.game.Drawboard()