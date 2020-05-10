from GUIcommunication import GuiComm
import numpy as np


GUI = GuiComm()
receivedPacket = GUI.receive_gui_mode()
GUI.send_gui_packet()
mode = receivedPacket[0]
board=np.zeros((19, 19), dtype=int)
board [3][3] = -1
print(board)
while True:
    dummy = GUI.receive_gui_mode(mode=0)
    GUI.send_gui_packet(board, 'n', [7,5], (9,9,1), timeBlack=0, timeWhite=0,
                             moveValidation=True, theBetterMove=0, betterMoveCoord=[0, 0])
    print(board[3][3])
