import sys
import math
from tkinter import *

"""
81 squares, split into 9 blocks containing 9 squares in a 3x3 brid
each of the 9 blocks has to contain all numbers 1-9 in their squares
each vertical and horizontal squares must also contain 1-9 uniquely
every sudoku has "exactly" one correct solution
case corresponds with a unique sudoku map
"""

"""
TERMINOLOGY:
    cell: a 3x3 grid
    sMap = the sudoku map
    expRes = a dictionary containing a unique lookup ID, and the results (this is tentative)
"""

class SudokuWorld:
    def __init__(self):
        self.X_COLS = 9
        self.Y_ROWS = 9
        self.sMap = [[0] * self.X_COLS] * self.Y_ROWS
        self.expRes = dict()

    # Add a new experiment result with key ID
    def __addExpRes(self, ID, res):
        if self.__isIDInExpRes(ID): # secondary checks
            print(f"ID {ID} already populated, failed to add to expRes.")
            return
        print(f"adding new ID {ID} and res")
        self.expRes[ID] = res
        return

    # Verify if ID is already in expRes
    def __isIDInExpRes(self, ID) -> bool:
        return True if ID in self.expRes else False # primary check

    # verify position being checked before proceeding, will terminate program if not a valid position
    def __verifyPos(self, X_POS, Y_POS, funcName) -> bool:
        if X_POS < 0 or X_POS >= self.X_COLS or Y_POS < 0 or Y_POS >= self.Y_ROWS:
            sys.exit(f"value X or Y: ({X_POS},{Y_POS}) beyond boundaries, function call: {funcName}")
        else:
            return True

    def __verifyGameFromPos(self, X_POS, Y_POS) -> bool:
        # get the num cell multiplier to apply to the X, Y position
        x_cell, y_cell = math.floor(X_POS / 3) + 1, math.floor(Y_POS / 3) + 1

        # verify in cell all numbers are unique
        s = set()
        for y in range(3):
            for x in range(3):
                valAtPos = self.expRes[(y_cell * 3) + y][(x_cell * 3) + x]
                if valAtPos != 0:
                    if valAtPos not in s:
                        s.add(valAtPos)
                    else:
                        print(f"[verifyGameFromPos] rep. found in grid xcell: {x_cell}, ycell: (y_cell)")
                        print(self.sMap)
                        return False # repeat found
                continue
        
        # verify x col is unique
        s.clear()
        for x in range(self.X_COLS + 1):
            valAtPos = self.expRes[Y_POS][x]
            if valAtPos != 0:
                if valAtPos not in s:
                    s.add(valAtPos)
                else:
                    print(f"[verifyGameFromPos] rep. found in X row, val: {valAtPos} at X: {x}, Y: {Y_POS}")
                    print(self.sMap)
                    return False # repeat found
            continue

        # verify y row is unique
        s.clear()
        for y in range(self.Y_ROWS + 1):
            valAtPos = self.expRes[y][X_POS]
            if valAtPos != 0:
                if valAtPos not in s:
                    s.add(valAtPos)
                else:
                    print(f"[verifyGameFromPos] rep. found in Y row, val: {valAtPos} at X: {X_POS}, Y: {y}")
                    print(self.sMap)
                    return False # repeat found
            continue

        return True # all checks passed

    # Display specific results with corresponding ID
    def displayExpRes(self, ID):

        if not self.__isIDInExpRes(ID):
            print(f"ID {ID} is not in expRes, will not display anything")
            return

        print(f"displaying result for {ID} below") # will be implemented via tkinter
        print(self.expRes[ID])

    # Display ALL results
    def expResSummary(self):
        print("displays experiment summary") # will be implemented via tkinter

    # Clear ALL experiment results
    def clearExpRes(self):
        self.expRes.clear()

    # Brute force solve experiment
    def bruteForceSolve(self, ID, case):
        if self.__isIDInExpRes(ID):
            print(f"{ID} is not unique. terminate brute force solver for case {case}")
            return

        print(f"brute force solve case {case}, ID {ID}")
        res = f"results for case {case} ID {ID} brute force"
        self.__addExpRes(ID, res)

    # Heuristics solve experiment
    def heuristicsSolve(self, ID, case):
        if self.__isIDInExpRes(ID):
            print(f"{ID} is not unique. terminate heuristics solver for case {case}")
            return

        print(f"heuristics solve case {case}, ID {ID}")
        res = f"results for case {case} ID {ID} heuristics"
        self.__addExpRes(ID, res)

# main func
if __name__==__name__:
    s = SudokuWorld()

    # s.bruteForceSolve(1, "1")
    # s.heuristicsSolve(2, "2")
    # s.heuristicsSolve(2, "67") # repeat
    #
    # s.displayExpRes(1)
    # s.displayExpRes(2)
    # s.displayExpRes(3)

    print(s.sMap)
