import numpy as np
from enum import IntEnum
import copy

class Position(IntEnum):
    black = -1
    empty = 0
    white = 1


class Turn(IntEnum):
    black = 1
    white = 0


"""

data members:
    _Wgroup: a list of white groups where each group is a list of tuple where each tuple is x-y coordinates
    _LWgroup: a list of of groups where each index corresponds to the liberties of the group at the same index in _Wgroup
                _LWgroup[i] = Liberties(_Wgroup[i])
    _Bgroup: a list of black groups where each group is a list of tuple where each tuple is x-y coordinates
    _LBgroup: a list of of groups where each group corresponds to the liberties of the group at the same index in _Bgroup
                _LBgroup[i] = Liberties(_Bgroup[i])
    _Egroup: a list of empty groups where each group is a list of tuple where each tuple is x-y coordinates
        initially one group with all board locations
    _Group: a list of _Wgroup, _Bgroup, _Egroup
    _LGroup: a list of _LWgroup, _LBgroup
    _CapturedStones: a two element list where each one represent the number of captured stones of the other team
        _CapturedStones[0] = captured black stones, _CapturedStones[1] = captured white stones
    _WPreviousBoardStates: Previous board states when it was white player turn
    _BPreviousBoardStates: Previous board states when it was black player turn
    _PreviousBoardStates: a two element list where each list represent the previous states of a certain player
        _PreviousBoardStates[0] = _WPreviousBoardStates,  _PreviousBoardStates[1] = _BPreviousBoardStates
    _WhiteTerr: a list of groups where each one represent a group of empty places that are considered as white territory
    _BlackTerr: a list of groups where each one represent a group of empty places that are considered as black territory
    _TerrGroups: a two element list where each element represent a list of certain players territories
        _TerrGroups[0] = _WhiteTerr, _TerrGroups[1] = _BlackTerr
    _board: a 19*19 matrix where each element represent whether it is empty or black stone or white stone
        _board[i][j] = 0 -> Empty, _board[i][j] = 1 -> White stone, _board[i][j] = -1 -> Black stone
    stoneAge: a 19*19 matrix where each element represent the number of moves that a stones at that location has been placed
        stoneAge[i][j] = Number of Turns Stone Exists at  _board[i][j] (if its empty then 0)

member functions:
    //TODO 

"""

