import copy
import random
import numpy as np
from FeatureExtractor import extractorFunctions as ef
from keras.models import Sequential, load_model, Model

class Node:
    def __init__(self, turn, currentGame=None, parentNode=None, parentMove=None, parentMoveProbability=None, value=0):
        self.currentGame = currentGame
        self.parentMoveProbability = parentMoveProbability
        self.turn = turn  # objective turn, 1 if whiteplayer, -1 if blackplayer
        self.parentNode = parentNode
        self.parentMove = parentMove
        self.moveProbabilities = []
        self.children = {}
        self.N = 0
        self.W = 0  # objective value, 1 if white wins, -1 if black wins

    def isLeaf(self):
        if self.children == {}:
            return True
        else:
            return False

    def getNNInput(self):
        NNInput = []

        gameBoard = self.currentGame.getBoard()
        stoneAge = self.currentGame.stoneAge
        opponentRank = 9
        _, terrBoard = self.currentGame.getScoreAndTerrBoard()

        my1Lib, my2Lib, my3Lib, opp1Lib, opp2Lib, opp3Lib = ef.getLiberties(gameBoard, self.turn)
        #myKo = ef.getKo(gameBoard, self.turn, self.currentGame)

        ourStones, opponentStones, emptyPositions = ef.getStoneOwnership(gameBoard, self.turn)
        ourStoneHistory, opponentStoneHistory = ef.getStoneHistory(stoneAge, ourStones, opponentStones)
        rank1, rank2, rank3, rank4, rank5, rank6, rank7, rank8, rank9 = ef.getOpponentRank(opponentRank)
        border = ef.getBorder()
        positionMask = ef.getPositionMask()
        ourTerritories, opponentTerritories = ef.getTerriroties(terrBoard, self.turn)

        NNInput.extend([my1Lib, my2Lib, my3Lib, opp1Lib, opp2Lib, opp3Lib])
        #NNInput.extend([myKo])
        NNInput.extend([ourStones, opponentStones, emptyPositions])
        NNInput.extend([ourStoneHistory, opponentStoneHistory])
        NNInput.extend([rank1, rank2, rank3, rank4, rank5, rank6, rank7, rank8, rank9])
        NNInput.extend([border, positionMask])
        NNInput.extend([ourTerritories, opponentTerritories])

        NNInput = np.asarray(NNInput)
        return NNInput

########################################################################################################################

class MCT:
    def __init__(self, rootNode):
        self.rootNode = rootNode

    def selectLeaf(self):
        currentNode = self.rootNode

        while not currentNode.isLeaf():
            maxQU = -np.inf
            for child in currentNode.children.values():
                U = child.parentMoveProbability * np.sqrt(currentNode.N) / (1 + child.N)
                Q = 0 if child.N == 0 else (child.W * self.rootNode.turn) / child.N # multiply by self.rootNode.turn because W is objective, so multiplying by self.rootNode.turn will make W subjective
                if Q + U > maxQU:
                    maxQU = Q + U
                    chosenNode = child

            currentNode = chosenNode

        return currentNode

    def isLeafValid(self, leafNode):
        if leafNode == self.rootNode:
            return True
        else:
            tempGame = copy.deepcopy(leafNode.parentNode.currentGame)
            move = (leafNode.parentMove // 19, leafNode.parentMove % 19)
            if leafNode.parentMove == 361:  # PASS Move
                leafNode.currentGame = tempGame
                return True
            elif tempGame.AddStone(move, int(leafNode.parentNode.turn == -1)):
                leafNode.currentGame = tempGame
                return True
            else:
                del leafNode.parentNode.children[leafNode.parentMove]
                return False

    def expandLeaf(self, leafNode: Node, model):
        if self.isLeafValid(leafNode):
            moveProbabilities = model.predict(np.asarray([leafNode.getNNInput()]))[0][0]  #TODO: place the NN function here

            # empty = np.append(np.reshape(leafNode.currentGame.getBoard() == 0, 361), True)
            #moveProbabilities = moveProbabilities[empty]

            for moveIndex, moveProbability in enumerate(moveProbabilities):
                # if empty[moveIndex]:
                leafNode.children[moveIndex] = Node(turn=-leafNode.turn, parentNode=leafNode, parentMove=moveIndex, parentMoveProbability=moveProbability)
            return True
        else:
            return False


    def simulateLeaf(self, leafNode: Node, model):
        modelValue = model.predict(np.asarray([leafNode.getNNInput()]))[0]
        leafValue = (int(modelValue > 0)*2 - 1) * leafNode.turn # NN.getLeafValue(leafNode.getNNInput()) #TODO: place the value network function here
        return leafValue

    def backpropagateLeafValue(self, node, leafValue):
        node.N += 1
        node.W += leafValue
        if node.parentNode is None:
            return
        else:
            self.backpropagateLeafValue(node.parentNode, leafValue)

    def pickMove(self):
        maxN = -1
        for child in self.rootNode.children.values():
            if child.N > maxN:
                maxN = child.N
                chosenNode = child
        self.rootNode = chosenNode
        self.rootNode.parentNode = None
        return self.rootNode.parentMove
