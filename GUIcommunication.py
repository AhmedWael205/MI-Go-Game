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
    # A SEND CHANNEL FOR GUI
    sendSocket = context.socket(zmq.REP)
    sendSocket.bind("tcp://*:2222")

    # A RECEIVE CHANNEL FRO, GUI
    receiveSocket = context.socket(zmq.REQ)
    receiveSocket.connect("tcp://localhost:1234")

    #   TERRITORY NOT REQ IN DOC :
    #   def send_gui_packet(self, board, terr, winLoss, scoreArr, lastPlay, mode, time, moveValidation):

    def send_gui_packet(self, board=np.zeros((19, 19), dtype=int), winLoss='n', scoreArr=[0, 0], lastPlay=[-1, -1],
                        timeBlack=0, timeWhite=0, moveValidation=1,
                        theBetterMove=0, betterMoveCoord=[-1, -1], capturedStones=None):
        # FLATTENING THE numpy 2D ARRAY
        # print("CURRENT \n", board)
        # print("LASTT \n ", self.lastBoard)

        if lastPlay != self.lastPlay:
            self.lastPlay = lastPlay
        else:
            lastPlay = self.lastPlay

        if capturedStones != self.capturedStones and capturedStones is not None:
            self.capturedStones = capturedStones
        else:
            capturedStones = self.capturedStones

        if theBetterMove != self.theBetterMove:
            self.theBetterMove = theBetterMove
        else:
            theBetterMove = self.theBetterMove

        # print("Score array current", scoreArr)
        # print("Score array LAAASTT ", self.lastScoreArr)
        if scoreArr != self.lastScoreArr and scoreArr[0] != 0 and scoreArr[1] != 0:
            self.lastScoreArr = scoreArr
        else:
            scoreArr = self.lastScoreArr
        # print("Score array LAAASTT AFTER IFFFFFFFFFFFF", self.lastScoreArr)
        if np.array_equal(board, np.zeros((19, 19), dtype=int)):
            board = self.lastBoard
        else:
            self.lastBoard = board
        # print("LASTT 3AKS \n ", self.lastBoard)
        tempBoard = list((np.array(board)).flatten())

        # CONVERTING INT32 TO INT FOR // (JSON) // SERIALIZATION
        tempBoard = [int(tempBoard[i]) for i in range(len(tempBoard))]

        # print("Temp Board", tempBoard)
        # tempTerr = list((np.array(terr)).flatten())
        # tempTerr = [int(tempTerr[i]) for i in range(len(tempTerr))]

        # CONCATENATION INTO A SINGLE STRING PACKET SEPARATED BY ","
        packet = winLoss + "," + ",".join(map(str, tempBoard)) + "," + ",".join(
            map(str, scoreArr[::-1])) + "," + ",".join(map(str, lastPlay[0:2])) + "," + str(
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
        print("packet[0] is " + packet[0])
        print("packet[1] is " + packet[1])
        print("packet[2] is " + packet[2])
        print("packet[3] is " + packet[3])
        print("packet[4] is " + packet[4])
        print("packet[5] is " + packet[5])

        # PACKET  [MODE, X, Y, RESIGN , PASS, HUMAN COLOR] --> MODE = 1: AI VS AI , -1--> HUMAN
        return int(packet[0]), int(packet[1]), int(packet[2]), int(packet[3]), int(packet[4]), int(packet[5])

    def receive_gui_mode(self):
        receivedPacket = self.receive_gui()
        print(receivedPacket)
        print(self.lastPacket)
        while receivedPacket == self.lastPacket:
            self.send_gui_packet()
            receivedPacket = self.receive_gui()
        self.lastPacket = receivedPacket
        return receivedPacket
