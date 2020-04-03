import numpy as np
from enum import IntEnum


class Position(IntEnum):
    black = -1
    empty = 0
    white = 1

class Turn(IntEnum):
    black = 1
    white = 0


class stones:
    _Wgroup = []
    _LWgroup = []
    _Bgroup = []
    _LBgroup = []
    _Egroup = [[(i, j) for i in range(19) for j in range(19)]]
    _Groups = [_Wgroup, _Bgroup,_Egroup]
    _LGroups = [_LWgroup, _LBgroup]
    _CapturedStones = [0,0]


########################################################################################################################
    def __init__(self, wloc=[], bloc=[]):
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
        print(self._board)
        # print(self._Groups)

        self._CreateLibs()
        self._LGroups = [self._LWgroup, self._LBgroup]
        #print(self._LGroups)

########################################################################################################################

    def AddStone(self, location, turn):
        if location[0] < 0 or location[1] < 0 or self._board[location[0]][location[1]] != Position.empty:
            print("Invalid Location")
            return False
        self._board[location[0]][location[1]] = turn
        if self._EatGroups(location,turn):
            self._UpdateMyGroups(location,turn)

        else:
            if turn == 1:
                a = Position.black
            else:
                a= Position.white

            Suicide = True
            for x in [(location[0] + 1, location[1]), (location[0] - 1, location[1]),
                      (location[0], location[1] + 1),
                      (location[0], location[1] - 1)]:
                if x[0] < 0 or x[1] < 0 or x[0] > 18 or x[1]> 18:
                    continue
                if self._board[x[0]][x[1]] == a:
                    Suicide = False
                    break
            if not Suicide:
                for group in self._LGroups[turn]:
                    if len(group) == 1 and group == [location]:
                        Suicide = True

            if Suicide:
                print("Suicide Move")
                return False
            else:
                self._UpdateMyGroups(location, turn)
                self._UpdateEmpty(location)
        self._UpdateBoard()
        print(self._board)
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
        for Groups,LGroups in [(self._Groups[0],self._LGroups[0]), (self._Groups[1],self._LGroups[1])]:
            count = 0
            for Group in Groups:
                LGroups.append([])
                for location in Group:
                    for x in [(location[0] + 1, location[1]), (location[0] - 1, location[1]), (location[0], location[1] + 1), (location[0], location[1] - 1)]:
                        if x[0] < 0 or x[1] < 0 or x[0] > 18 or x[1]> 18:
                            continue
                        if self._board[x[0]][x[1]] == Position.empty:
                            if x not in LGroups[count]:
                                LGroups[count].append(x)
                count = count + 1

########################################################################################################################
    def _EatGroups(self, location, turn):
        Eat = False
        for group in self._LGroups[1 - turn]:
            if location in group:
                if len(group) == 1:
                    print("Eat Group")
                    removedGroup = self._LGroups[1 - turn].index([location])
                    self._CapturedStones[turn] = self._CapturedStones[turn] + len(self._Groups[1 - turn][removedGroup])
                    self._UpdateEmpty(location, self._Groups[1 - turn][removedGroup][:])
                    self._LGroups[1 - turn].remove([location])
                    self._Groups[1 - turn].pop(removedGroup)
                    Eat = True
                else:
                    self._UpdateEmpty(location)
                    affectedGroup = self._LGroups[1 - turn].index(group)
                    self._LGroups[1 - turn][affectedGroup].remove(location)
                    Eat = False

        return Eat
########################################################################################################################
    def _UpdateMyGroups(self,location,turn):
        loc = []
        for group in self._LGroups[turn]:
            if location in group:
                loc.append(self._LGroups[turn].index(group))
                group.remove(location)
        NewLib = []
        NewGroup = [location]

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
        if len(NewLib) == 0:
            for x in [(location[0] + 1, location[1]), (location[0] - 1, location[1]), (location[0], location[1] + 1),
                      (location[0], location[1] - 1)]:
                if x[0] < 0 or x[1] < 0 or x[0] > 18 or x[1]> 18:
                    continue
                NewLib.append((x[0], x[1]))
        self._LGroups[turn].append(NewLib)
        self._Groups[turn].append(NewGroup)

########################################################################################################################
#TODO remove empty space recreate empty groups
    def _UpdateEmpty(self,AddedLocation,RemovedLocations = []):
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
    def _UpdateBoard(self):
        self._board = np.zeros((19, 19), dtype=int)
        for group in self._Bgroup:
            for location in group:
                self._board[location[0]][location[1]] = -1
        for group in self._Wgroup:
            for location in group:
                self._board[location[0]][location[1]] = 1

########################################################################################################################
    def Score(self):
        territory = self._CalcTerr()
        count = 6.5 + self._CapturedStones [0]
        for group in self._Wgroup:
            count = count + len(group)
        territory[0] = territory[0] + count

        count = self._CapturedStones [1]
        for group in self._Bgroup:
            count = count + len(group)
        territory[1] = territory[1] + count
        return territory

########################################################################################################################
    def _CalcTerr(self):
        Terr = [0,0]
        for group in self._Egroup:
            state = -1 #0: all 2:black 1: white
            count = 0
            for location in group:
                count = count + 1
                for x in [(location[0] + 1, location[1]), (location[0] - 1, location[1]),
                          (location[0], location[1] + 1),
                          (location[0], location[1] - 1)]:
                    if x[0] < 0 or x[1] < 0 or x[0] > 18 or x[1]> 18:
                        continue
                    elif self._board[x[0]][x[1]] == 1 and (state == 1 or state == -1):
                        state = 1
                    elif self._board[x[0]][x[1]] == -1 and (state == 2 or state == -1):
                        state = 2
                    elif self._board[x[0]][x[1]] != 0:
                        state = 0


            if state != 0:
                Terr[state-1] = Terr[state-1] + count
        return Terr
########################################################################################################################
A = stones([(1, 0), (2, 1), (0, 1), (2, 2),(1, 3),(18,16),(17,16),(16,18),(16,17)], [ (2, 3),(1,2)])
A.AddStone((1,1),0)
A.AddStone((0,2),0)
print(A.Score())