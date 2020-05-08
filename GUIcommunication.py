import zmq
import numpy as np


class GuiComm:
    context = zmq.Context()

    # A SEND CHANNEL FOR GUI
    sendSocket = context.socket(zmq.REP)
    sendSocket.bind("tcp://*:2222")

    # A RECEIVE CHANNEL FRO, GUI
    receiveSocket = context.socket(zmq.REQ)
    receiveSocket.connect("tcp://localhost:1234")

    #   TERRITORY NOT REQ IN DOC :
    #   def send_gui_packet(self, board, terr, winLoss, scoreArr, lastPlay, mode, time, moveValidation):

    def send_gui_packet(self, board=[], winLoss="", scoreArr=[], lastPlay=[], timeBlack=0, timeWhite=0, moveValidation=True, theBetterMove=0, betterMoveCoord=[], capturedStones=[]):
        # FLATTENING THE numpy 2D ARRAY
        tempBoard = list((np.array(board)).flatten())

        # CONVERTING INT32 TO INT FOR // (JSON) // SERIALIZATION
        tempBoard = [int(tempBoard[i]) for i in range(len(tempBoard))]

        # tempTerr = list((np.array(terr)).flatten())
        # tempTerr = [int(tempTerr[i]) for i in range(len(tempTerr))]

        # CONCATENATION INTO A SINGLE STRING PACKET SEPARATED BY ","
        packet = winLoss + "," + ",".join(map(str, tempBoard)) + "," + ",".join(
            map(str, scoreArr[::-1])) + "," + ",".join(map(str, lastPlay[0:2])) + "," + str(
            timeBlack) + "," + str(timeWhite) + "," + str(moveValidation) + "," + str(theBetterMove) + "," + ",".join(map(str, betterMoveCoord)) + "," + ",".join(map(str, capturedStones))

        # DON'T SEND UNLESS THERE'S A CLIENT
        ack = self.sendSocket.recv()

        self.sendSocket.send_string(packet)

    # PACKET CONTAINS: MODE, X, Y, RESIGN, PASS RESPECTIVELY
    def receive_gui_mode(self):
        # DON'T SEND UNLESS THERE'S A CLIENT
        self.receiveSocket.send(b"")

        packet = self.receiveSocket.recv_string()

        # CONVERT PACKET TO ARR
        packet = packet.split(",")

        # PACKET  [MODE, X, Y, RESIGN , PASS, HUMAN COLOR]
        return int(packet[0]), int(packet[1]), int(packet[2]), int(packet[3]), int(packet[4]), int(packet[5])
