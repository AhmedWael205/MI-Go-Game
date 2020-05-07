from Stones import stones
from GUIcommunication import GuiComm
import random


class Game:
    comm = None

    def __init__(self, wloc=[], bloc=[], bCapturedStones=0, wCapturedStones=0, mode=1, GuiObject=None):
        self.turn = 1
        self.Pass = [False, False]
        self.Resign = False
        self.game = stones(wloc, bloc, bCapturedStones, wCapturedStones)
        if GuiObject is None:
            self.comm = GuiComm()
        else:
            self.comm = GuiObject
        if mode == 1:
            # AI vs AI mode
            # Mode is FALSE packet indicating AI VS AI, Disregard the rest of the packet
            self.mode = False
            self.comm.send_gui_packet(mode=self.mode)
            pass
        else:
            # Human vs AI mode
            # Mode is TRUE packet indicating HUMAN VS AI, Disregard the rest of the packet
            self.mode = True
            self.comm.send_gui_packet(mode=self.mode)
            pass

    def play(self, Move, Debugging=False):

        # Todo set pass = false @wael

        # Last Play and Valid initialized outside the ifs scope
        valid = False
        lastPlay = []
        if not self.mode:
            # IF SELF MODE == TRUE, MOVE PARAMETER IS DIFFERENT

            if Move[2] == 1:  # MOVE[2] IS THE RESIGN
                self.Resign = True
                valid = True
            elif Move[3] == 1:  # MOVE[3] IS THE PASS
                self.Pass[self.turn] = True
                valid = True
            else:
                lastPlay = Move[0:2]
                # todo move[2] representing el turn mesh Mwgooda men el GUI
                valid = self.game.AddStone((int(Move[0]), int(Move[1])), int(Move[2]))
                self.turn = int(Move[2])
        else:
            # Todo Coordinate the move m3 samadoni
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

            if Debugging:
                print("\n                           Board")
                self.game.Drawboard()
                print("\n                           Territory")
                self.game.Drawboard(TerrBoard)
                print("Score [White,Black]:", score)

            if self.Resign:

                # Sending Last PLay as -2,-2 if any player resigns
                lastPlay = [-2, -2]

                if self.turn == 1:
                    winner = "White"
                    # SENDING PACKET TO GUI
                    self.comm.send_gui_packet(gameBoard, 'w', score, lastPlay, self.mode, 0, True)
                else:
                    winner = "Black"
                    # SENDING PACKET TO GUI
                    self.comm.send_gui_packet(gameBoard, 'b', score, lastPlay, 0, self.mode, 0, True)
                return valid, True

            if False not in self.Pass:
                if score[0] > score[1]:
                    winner = "White"
                    # SENDING PACKET TO GUI
                    self.comm.send_gui_packet(gameBoard, 'w', score, lastPlay, self.mode, 0, True)
                else:
                    winner = "Black"
                    # SENDING PACKET TO GUI
                    self.comm.send_gui_packet(gameBoard, 'b', score, lastPlay, self.mode, 0, True)
                return valid, True

            if True in self.Pass:
                # If any player chose pass, set last play to -3, -3
                lastPlay = [-3, -3]

            # Lastly, Sending packet to GUI in in case there's no winner
            self.comm.send_gui_packet(gameBoard, 'n', score, lastPlay, mode=self.mode, time=0, moveValidation=valid)

        return valid, False  # not Valid

    def getMove(self):
        x = random.randint(0, 362)
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
