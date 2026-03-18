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
        self.sMap = [[self.X_COLS] * self.Y_ROWS]
        self.expRes = {}

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
    def __verifyPos(self, X, Y, funcName) -> bool:
        if X < 0 or X > 8 or Y < 0 or Y > 8:
            sys.exit(f"value X or Y: ({X},{Y}) beyond boundaries, function call: {funcName}")
        else:
            return True

    def __verifyGameFromPos(self, X, Y) -> bool:
        # get the num cell multiplier to apply to the X, Y position
        x_cell, y_cell = math.floor(X/3) + 1, math.floor(Y/3) + 1

    
        


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

    s.bruteForceSolve(1, "1")
    s.heuristicsSolve(2, "2")
    s.heuristicsSolve(2, "67") # repeat

    s.displayExpRes(1)
    s.displayExpRes(2)
    s.displayExpRes(3)
