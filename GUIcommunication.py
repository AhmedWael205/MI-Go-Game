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


    def send_gui_packet(self,board, terr, winLoss, scoreArr, lastPlay):
        # FLATTENING THE numpy 2D ARRAY
        tempBoard = list((np.array(board)).flatten())
        tempBoard = [int(tempBoard[i]) for i in range(len(tempBoard))]

        # CONVERTING INT32 TO INT FOR // (JSON) // SERIALIZATION
        tempTerr = list((np.array(terr)).flatten())
        tempTerr = [int(tempTerr[i]) for i in range(len(tempTerr))]

        # CONCATENATION INTO A SINGLE STRING PACKET SEPARATED BY ","
        packet = winLoss + "," + ",".join(map(str, tempBoard)) + "," + ",".join(map(str, tempTerr)) + "," + ",".join(
            map(str, scoreArr[::-1])) + "," + ",".join(map(str, lastPlay[0:2]))

        # DON'T SEND UNLESS THERE'S A CLIENT
        ack = self.sendSocket.recv()

        self.sendSocket.send_string(packet)

    def receive_gui_mode(self):
        # DON'T SEND UNLESS THERE'S A CLIENT
        self.receiveSocket.send(b"")

        packet = self.receiveSocket.recv_string()

        # CONVERT PACKET TO ARR
        packet = packet.split(",")

        # PACKET  [ MODE, X, Y] // MODE IS TRUE WHEN HUMAN VS AI IS TRUE
        return packet[0] == "True", int(packet[1]), int(packet[2])
