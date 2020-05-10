import copy

from Stones import stones
from GUIcommunication import GuiComm
import random
from FeatureExtractor.AI import AIplayer
from GameManager import GameManager

class Game:
    comm = None
    LastPass = 0;
    OurTurn = 1; # default we are Black

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
            pass
        else:
            # Human vs AI mode
            # Mode is TRUE packet indicating HUMAN VS AI, Disregard the rest of the packet
            self.mode = True
            pass
        #MCTS = False
        #mctSims= 1000
        #self.Agent = AIplayer("LargeNoKoModel18.h5",MCTS,mctSims)
        self.Agent = AIplayer("D:/University Materials/CMPN courses/Machine intelligence/Spring 2020/Project/Our Project/FeatureExtractor/LargeNoKoModel18.h5")
        self.previousMove = [-2,-2]

    def setOurTurn(self,OurTurn):
        self.OurTurn = OurTurn

    def play(self, Move, turn=-1, Debugging=False, mode=None, Time=None):
        if Time is None:
            # Time[0] = White Player Time, Time [1] = Black Player Time
            Time = [900000, 900000]

        # Last Play and Valid initialized outside the ifs scope
        valid = False
        lastPlay = [-3,-3]
        if self.mode and mode is None:
            # IF SELF MODE == TRUE, HUMAN VS AI MOVE PARAMETER IS DIFFERENT

            if Move[3] == 1:  # MOVE[2] IS THE RESIGN
                self.Resign = True
                valid = True
            elif Move[4] == self.LastPass + 1:  # MOVE[3] IS THE PASS
                self.Pass[turn] = True
                self.turn = turn
                self.LastPass = self.LastPass + 1
                valid = self.game.AddStone(1, self.turn)
                valid = True
            else:
                self.Pass[self.turn] = False
                lastPlay = Move[2:0:-1]
                valid = self.game.AddStone((int(Move[2]), int(Move[1])), turn)
                self.game.Drawboard()
                self.turn = turn
        else:
            if Move == 0:
                self.Resign = True
                valid = True
            elif Move == 1:
                if self.turn != self.OurTurn:
                    self.previousMove = [-1,-1]
                valid = self.game.AddStone(1,self.turn)
                self.Pass[self.turn] = True
                valid = True
            else:
                lastPlay = Move
                if self.turn == 1-self.OurTurn:
                    self.previousMove = [int(Move[0]), int(Move[1])]
                if turn == -1:
                    valid = self.game.AddStone((int(Move[0]), int(Move[1])), int(Move[2]))
                    self.turn = int(Move[2])
                else:
                    valid = self.game.AddStone((int(Move[0]), int(Move[1])), turn)
                    self.turn = int(turn)

        if valid:
            score, TerrBoard = self.game.getScoreAndTerrBoard()
            gameBoard = self.game.getBoard()

            if Debugging:
                print("\n                           Board")
                self.game.Drawboard()
                #print("\n                           Territory")
                #self.game.Drawboard(TerrBoard)
                print("Score [White,Black]:", score)

            capturedStones = self.game.CapturedStones

            if self.Resign:

                # Sending Last PLay as -2,-2 if any player resigns
                lastPlay = [-2, -2]

                if self.turn == self.OurTurn:
                    # SENDING PACKET TO GUI
                    if self.mode:
                        dummy = self.comm.receive_gui()
                    else:
                        dummy = self.comm.receive_gui_mode(mode=0)
                    print("We lose")
                    self.comm.send_gui_packet(gameBoard, 'l', score, lastPlay, Time[1], Time[0], True, 0,
                                                  capturedStones=capturedStones)
                else:
                    # SENDING PACKET TO GUI
                    if self.mode:
                        dummy = self.comm.receive_gui()
                    else:
                        dummy = self.comm.receive_gui_mode(mode=0)
                    print("We won")
                    self.comm.send_gui_packet(gameBoard, 'w', score, lastPlay, Time[1], Time[0], True, 0,
                                                  capturedStones=capturedStones)
                print("Game End Reason: Resign")
                return valid, True
            if self.Pass[turn]:
                # If any player chose pass, set last play to -3, -3
                lastPlay = [-3, -3]
            if False not in self.Pass:
                if score[self.OurTurn] > score[1 - self.OurTurn]:
                    # SENDING PACKET TO GUI
                    if self.mode:
                        dummy = self.comm.receive_gui()
                    else:
                        dummy = self.comm.receive_gui_mode(mode=0)
                    print("We won")
                    self.comm.send_gui_packet(gameBoard, 'w', score, lastPlay, Time[1], Time[0], True, 0,
                                                  capturedStones=capturedStones)
                else:
                    # SENDING PACKET TO GUI
                    if self.mode:
                        dummy = self.comm.receive_gui()
                    else:
                        dummy = self.comm.receive_gui_mode(mode=0)
                    print("We lose")
                    self.comm.send_gui_packet(gameBoard, 'l', score, lastPlay, Time[1], Time[0], True, 0,
                                                  capturedStones=capturedStones)
                print("Game End Reason: Pass")
                return valid, True

            # Lastly, Sending packet to GUI in in case there's no winner
            if self.mode:
                dummy = self.comm.receive_gui()
            else:
                dummy = self.comm.receive_gui_mode(mode=0)
            # print(gameBoard)
            # input("Before Sending ")
            #print("Before Sending last Move: ",lastPlay)
            #print("Remaining Time in seconds: ",Time[0]/1000,Time[1]/1000)
            self.comm.send_gui_packet(gameBoard, 'n', score, lastPlay, timeBlack=Time[1], timeWhite=Time[0], moveValidation=valid,
                                      theBetterMove=0, betterMoveCoord=[0, 0], capturedStones=capturedStones)
            # input("AFTER Sending ")
        self.turn = 1 - self.turn
        return valid, False  # not Valid

    def getMove(self,stones=None,turn=None,previousMove=None,Random=False,invalid=False):
        if stones is None:
            stones = self.game
        if turn is None:
            turn = self.OurTurn
        if previousMove is None:
            previousMove = self.previousMove
        if not Random:
            if not invalid:
                move = self.Agent.getMove(stones,turn,(previousMove[0],previousMove[1]))[0]
                if move[0] ==-1 and move[1] == -1:
                    move = 1
            else:
                x = GameManager(self.game)
                validMoves = x.GetPossibleMoves(1-turn)[0]
                y = random.randint(0, len(validMoves))
                if int(validMoves[y]) == 361:
                    move = 1
                else:
                    move = [int(validMoves[y]) // 19, int(validMoves[y])%19]
            return move


        else:
            x = random.randint(0, 361)
            if x == 361:
                return 1
            else:
                row = random.randint(0, 18)
                column = random.randint(0, 18)
                move = (row, column)
                return move


    def Drawboard(self):
        self.game.Drawboard()
