import sys
import math
from tkinter import *
import pandas as pd

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
        print(self.expRes[ID]) # temporary method

    # Display ALL results
    def expResSummary(self):
        print("displays experiment summary") # will be implemented via tkinter
        print(self.expRes) # temporary method

    # Clear ALL experiment results
    def clearExpRes(self):
        self.expRes.clear()

    """
    NOTE TO CONTRIBUTORS:
    
    below is the section yall should mainly be focusing on, i.e. the brute force and heuristics function

    in each one, you will be making a call to ID, and case val (refer to cases/ folder for names), make sure to put the
    FULL file name ex. bruteForceSolve(1, "case1.txt"). ID must be unique
    """

    # Brute force solve experiment
    def bruteForceSolve(self, ID, case):
        if self.__isIDInExpRes(ID):
            print(f"{ID} is not unique. terminate brute force solver for case {case}")
            return

        """
        implement brute force solver here
        res should contain in itself some datastructure, maybe a dict as well, that stores the following:
        - solve time
        - number of operations
        - number of explored nodes
        - number of backtracks
        - memory usage (tentative)
        """

        print(f"brute force solve case {case}, ID {ID}")
        res = f"results for case {case} ID {ID} brute force"
        self.__addExpRes(ID, res)

    # Heuristics solve experiment
    def heuristicsSolve(self, ID, case):
        if self.__isIDInExpRes(ID):
            print(f"{ID} is not unique. terminate heuristics solver for case {case}")
            return

        """
        implement heuristics solver solver here
        res should contain in itself some datastructure, maybe a dict as well, that stores the following:
        - solve time
        - number of operations
        - number of explored nodes
        - number of backtracks
        - memory usage (tentative)
        """

        print(f"heuristics solve case {case}, ID {ID}")
        res = f"results for case {case} ID {ID} heuristics"
        self.__addExpRes(ID, res)

# main func
if __name__==__name__:
    s = SudokuWorld()
    #
    # s.bruteForceSolve(1, "1")
    # s.heuristicsSolve(2, "2")
    # s.heuristicsSolve(2, "67") # repeat
    #
    # s.displayExpRes(1)
    # s.displayExpRes(2)
    # s.displayExpRes(3)
    #
    # print(s.sMap)

    df = pd.read_csv("data.csv")

    print(df.to_string())