class stones:

    ########################################################################################################################
    def __init__(self, wloc=[], bloc=[], bCapturedStones=0, wCapturedStones=0):
        self._Wgroup = []
        self._LWgroup = []
        self._Bgroup = []
        self._LBgroup = []
        self._Egroup = [[(i, j) for i in range(19) for j in range(19)]]
        self._Groups = [self._Wgroup, self._Bgroup, self._Egroup]
        self._LGroups = [self._LWgroup, self._LBgroup]
        self._CapturedStones = [wCapturedStones, bCapturedStones]
        self._WPreviousBoardStates = []
        self._BPreviousBoardStates = []
        self._PreviousBoardStates = [self._WPreviousBoardStates, self._BPreviousBoardStates]
        self._BlackTerr = []
        self._WhiteTerr = []
        self._TerrGroups = [self._WhiteTerr, self._BlackTerr]
        self.stoneAge = np.zeros((19, 19), dtype=int)

        self._board = np.zeros((19, 19), dtype=int)
        if len(wloc) != 0:
            for location in wloc:
                self._board[location[0]][location[1]] = Position.white
            self._CreateGroups(wloc, "w")

        if len(bloc) != 0:
            for location in bloc:
                self._board[location[0]][location[1]] = Position.black
            self._CreateGroups(bloc, "b")
        self._Egroup = self._CreateGroups(self._Egroup[0][:], "e")
        self._Groups = [self._Wgroup, self._Bgroup, self._Egroup]
        # print(self._board)
        # print(self._Groups)

        self._CreateLibs()
        self._LGroups = [self._LWgroup, self._LBgroup]
        self.stoneAge = np.where(self._board, 1, 0)
        # print(self._LGroups)

    ########################################################################################################################
    def checkKo(self, glocation, turn):
        location = (int(glocation[0]), int(glocation[1]))

        if turn == 1:
            color = Position.black
        else:
            color = Position.white

        tempGame = copy.deepcopy(self)

        if self._EatGroups(location, turn, color):
            self._UpdateGroups(location, turn, color)

        elif self._SuicideMove(location, turn):
            return False
        else:
            self._UpdateGroups(location, turn, color)
            self._UpdateEmpty(location)
            self._UpdateBoard(location, color)

        if not self._CheckState(self._board, self._PreviousBoardStates[turn]):
            self.__dict__.update(tempGame.__dict__)
            return True
        else:
            self.__dict__.update(tempGame.__dict__)
            return False



    def AddStone(self, glocation, turn,test = 0):
        location = (int(glocation[0]),int(glocation[1]))
        # print(location)
        if location[0] < 0 or location[1] < 0 or location[0] > 18 or location[1] > 18 or self._board[location[0]][location[1]] != Position.empty:
            print("Invalid Location")
            return False

        if turn == 1:
            color = Position.black
        else:
            color = Position.white
        eat = False
        if test:
            self._UpdateGroups(location, turn, color)
            return True

        tempGame = copy.deepcopy(self)

        if self._EatGroups(location, turn,color):
            eat = True
            self._UpdateGroups(location, turn,color)

        elif self._SuicideMove(location,turn):
            print("Suicide Move")
            return False
        else:
            self._UpdateGroups(location, turn,color)
            self._UpdateEmpty(location)
            self._UpdateBoard(location,color)


        if  not self._CheckState(self._board,self._PreviousBoardStates[turn]):
            print("Super KO")
            self.__dict__.update(tempGame.__dict__)
            return False

        if eat:
            print("Eat Group")
        self._PreviousBoardStates[turn].append(np.copy(self._board))
        self.stoneAge = np.where(self._board, self.stoneAge + 1, 0)
        self.stoneAge[location[0]][location[1]] = 1
        return True

    ########################################################################################################################
    def _CreateGroups(self, locations, Group):
        if Group == "w":
            Cgroup = self._Wgroup
        elif Group == "b":
            Cgroup = self._Bgroup
        else:
            Cgroup = self._Egroup
            Cgroup = []

        for location in locations:
            notlocated = True

            for group in Cgroup:
                if location in group:
                    notlocated = False
                    break

            if notlocated:
                for x in [(location[0] + 1, location[1]), (location[0] - 1, location[1]),
                          (location[0], location[1] + 1),
                          (location[0], location[1] - 1)]:
                    if x[0] < 0 or x[1] < 0 or x[0] > 18 or x[1] > 18:
                        continue
                    for group in Cgroup:
                        if x in group:
                            if notlocated == True:
                                group.append(location)
                                notlocated = False
                                merge = group
                                break  # if x in group:
                            elif x not in merge:
                                for i, j in group:
                                    merge.append((i, j))
                                Cgroup.remove(group)
            if notlocated:
                Cgroup.append([location])
            if Group != "e":
                self._Egroup[0].remove(location)

        return Cgroup

    ########################################################################################################################
    def _CreateLibs(self):
        for Groups, LGroups in [(self._Groups[0], self._LGroups[0]), (self._Groups[1], self._LGroups[1])]:
            count = 0
            for Group in Groups:
                LGroups.append([])
                for location in Group:
                    for x in [(location[0] + 1, location[1]), (location[0] - 1, location[1]),
                              (location[0], location[1] + 1), (location[0], location[1] - 1)]:
                        if x[0] < 0 or x[1] < 0 or x[0] > 18 or x[1] > 18:
                            continue
                        if self._board[x[0]][x[1]] == Position.empty:
                            if x not in LGroups[count]:
                                LGroups[count].append(x)
                count = count + 1

    ########################################################################################################################
    def _EatGroups(self, location, turn,color):
        Eat = False
        for group in reversed(self._LGroups[1 - turn]):
            if location in group and len(group) == 1:
                removedGroup = self._LGroups[1 - turn].index([location])
                self._UpdateBoard(location, color,self._Groups[1 - turn][removedGroup])
                self._CapturedStones[turn] = self._CapturedStones[turn] + len(self._Groups[1 - turn][removedGroup])
                self._UpdateEmpty(location, self._Groups[1 - turn][removedGroup][:])
                self._LGroups[1 - turn].remove([location])
                self._UpdateAffectedLib(self._Groups[1 - turn][removedGroup], turn)
                del self._Groups[1 - turn][removedGroup]
                Eat = True

        return Eat

    ########################################################################################################################
    def _UpdateGroups(self, location, turn,color):
        loc = []
        for group in self._LGroups[turn]:
            if location in group:
                loc.append(self._LGroups[turn].index(group))
                group.remove(location)
        NewLib = []
        NewGroup = [location]

        for x in [(location[0] + 1, location[1]), (location[0] - 1, location[1]), (location[0], location[1] + 1),
                  (location[0], location[1] - 1)]:
            if x[0] < 0 or x[1] < 0 or x[0] > 18 or x[1] > 18:
                continue
            if self._board[x[0]][x[1]] == Position.empty:
                NewLib.append((x[0], x[1]))

        for w in loc:
            for i, j in self._LGroups[turn][w]:
                if (i, j) not in NewLib:
                    NewLib.append((i, j))
            for i, j in self._Groups[turn][w]:
                NewGroup.append((i, j))

        count = 0
        for w in loc:
            self._LGroups[turn].pop(w - count)
            self._Groups[turn].pop(w - count)
            count = count + 1

        self._LGroups[turn].append(NewLib)
        self._Groups[turn].append(NewGroup)

        for group in self._LGroups[1 - turn]:
            if location in group:
                affectedGroup = self._LGroups[1 - turn].index(group)
                self._LGroups[1 - turn][affectedGroup].remove(location)


    ########################################################################################################################
    def _UpdateEmpty(self, AddedLocation, RemovedLocations=[]):
        temp = []
        for group in self._Egroup:
            for location in group:
                if location != AddedLocation:
                    temp.append(location)

        if len(RemovedLocations) != 0:
            for location in RemovedLocations:
                temp.append(location)
        self._Egroup = self._CreateGroups(temp, "e")

    ########################################################################################################################
    def _UpdateBoard(self,AddedLocation,color,RemovedLocations=[]):
        self._board[AddedLocation[0]][AddedLocation[1]] = color
        for location in RemovedLocations:
            self._board[location[0]][location[1]] = 0

    ########################################################################################################################
    def _CheckState(self,FutureState,PrevStates):
        return not any(np.array_equal(FutureState, state) for state in PrevStates)
    ########################################################################################################################
    def getScoreAndTerrBoard(self):
        territory = self._CalcTerr()
        count = 6.5 + self._CapturedStones[0]
        for group in self._Wgroup:
            count = count + len(group)
        territory[0] = territory[0] + count

        count = self._CapturedStones[1]
        for group in self._Bgroup:
            count = count + len(group)
        territory[1] = territory[1] + count
        TerrBoard = self._getTerr()
        return territory,TerrBoard

    ########################################################################################################################
    def _CalcTerr(self):
        Terr = [0, 0]
        self._TerrGroups = [[],[]]
        for group in self._Egroup:
            state = -1  # 0: all 2:black 1: white
            count = 0
            for location in group:
                count = count + 1
                for x in [(location[0] + 1, location[1]), (location[0] - 1, location[1]),
                          (location[0], location[1] + 1),
                          (location[0], location[1] - 1)]:
                    if x[0] < 0 or x[1] < 0 or x[0] > 18 or x[1] > 18:
                        continue
                    elif self._board[x[0]][x[1]] == 1 and (state == 1 or state == -1):
                        state = 1
                    elif self._board[x[0]][x[1]] == -1 and (state == 2 or state == -1):
                        state = 2
                    elif self._board[x[0]][x[1]] != 0:
                        state = 0

            if state > 0:
                Terr[state - 1] = Terr[state - 1] + count
                for x,y in group:
                    self._TerrGroups [state - 1].append((x,y))
        return Terr


