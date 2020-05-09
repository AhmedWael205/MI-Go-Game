# from Stones import stones
# from Stones import Turn
# import zmq
# import numpy as np
import copy
import os

from ServerConfig import server_config
from game import Game
from GUIcommunication import GuiComm
import datetime

def go():

    GUI = GuiComm()
    receivedPacket = GUI.receive_gui_mode()
    GUI.send_gui_packet()
    mode = receivedPacket[0]

    if mode == 1:  # AI vs Human
        Time = [900000, 900000]
        """
        if int(initial_locations):
            file_name = input("Enter the JSON file name: ")
            game = server_config(file_name,mode=0,GuiObject=GUI)
        else:
            # MODE = 0 MEANING HUMAN VS AI
            game = Game(GuiObject=GUI, mode=0)
         """
        # Receiving Human Color
        Human = 1
        # @ Todo CALL RECEIVE A HUMAN COLOUR

        # receivedPacket = GUI.receive_gui_mode()
        # GUI.send_gui_packet()
        # print("Human color = ", Human)

        game = Game(GuiObject=GUI, mode=0)
        game_end = False
        turn = game.turn
        while not game_end:
            valid = False
            if turn == Human:
                # Receive from GUI a packet
                receivedPacket = GUI.receive_gui_mode()
                GUI.send_gui_packet()
                valid, game_end = game.play(receivedPacket, turn,Time=Time)
                game.Drawboard()
                while not valid:
                    # send a packet back to GUI
                    dummy = GUI.receive_gui()
                    GUI.send_gui_packet(moveValidation=False)
                    # receive another one
                    receivedPacket = GUI.receive_gui_mode()
                    GUI.send_gui_packet()
                    valid, game_end = game.play(receivedPacket, turn,Time=Time)
                LastPlay = receivedPacket[1:3]
            AI_move = game.getMove()
            tempGame = copy.deepcopy(game.game)
            valid = tempGame.AddStone(AI_move, turn)
            while not valid:
                AI_move = game.getMove()
                valid = tempGame.AddStone(AI_move, turn)
            if turn != Human:
                valid, game_end = game.play(AI_move, turn, mode=True,Time=Time)
                while not valid:
                    AI_move = game.getMove()
                    valid, game_end = game.play(AI_move, turn, mode=True,Time=Time)

            AI_score = tempGame.getScoreAndTerrBoard()[0]

            LastPlay = AI_move

            score = game.game.getScoreAndTerrBoard()[0]
            if turn == Human:
                print("Human Score Diff :", score[Human] - score[1 - Human])
                print("AI Score Diff :", AI_score[Human] - AI_score[1 - Human])
                if score[Human] - score[1 - Human] >= AI_score[Human] - AI_score[1 - Human]:
                    print("Here1")
                    dummy = GUI.receive_gui()
                    GUI.send_gui_packet(theBetterMove=1, betterMoveCoord=AI_move)
                else:
                    print("Here2")
                    dummy = GUI.receive_gui()
                    GUI.send_gui_packet(theBetterMove=-1, betterMoveCoord=AI_move)
            turn = 1 - turn  # White turn = 0 , Black Turn = 0
    else:
        os.system('python CommunicationSamadoni.py BS ws://127.0.0.1:8080')

    return True


if __name__ == "__main__":
    go()
