import numpy as np
from enum import IntEnum


class Position(IntEnum):
    black = -1
    empty = 0
    white = 1


class stones:
    _Wgroup = []
    _LWgroup = []
    _Bgroup = []
    _LBgroup = []
    _Egroup = [[(i, j) for i in range(19) for j in range(19)]]
    _Groups = [_Wgroup, _Bgroup,_Egroup]
    _LGroups = [_LWgroup, _LBgroup]


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
        print(self._LGroups)

########################################################################################################################

    # TODO Kmal el function
    def AddStone(self, location, turn):
        if self._board[location[0]][location[1]] != Position.empty:
            print("Invalid Location ")
            return False
        self._board[location[0]][location[1]] = turn

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
            count = 0;
            for Group in Groups:
                LGroups.append([])
                for location in Group:
                    for x in [(location[0] + 1, location[1]), (location[0] - 1, location[1]), (location[0], location[1] + 1), (location[0], location[1] - 1)]:
                        if x[0] < 0 or x[1] < 0:
                            continue
                        if self._board[x[0]][x[1]] == Position.empty:
                            if x not in LGroups[count]:
                                LGroups[count].append(x)
                count = count + 1

########################################################################################################################

A = stones([(1, 0), (2, 1), (0, 1), (1, 2), (1, 1)], [(2, 2), (3, 3), (2, 3)])
