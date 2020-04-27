from Stones import stones
from Stones import Turn
import zmq
import numpy as np


def go():
    InitialWhiteLocations = []
    InitialBlackLocations = []
    turn = Turn.black
    Pass = [False, False]
    score = [6.5, 0]
    Board = stones(InitialWhiteLocations, InitialBlackLocations)
    Resign = False

    while False in Pass:
        Pass[turn] = False
        Move = input("Enter you move (Resign = 0,Pass = 1, Place a Stone = 2): ")

        if Move == "2":
            x = input("Enter Stone x-cord:")
            y = input("Enter Stone y-cord:")
            # btab2a bel 3aks(y,x) mesh (x,y)
            while not Board.AddStone((y, x), turn):
                x = input("Enter Stone x-cord:")
                y = input("Enter Stone y-cord:")
                pass
        elif Move == "1":
            Pass[turn] = True
        elif Move == "0":
            Resign = True
            break
        else:
            print("Wrong Input")
            continue
        LastPlay = (x, y, turn)  # White turn = 0 , Black Turn = 0
        turn = 1 - turn
        score, TerrBoard = Board.getScoreAndTerrBoard()
        gameBoard = Board.getBoard()

        # SENDING PACKET TO GUI
        # send_gui_packet(gameBoard, TerrBoard, 'n', score, LastPlay)

        print(gameBoard)
        print(TerrBoard)
        print("Score [White,Black]:", score)

    if score[0] > score[1] or (Resign and turn == 1):
        winner = "White"
        # SENDING PACKET TO GUI
        # send_gui_packet(gameBoard, TerrBoard, 'w', score, LastPlay)
    else:
        winner = "Black"
        # SENDING PACKET TO GUI
        # send_gui_packet(gameBoard, TerrBoard, 'b', score, LastPlay)

    print(winner, "wins")

    if Resign:
        return winner

    return score


context = zmq.Context()

# A SEND CHANNEL FOR GUI
sendSocket = context.socket(zmq.REP)
sendSocket.bind("tcp://*:2222")

# A RECEIVE CHANNEL FRO, GUI
receiveSocket = context.socket(zmq.REQ)
receiveSocket.connect("tcp://localhost:1234")


def send_gui_packet(board, terr, winLoss, scoreArr, lastPlay):
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
    ack = sendSocket.recv()

    sendSocket.send_string(packet)


def receive_gui_mode():
    # DON'T SEND UNLESS THERE'S A CLIENT
    receiveSocket.send(b"")

    packet = receiveSocket.recv_string()

    # CONVERT PACKET TO ARR
    packet = packet.split(",")

    # PACKET  [ MODE, X, Y] // MODE IS TRUE WHEN HUMAN VS AI IS TRUE
    return packet[0] == "True", int(packet[1]), int(packet[2])


if __name__ == "__main__":
    go()
