import copy
from FeatureExtractor import MCTS
from Stones import stones
import time
class Agent:
    def __init__(self, turn, Pmodel, Vmodel, mctSims):
        self.mctSims = mctSims
        self.turn = turn  # 1 if white, -1 if black
        self.mct = None
        self.Pmodel = Pmodel
        self.Vmodel = Vmodel

    def makeMove(self, game: stones, lastPlayerMove):
        currentGame = copy.deepcopy(game)


        if lastPlayerMove == -1 or self.mct is None:
            rootNode = MCTS.Node(currentGame=currentGame, turn=self.turn)
            self.mct = MCTS.MCT(rootNode)
        else:
            self.mct.rootNode = self.mct.rootNode.children[lastPlayerMove]
            if self.mct.rootNode.currentGame is None:
                self.mct.rootNode.currentGame = currentGame

        #now = time.perf_counter()
        for i in range(self.mctSims):
            leafNode = self.mct.selectLeaf()
            if self.mct.expandLeaf(leafNode, self.Pmodel):
                leafValue = self.mct.simulateLeaf(leafNode, self.Vmodel)
                self.mct.backpropagateLeafValue(leafNode, leafValue)
        #print(time.perf_counter() - now)
        chosenMove = self.mct.pickMove()
        return chosenMove

