#!/usr/bin/env python
# coding: utf-8

# System couldn't find module so I had to add the path of my installed modules
# Need to figure out how to do it on device
import sys


# needed imports for communication protocol
import asyncio
import websockets
import logging
import json
import enum
from ServerConfig import server_config
from GUIcommunication import GuiComm



# To access the name of an Enum you should add .name to you variable
class ClientState(enum.Enum):
    INIT = 1  # The client is initializing the connection with the server
    READY = 2  # The client is ready to start a game
    IDLE = 3  # The client is waiting for the opponent's move
    THINKING = 4  # The client is thinking of a move
    AWAITING_MOVE_RESPONSE = 5  # The client is awaiting the server's response about the move (VALID or INVALID)


class Client:
    # Taken from command line for future purposes
    # name of the team
    name = "GG"
    url = "ws://localhost:8080"
    disconnectdict = {"type": "DISCONNECTION"}

    def __init__(self,name=None,url=None):
        self.state = ClientState.INIT  # At first the client starts from INIT state will change accordingly
        self.color = None
        # initializing Snd and Rcv Dictionaries
        self.rcvdict = dict()
        self.snddict = dict()
        self.game = None
        self.move = None
        self.time = None
        if name is not None:
            self.name = name
        if url is not None:
            self.url = url
        self.pause = False




async def main2(GUIObject=None,name=None,url=None):
    if GUIObject == None:
        GUI = GuiComm()
    else:
        GUI = GUIObject
    # receivedPacket = GUI.receive_gui_mode()
    # GUI.send_gui_packet()
    # mode = receivedPacket[0]
    # if mode ==1:
    #     return
    C = Client(name,url)
    while True:
        async with websockets.connect(C.url) as websocket:
            while True:
                # Testing
                print(not websocket.open)
                if (not websocket.open):
                    websocket = await websockets.connect(C.url)
                try:
                    # Received String from websocket
                    JRCV = await websocket.recv()
                    # convert from string to dictionary after recv
                    C.rcvdict = json.loads(JRCV)
                    # Testing
                    print("RCV: ", C.rcvdict)
                    # Process with the Implementation what we received and receive a dictionary to send to server
                    await ProcessEvent(C, websocket,GUI)
                    # Testing
                    print("In Main: ", C.state.name)
                except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosed) as e:
                    print(e)
                    C.rcvdict = C.disconnectdict
                    await ProcessEvent(C, websocket,GUI)
                    print("In Except: ", C.state.name)
                    break


async def ProcessEvent(C, websocket,GUI):
    if (C.rcvdict["type"] == "END"):
        print("Game ended")
        print("Reason ", C.rcvdict["reason"])
        print("Winner ", C.rcvdict["winner"])
        if(C.rcvdict["reason"]=="pause"):
            C.pause = True
        else:
            C.pause = False
        C.state = ClientState.READY
        return
    elif (C.rcvdict["type"] == "DISCONNECTION"):
        C.state = ClientState.INIT
        return
    else:
        if (C.state == ClientState.INIT):
            if (C.rcvdict["type"] == "NAME"):
                C.snddict["type"] = "NAME"
                C.snddict["name"] = C.name
                JSND = json.dumps(C.snddict)
                C.state = ClientState.READY
                await websocket.send(JSND)
                # Testing
                print("In PE: ", C.state.name)
                print("SND: ", C.snddict)
                return
        elif (C.state == ClientState.READY):
            if (C.rcvdict["type"] == "START"):

                # to be sent to the Agent
                GameConfig = C.rcvdict["configuration"]

                # Call func Initialize game
                if(not C.pause):
                    C.game = server_config(GameConfig=GameConfig,GuiObject=GUI)
                else:
                    C.game = C.game
                
                GameState = GameConfig["initialState"]
                C.color = C.rcvdict["color"]
                if C.color == "B":
                    C.game.setOurTurn(1)
                else:
                    C.game.setOurTurn(0)

                # if true that means that it's our turn
                if (((C.color == GameState["turn"]) and (len(GameConfig["moveLog"]) % 2 == 0)) or (
                        (C.color != GameState["turn"]) and (len(GameConfig["moveLog"]) % 2 != 0))):
                    # Need to generate new move to send to server
                    C.time = [GameState["players"]["W"],GameState["players"]["B"]]
                    C.state = ClientState.THINKING
                    await ProcessEvent(C, websocket,GUI)
                else:
                    # will wait for opponent move in that
                    C.state = ClientState.IDLE
        elif (C.state == ClientState.THINKING):
            C.snddict["type"] = "MOVE"
            C.snddict["move"] = dict()
            # This means eno kan el dor 3alaya w da awel move fel game aw eno galy oponent move aw kunt ba3ta invlaid move
            if (C.rcvdict["type"] == "START" or C.rcvdict["type"] == "MOVE"):
                # call func generate move
                C.move = C.game.getMove(invalid = False)
            elif (C.rcvdict["type"] == "INVALID"):
                C.move = C.game.getMove(invalid = False)

            if (C.move == 0):
                m = {"type": "resign"}
            elif (C.move == 1):
                m = {"type": "pass"}
            else:
                m = {"type": "place", "point": {"row": int(C.move[0]), "column": int(C.move[1])}}

            print("C.snddict[move]: ", m)
            print("C.snddict: ", C.snddict)

            C.snddict["move"] = m
            JSND = json.dumps(C.snddict)
            await websocket.send(JSND)
            C.state = ClientState.AWAITING_MOVE_RESPONSE
        elif (C.state == ClientState.IDLE):
            if (C.rcvdict["type"] == "MOVE"):
                C.time = [C.rcvdict["remainingTime"]["W"], C.rcvdict["remainingTime"]["B"]]
                # call func to SEND opponent move to agent
                OppMove = C.rcvdict["move"]
                if (OppMove["type"] == "resign"):
                    C.game.play(0, Debugging=True, Time = C.time)
                elif (OppMove["type"] == "pass"):
                    C.game.play(1, Debugging=True, Time = C.time)
                else:
                    PlaceMove = OppMove["point"]
                    if (C.color == 'B'):
                        turn = 0
                    else:
                        turn = 1
                    MoveTuple = (PlaceMove["row"], PlaceMove["column"], turn)
                    C.game.play(MoveTuple, Debugging=True, Time = C.time)

                C.state = ClientState.THINKING
                await ProcessEvent(C, websocket,GUI)
        elif (C.state == ClientState.AWAITING_MOVE_RESPONSE):
            if (C.rcvdict["type"] == "INVALID"):
                print("Invalid Reason ", C.rcvdict["message"])
                C.time = [C.rcvdict["remainingTime"]["W"], C.rcvdict["remainingTime"]["B"]]
                C.state = ClientState.THINKING
                await ProcessEvent(C, websocket,GUI)
            else:
                C.time = [C.rcvdict["remainingTime"]["W"], C.rcvdict["remainingTime"]["B"]]
                # SEND to agent that they should save last move
                if (C.move == 0):
                    C.game.play(0, Debugging=True, Time = C.time)
                elif (C.move == 1):
                    C.game.play(1, Debugging=True, Time = C.time)
                else:
                    if (C.color == 'B'):
                        turn = 1
                    else:
                        turn = 0
                    MoveTuple = (C.move[0], C.move[1], turn)
                    C.game.play(MoveTuple, Debugging=True, Time = C.time)
                C.state = ClientState.IDLE
        return

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
    main2()

# loop = asyncio.get_event_loop()
# asyncio.ensure_future(main2())
# loop.run_forever()