########################################################################################################################
    def _SuicideMove(self,location,turn):

        tempGame = copy.deepcopy(self)
        tempGame.AddStone(location,turn,1)
        return tempGame.ChecKSuicide(turn)
    def ChecKSuicide(self,turn):
        for group in self._LGroups[turn]:
            if len(group) == 0:
                return True
        return False

########################################################################################################################
    def getBoard(self):
        return self._board

    def _getTerr(self):
        Terrboard = np.zeros((19, 19), dtype=int)
        for x,y in self._TerrGroups[0]:
            Terrboard[x][y] = 1
        for x,y in self._TerrGroups[1]:
            Terrboard[x][y] = -1
        return Terrboard



########################################################################################################################
    def tryAction(self,location,turn):
        if turn == 1:
            color = Position.black
        else:
            color = Position.white

        FutureBoardState = np.copy(self._board)
        FutureBoardState[location[0]][location[1]] = color

        if not self._CheckState(FutureBoardState, self._PreviousBoardStates[turn]):
            return False

        if self._TryEatGroups(location, turn, color):
            return True
        elif self._SuicideMove(location, turn):
            return False
        return True


    def _TryEatGroups(self, location, turn,color):
        for group in self._LGroups[1 - turn]:
            if location in group and len(group) == 1:
                return True
        return False

########################################################################################################################
    def _UpdateAffectedLib(self,removedGroup,turn):
        for location in removedGroup:
            for x in [(location[0] + 1, location[1]), (location[0] - 1, location[1]),
                      (location[0], location[1] + 1),
                      (location[0], location[1] - 1)]:
                if x[0] < 0 or x[1] < 0 or x[0] > 18 or x[1] > 18:
                    continue
                else:
                    for group in self._Groups[turn]:
                        w = self._Groups[turn].index(group)
                        if x in group and location not in self._LGroups[turn][w]:
                            self._LGroups[turn][w].append(location)

########################################################################################################################

    def Drawboard(self,Board = []):
        if len(Board) == 0:
            Board = self._board
        print ("N\t0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18\t")
        for i in range (19):
            print(i, end="\t")
            for j in range (19):
                if Board[i][j] == 1:
                    print(u"\u2588", end="  ")
                elif Board[i][j] == -1:
                    print("▒", end="  ")
                else:
                    print(".", end="  ")
            print()