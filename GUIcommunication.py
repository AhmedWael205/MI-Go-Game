import zmq
import numpy as np


class GuiComm:
    context = zmq.Context()
    lastPacket = (-2, -2, -2, -2, -2, -2)
    lastBoard = np.zeros((19, 19), dtype=int)
    lastPlay = [-1, -1]
    capturedStones = [0, 0]
    theBetterMove = 0
    lastScoreArr = [0, 0]
    winner = 'n'
    betterMoveCoordLast = [-1, -1]
    # A SEND CHANNEL FOR GUI
    sendSocket = context.socket(zmq.REP)
    sendSocket.bind("tcp://*:2222")

    # A RECEIVE CHANNEL FRO, GUI
    receiveSocket = context.socket(zmq.REQ)
    receiveSocket.connect("tcp://localhost:1234")

    #   TERRITORY NOT REQ IN DOC :
    #   def send_gui_packet(self, board, terr, winLoss, scoreArr, lastPlay, mode, time, moveValidation):

    def send_gui_packet(self, board=np.zeros((19, 19), dtype=int), winLoss='n', scoreArr=[0, 0], lastPlay=[-1, -1],
                        timeBlack=-1, timeWhite=-1, moveValidation=1,
                        theBetterMove=0, betterMoveCoord=[-1, -1], capturedStones=None):
        # FLATTENING THE numpy 2D ARRAY
        # print("LAST PLAYABLES \n", lastPlay)
        # print(self.lastPlay)
        if lastPlay == 1:
            lastPlay = [-3,-3]
        if  lastPlay == 0:
            lastPlay = [-2, -2]
        if lastPlay != self.lastPlay and lastPlay[0] != -1 and lastPlay[1] != -1:
            self.lastPlay = lastPlay
        else:
            lastPlay = self.lastPlay
        # print(self.lastPlay)
        if capturedStones != self.capturedStones and capturedStones is not None:
            self.capturedStones = capturedStones
        else:
            capturedStones = self.capturedStones

        if theBetterMove != self.theBetterMove and theBetterMove != '0':
            self.theBetterMove = theBetterMove
        else:
            theBetterMove = self.theBetterMove

        if scoreArr[0] != 0 and scoreArr[1] != 0 and scoreArr != self.lastScoreArr:
            self.lastScoreArr = scoreArr
        else:
            scoreArr = self.lastScoreArr

        if winLoss != 'n' and winLoss != self.winner:
            self.winner = winLoss
        else:
            winLoss = self.winner

        if betterMoveCoord[0] != -1 and betterMoveCoord[1] != -1 and betterMoveCoord != self.betterMoveCoordLast:
            self.betterMoveCoordLast = betterMoveCoord
        else:
            betterMoveCoord = self.betterMoveCoordLast

        # scoreArr[0] = int(scoreArr[0])
        # scoreArr[1] = int(scoreArr[1])
        if np.array_equal(board, np.zeros((19, 19), dtype=int)):
            board = self.lastBoard
        else:
            self.lastBoard = board
        tempBoard = list((np.array(board)).flatten())

        # CONVERTING INT32 TO INT FOR // (JSON) // SERIALIZATION
        tempBoard = [int(tempBoard[i]) for i in range(len(tempBoard))]

        # print("Temp Board", tempBoard)
        # tempTerr = list((np.array(terr)).flatten())
        # tempTerr = [int(tempTerr[i]) for i in range(len(tempTerr))]

        # CONCATENATION INTO A SINGLE STRING PACKET SEPARATED BY ","
        packet = winLoss + "," + ",".join(map(str, tempBoard)) + "," + ",".join(
            map(str, scoreArr)) + "," + ",".join(map(str, lastPlay[0:2])) + "," + str(
            timeBlack) + "," + str(timeWhite) + "," + str(moveValidation) + "," + str(theBetterMove) + "," + ",".join(
            map(str, betterMoveCoord)) + "," + ",".join(map(str, capturedStones))

        # DON'T SEND UNLESS THERE'S A CLIENT
        ack = self.sendSocket.recv()

        self.sendSocket.send_string(packet)

    def receive_gui(self):
        # DON'T SEND UNLESS THERE'S A CLIENT
        self.receiveSocket.send(b"HELLO GUIIII")

        packet = self.receiveSocket.recv_string()

        # CONVERT PACKET TO ARR
        packet = packet.split(",")

        # PACKET  [MODE, X, Y, RESIGN , PASS, HUMAN COLOR] --> MODE = 1: AI VS AI , -1--> HUMAN
        return int(packet[0]), int(packet[1]), int(packet[2]), int(packet[3]), int(packet[4]), int(packet[5])

    def receive_gui_mode(self,mode=1):

        receivedPacket = self.receive_gui()
        # print(receivedPacket)
        # print(self.lastPacket)
        if mode == 1:
            while receivedPacket == self.lastPacket:
                self.send_gui_packet()
                receivedPacket = self.receive_gui()
        else:
            for i in range(50):
                self.send_gui_packet()
                receivedPacket = self.receive_gui()
        self.lastPacket = receivedPacket
        return receivedPacket
