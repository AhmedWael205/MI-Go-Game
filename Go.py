# from Stones import stones
# from Stones import Turn
# import zmq
# import numpy as np
from ServerConfig import server_config
from game import Game
from GUIcommunication import GuiComm


def go():
    Human = input("Do you want human to be black (0 = no, 1 = yes)?")
    Human = int(Human)
    initial_locations = input("Is there an initial board state in a JSON file (0 = no, 1 = yes)? ")
    GUI = GuiComm()
    if int(initial_locations):
        file_name = input("Enter the JSON file name: ")
        game = server_config(file_name,mode=0,GuiObject=GUI)
    else:
        # MODE = 0 MEANING HUMAN VS AI
        game = Game(GuiObject=GUI, mode=0)
    game_end = False
    score, TerrBoard = game.game.getScoreAndTerrBoard()
    turn = game.turn
    while not game_end:
        valid = False
        if turn == Human:
            # Receive from GUI a packet

            # PACKET CONTAINS: X, Y, RESIGN, PASS RESPECTIVELY
            receivedPacket = GUI.receive_gui_mode()

            valid, game_end = game.play(receivedPacket, turn)
            while not valid:
                # send a packet back to GUI
                GUI.send_gui_packet(moveValidation=False)
                # receive another one
                receivedPacket = GUI.receive_gui_mode()
                valid, game_end = game.play(receivedPacket, turn)
            LastPlay = receivedPacket[0:2]

        else:
            # Todo Confirm en el Last play of AI_MOVE matches Last play of human in game.play
            AI_move = game.getMove()
            valid, game_end = game.play(AI_move, turn)
            while not valid:
                AI_move = game.getMove()
                valid, game_end = game.play(AI_move, turn)
            LastPlay = AI_move

        turn = 1 - turn  # White turn = 0 , Black Turn = 0
        score, TerrBoard = game.game.getScoreAndTerrBoard()
        gameBoard = game.game.getBoard()

    return score


if __name__ == "__main__":
    go()
