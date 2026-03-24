import sys
from typing import List

"""
TERMINOLOGY:
    cell: a 3x3 grid
    sMap = the sudoku map
    expRes = dict to interpret experiment data
    terminalState: if sMap == current answer

NOTES:
    to edit a spot, it's self.sMap[Y][X]
    ^ it's weird ik lol, but the Y must go first before the X.

FUNCTIONS:
    addExpData(res: List)
    - takes in a List (has to be formatted a certain way) and adds to expData

    verifyPos(X_POS, Y_POS, funcName) -> bool:
    - helper function for identifying if an X pos and Y pos is out of bounds, and the function it was called from

    verifyGameFromPos(X_POS, Y_POS) -> bool:
    - from the X, Y position, will check if the cell, X and Y axes are valid. good for checking when you change a value in a certain position

    populateSudokuWorld(q)
    - overwrites sudoku board with new initial state, ENSURE IT IS ALL INTS

    verifyTerminalReached(self, a) -> bool:
    - verify if terminal has been reached by comparing a to sMap

    interpretExpData()
    - will interpret the data in expData as per requested data
"""

class SudokuWorld:
    def __init__(self):
        self.X_COLS = 9
        self.Y_ROWS = 9
        self.sMap = [[0] * self.X_COLS for _ in range(self.Y_ROWS)]
        self.expData = { "isHeuristic": [],
                        "solveTimeSecs": [],
                        "numOfOperations": [],
                        "numOfBacktraces": [],
                        "peakMemUsage": [] }

    # Add new res list to expData
    def addExpData(self, res: List):
        for k, z, r in zip(self.expData.keys(), range(5), res):
            if (type(r) is bool and z == 0) or (type(r) is int or type(r) is float):
                self.expData[k].append(r)
            else:
                raise TypeError(f"Faulty type detected for res {res}")

    # verify if position about to be accessed is even valid, if it isn't terminate program
    def verifyPos(self, X_POS, Y_POS, funcName) -> bool:
        if X_POS < 0 or X_POS >= self.X_COLS or Y_POS < 0 or Y_POS >= self.Y_ROWS:
            sys.exit(f"value X or Y: ({X_POS},{Y_POS}) beyond boundaries, function call: {funcName}")
        else:
            return True

    # verify, from X,Y position, if the board is valid.
    def verifyGameFromPos(self, X_POS, Y_POS) -> bool:
        self.verifyPos(X_POS, Y_POS, "verifyGameFromPos")

        # get the num cell multiplier to apply to the X, Y position
        x_cell = (X_POS // 3) * 3
        y_cell = (Y_POS // 3) * 3

        # verify in cell all numbers are unique
        s = set()
        for y in range(3):
            for x in range(3):
                valAtPos = self.sMap[y_cell + y][x_cell + x]
                if valAtPos != 0:
                    if valAtPos not in s:
                        s.add(valAtPos)
                    else:
                        print(f"[verifyGameFromPos] rep. found in grid xcell: {x_cell}, ycell: {y_cell}")
                        print(self.sMap)
                        return False # repeat found
        
        # verify x col is unique
        s.clear()
        for x in range(self.X_COLS):
            valAtPos = self.sMap[Y_POS][x]
            if valAtPos != 0:
                if valAtPos not in s:
                    s.add(valAtPos)
                else:
                    print(f"[verifyGameFromPos] rep. found in X row, val: {valAtPos} at X: {x}, Y: {Y_POS}")
                    print(self.sMap)
                    return False # repeat found

        # verify y row is unique
        s.clear()
        for y in range(self.Y_ROWS):
            valAtPos = self.sMap[y][X_POS]
            if valAtPos != 0:
                if valAtPos not in s:
                    s.add(valAtPos)
                else:
                    print(f"[verifyGameFromPos] rep. found in Y row, val: {valAtPos} at X: {X_POS}, Y: {y}")
                    print(self.sMap)
                    return False # repeat found

        return True # all checks passed

    # ensure expData is set properly
    def clearExpData(self):
        self.expData = { "isHeuristic": [],
                        "solveTimeSecs": [],
                        "numOfOperations": [],
                        "numOfBacktraces": [],
                        "peakMemUsage": [] }

    # overwrite current sMap with new q, ENSURE IT IS ALL INTS
    def populateSudokuWorld(self, q):
        for y in range(self.Y_ROWS):
            for x in range(self.X_COLS):
                val = q[(y * self.Y_ROWS) + x]
                self.sMap[y][x] = 0 if val == "." else int(val)

    # verify if terminal has been reached
    def verifyTerminalReached(self, a) -> bool:
        for y in range(self.Y_ROWS):
            for x in range(self.X_COLS):
                val = a[(y * self.Y_ROWS) + x]
                
                if val == ".":
                    expectedVal = 0
                else:
                    expectedVal = int(val)
                    
                if self.sMap[y][x] != expectedVal:
                   return False 
        return True

    """
    NOTE TO CONTRIBUTORS:
    
    below is the section yall should mainly be focusing on, i.e. the uninformed function and heuristics function

    please if you got questions ask away yallsies
    """
    
    # Moved the solver functions to its own class in the solver.py file -JS
    
    def interpretExpData(self): # -> determine return type
        """
        only use self.expData
        
        must interpret the following for both HEURISTICS and UNINFORMED functions SEPERATELY
        - worst, best, average solve time
        - worst, best, avg # of ops
        - worst, best, avg # of backtraces
        - worst, best, avg mem usage

        compare the BOTH
        - how much % faster
        - how much % decreased operation usage
        - how much % # of backtraces decreased
        - how much % of memory efficiency
        """
        
        return # will return a dataframe, or some list idk up to you
