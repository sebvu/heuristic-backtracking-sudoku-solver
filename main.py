from tkinter import *

# 81 squares, split into 9 blocks containing 9 squares in a 3x3 brid
# each of the 9 blocks has to contain all numbers 1-9 in their squares
# each vertical and horizontal squares must also contain 1-9 uniquely
# every sudoku has "exactly" one correct solution
# case corresponds with a unique sudoku map
class SudokuWorld:
    def __init__(self):
        self.WIDTH = 81
        self.HEIGHT = 81
        self.expRes = {}

    def __addExpRes(self, ID, res):
        if self.__isIDInExpRes(ID): # secondary checks
            print(f"ID {ID} already populated, failed to add to expRes.")
            return
        print(f"adding new ID {ID} and res")
        self.expRes[ID] = res
        return

    def __isIDInExpRes(self, ID) -> bool:
        return True if ID in self.expRes else False # primary check

    def displayExpRes(self, ID):

        if not self.__isIDInExpRes(ID):
            print(f"ID {ID} is not in expRes, will not display anything")
            return

        print(f"displaying result for {ID} below") # will be implemented via tkinter
        print(self.expRes[ID])

    def expResSummary(self):
        print("displays experiment summary") # will be implemented via tkinter

    def clearExpRes(self):
        self.expRes.clear()

    def bruteForceSolve(self, ID, case):
        if self.__isIDInExpRes(ID):
            print(f"{ID} is not unique. terminate brute force solver for case {case}")
            return

        print(f"brute force solve case {case}, ID {ID}")
        res = f"results for case {case} ID {ID} brute force"
        self.__addExpRes(ID, res)

    def heuristicsSolve(self, ID, case):
        if self.__isIDInExpRes(ID):
            print(f"{ID} is not unique. terminate heuristics solver for case {case}")
            return

        print(f"heuristics solve case {case}, ID {ID}")
        res = f"results for case {case} ID {ID} heuristics"
        self.__addExpRes(ID, res)

if __name__==__name__:
    s = SudokuWorld()

    s.bruteForceSolve(1, "1")
    s.heuristicsSolve(2, "2")
    s.heuristicsSolve(2, "67") # repeat

    s.displayExpRes(1)
    s.displayExpRes(2)
    s.displayExpRes(3)

    s.expResSummary()
