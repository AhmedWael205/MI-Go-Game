import json
import numpy as np
from game import Game
from Stones import Turn


def server_config(FileName):
    with open(FileName, 'r') as f:
        GameConfig = json.load(f)

    # TODO DO we need reamining time of anything at the initalization state(begining of the game from a certain stage)
    GameState = GameConfig["initialState"]
    moveLogJsonArr = GameConfig["moveLog"]

    wloc = list(zip(*np.where((np.array(GameState["board"])) == "W")))
    bloc = list(zip(*np.where((np.array(GameState["board"])) == "B")))
    bCaptured = GameState["players"]["W"]["prisoners"]
    wCaptured = GameState["players"]["B"]["prisoners"]

    gameArgs = {"wloc": wloc, "bloc": bloc,
                "wCapturedStones": wCaptured,
                "bCapturedStones": bCaptured}

    # TODO  Check for any misplaced argument and if initalization of any argument can affect other class members
    """
    instance of backend game supposed to be only one instancec
    """
    backEndGame = Game(**gameArgs)

    turn = Turn.black if GameState["turn"] == "B" else Turn.white

    """
    logically speaking yahia should not send resign move at the begining
    """
    """
        Taking the move log and adding stones till we reach final state to begin with
    """
    for move in moveLogJsonArr:

        if move["move"]["type"] == "place":
            x=backEndGame.play(
                (move["move"]["point"]["row"],move["move"]["point"]["column"]), turn)
            #gameBoard = backEndGame.getBoard()
            #print(gameBoard)
            if(not x):
                print("Error in location",(move["move"]["point"]["row"],move["move"]["point"]["column"]),turn)
                backEndGame.Drawboard()
                input('Press any key ...')
        elif (move["move"]["type"] == "pass"):
            pass
        elif (move["move"]["type"] == "resign"):
            # TODO handle resign at game config(illogical)
            print("Error in parsing JSON FILE AT GAME INIT CONFIG")
        else:
            # TODO handle error at game config
            pass
            print("Error in parsing JSON FILE AT GAME INIT CONFIG")
        turn = 1 - turn
        #backEndGame.Drawboard()
        #input('Press any key ...')

    #score, TerrBoard = backEndGame.getScoreAndTerrBoard()
    #print(score)
    """"
    NOW instance backEnd stage is initialized with the data parsed
    """

    return backEndGame
