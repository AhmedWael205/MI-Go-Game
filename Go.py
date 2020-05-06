# from Stones import stones
# from Stones import Turn
# import zmq
# import numpy as np
from ServerConfig import server_config
from game import Game

def go():
    Human = input("Do you want human to be black (0 = no, 1 = yes)?")
    Human = int(Human)
    initial_locations = input("Is there an initial board state in a JSON file (0 = no, 1 = yes)? ")
    if int(initial_locations):
        file_name = input("Enter the JSON file name: ")
        game = server_config(file_name)
    else:
        game = Game()
    game_end = False
    score, TerrBoard = game.game.getScoreAndTerrBoard()
    turn = game.turn
    while not game_end:
        valid = False
        if turn == Human:
            # Recieve from GUI a packet
            """
            0 -> Resign
            1 -> Pass
            (row, column, turn) -> move
            """
            recievedPacket = 0
            valid, game_end = game.play((recievedPacket),turn)
            while not valid:
                # send a packet back to GUI
                # recieve another one
                valid, game_end = game.play((recievedPacket),turn)
            LastPlay = recievedPacket
        else:
            AI_move = game.getMove()
            valid, game_end = game.play((AI_move),turn)
            while not valid:
                AI_move = game.getMove()
                valid, game_end = game.play((AI_move),turn)
            # send Move to GUI
            LastPlay = AI_move

        turn = 1 - turn  # White turn = 0 , Black Turn = 0
        score, TerrBoard = game.game.getScoreAndTerrBoard()
        gameBoard = game.game.getBoard()

    return score


if __name__ == "__main__":
    go()
