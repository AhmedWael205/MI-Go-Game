# from Stones import stones
# from Stones import Turn
# import zmq
# import numpy as np
# import os
# from ServerConfig import server_config

import asyncio
import copy
from game import Game
from GUIcommunication import GuiComm
import datetime
from CommunicationSamadoni import main2


def go():

    GUI = GuiComm()
    receivedPacket = GUI.receive_gui_mode()
    GUI.send_gui_packet()
    mode = receivedPacket[0]
    Human = receivedPacket[5]
    PreviousHumanMove = [-2,-2]
    PreviousAIMove = [-2, -2]
    SuggestedAIMove = [-1,-1]

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

        # receivedPacket = GUI.receive_gui_mode()
        # GUI.send_gui_packet()
        # print("Human color = ", Human)

        game = Game(GuiObject=GUI, mode=0)
        game.setOurTurn(Human)
        game_end = False
        turn = game.turn
        while not game_end:
            valid = False
            if turn == Human:
                # Receive from GUI a packet
                a = datetime.datetime.now()
                receivedPacket = GUI.receive_gui_mode()
                GUI.send_gui_packet()
                b = datetime.datetime.now()
                c = b - a
                Time[turn] = Time[turn] - int(c.total_seconds() * 1000)
                valid, game_end = game.play(receivedPacket, turn,Time=Time)
                game.Drawboard()
                while not valid:
                    # send a packet back to GUI
                    dummy = GUI.receive_gui()
                    GUI.send_gui_packet(moveValidation=False)
                    # receive another one
                    a = datetime.datetime.now()
                    receivedPacket = GUI.receive_gui_mode()
                    GUI.send_gui_packet()
                    b = datetime.datetime.now()
                    c = b - a
                    Time[turn] = Time[turn] - int(c.total_seconds() * 1000)
                    valid, game_end = game.play(receivedPacket, turn,Time=Time)
                PreviousHumanMove = receivedPacket[1:3]
                # a = datetime.datetime.now()
                AI_move = game.getMove(turn=Human,previousMove=PreviousAIMove)
                # b = datetime.datetime.now()
                # c = b - a
                tempGame = copy.deepcopy(game.game)
                valid = tempGame.AddStone(AI_move, turn)
                while not valid:
                    # a = datetime.datetime.now()
                    AI_move = game.getMove(turn=Human,previousMove=PreviousAIMove)
                    # b = datetime.datetime.now()
                    # c = c + (b - a)
                    valid = tempGame.AddStone(AI_move, turn)
                SuggestedAIMove = AI_move
                AI_score = tempGame.getScoreAndTerrBoard()[0]

                score = game.game.getScoreAndTerrBoard()[0]
                if SuggestedAIMove == 0 or SuggestedAIMove == 1:
                    SuggestedAIMove = [-1, -1]

                # print("Human Score Diff :", score[Human] - score[1 - Human])
                # print("AI Score Diff :", AI_score[Human] - AI_score[1 - Human])
                if score[Human] - score[1 - Human] >= AI_score[Human] - AI_score[1 - Human]:
                    dummy = GUI.receive_gui()
                    GUI.send_gui_packet(theBetterMove=1, betterMoveCoord=SuggestedAIMove)
                else:
                    dummy = GUI.receive_gui()
                    GUI.send_gui_packet(theBetterMove=-1, betterMoveCoord=SuggestedAIMove)

            else:
                a = datetime.datetime.now()
                AI_move = game.getMove(turn=1-Human, previousMove=PreviousHumanMove)
                b = datetime.datetime.now()
                c = (b - a)
                Time[turn] = Time[turn] - int(c.total_seconds() * 1000)
                valid, game_end = game.play(AI_move, turn, mode=True, Time=Time)
                while not valid:
                    a = datetime.datetime.now()
                    AI_move = game.getMove(turn=1-Human, previousMove=PreviousHumanMove)
                    b = datetime.datetime.now()
                    c = b - a
                    Time[turn] = Time[turn] - int(c.total_seconds() * 1000)
                    valid, game_end = game.play(AI_move, turn, mode=True,Time=Time)
                PreviousAIMove = AI_move


            turn = 1 - turn  # White turn = 0 , Black Turn = 0

    else:
        # os.system('python CommunicationSamadoni.py BS ws://127.0.0.1:8080')
        name = None
        url = None

        x = input("Would you like to enter client name: (1 = yes, 0 = no) ?")
        if int(x) == 1:
            name = input("Please enter the client name: ")

        y = input("Would you like to enter client url: (1 = yes, 0 = no) ?")
        if int(y) == 1:
            url = input("Please enter the client url: ")

        loop = asyncio.get_event_loop()
        asyncio.ensure_future(main2(GUI, name, url))
        loop.run_forever()

    return True


if __name__ == "__main__":
    go()
