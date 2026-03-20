import sys
import math
from typing import List
import time
import tracemalloc

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
    __addExpData(res: List)
    - takes in a List (has to be formatted a certain way) and adds to expData

    __verifyPos(X_POS, Y_POS, funcName) -> bool:
    - helper function for identifying if an X pos and Y pos is out of bounds, and the function it was called from

    __verifyGameFromPos(X_POS, Y_POS) -> bool:
    - from the X, Y position, will check if the cell, X and Y axes are valid. good for checking when you change a value in a certain position

    __populateSudokuWorld(q)
    - overwrites sudoku board with new initial state, ENSURE IT IS ALL INTS

    __verifyTerminalReached(self, a) -> bool:
    - verify if terminal has been reached by comparing a to sMap

    uninformedSolve(q, a)
    - takes in q (the initial sudoku world) and a (the terminal state) and solves using an uninformed algorithm, will put data, res, in expData

    heuristicsSolve(q, a)
    - takes in q (the initial sudoku world) and a (the terminal state) and solves using an heuristics algorithm, will put data, res, in expData

    interpretExpData()
    - will interpret the data in expData as per requested data

"""

class SudokuWorld:
    def __init__(self):
        self.X_COLS = 9
        self.Y_ROWS = 9
        self.sMap = [[0] * self.X_COLS for _ in range(self.Y_ROWS)]
        # Per-solve metrics (reset at start of each solve; solvers should increment as they search)
        self.nodes_explored = 0
        self.backtracks = 0
        self.solve_time = 0.0
        self.expData = { "isHeuristic": [],
                        "solveTimeSecs": [],
                        "numOfOperations": [],
                        "numOfBacktraces": [],
                        "peakMemUsage": [] }

    # Add new res list to expData
    def __addExpData(self, res: List):
        for k, z, r in zip(self.expData.keys(), range(5), res):
            if (type(r) is bool and z == 0) or (type(r) is int or type(r) is float):
                self.expData[k].append(r)
            else:
                raise TypeError(f"Faulty type detected for res {res}")

    # verify if position about to be accessed is even valid, if it isn't terminate program
    def __verifyPos(self, X_POS, Y_POS, funcName) -> bool:
        if X_POS < 0 or X_POS >= self.X_COLS or Y_POS < 0 or Y_POS >= self.Y_ROWS:
            sys.exit(f"value X or Y: ({X_POS},{Y_POS}) beyond boundaries, function call: {funcName}")
        else:
            return True

    # verify, from X,Y position, if the board is valid.
    def __verifyGameFromPos(self, X_POS, Y_POS) -> bool:
        # get the num cell multiplier to apply to the X, Y position
        x_cell, y_cell = math.floor(X_POS / 3) + 1, math.floor(Y_POS / 3) + 1

        # verify in cell all numbers are unique
        s = set()
        for y in range(3):
            for x in range(3):
                valAtPos = self.sMap[(y_cell * 3) + y][(x_cell * 3) + x]
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
            valAtPos = self.sMap[Y_POS][x]
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
            valAtPos = self.sMap[y][X_POS]
            if valAtPos != 0:
                if valAtPos not in s:
                    s.add(valAtPos)
                else:
                    print(f"[verifyGameFromPos] rep. found in Y row, val: {valAtPos} at X: {X_POS}, Y: {y}")
                    print(self.sMap)
                    return False # repeat found
            continue

        return True # all checks passed

    # ensure expData is set properly
    def clearExpData(self):
        self.expData = { "isHeuristic": [],
                        "solveTimeSecs": [],
                        "numOfOperations": [],
                        "numOfBacktraces": [],
                        "peakMemUsage": [] }

    # overwrite current sMap with new q, ENSURE IT IS ALL INTS
    def __populateSudokuWorld(self, q):
        for y in range(self.Y_ROWS):
            for x in range(self.X_COLS):
                val = q[(y * self.Y_ROWS) + x]
                self.sMap[y][x] = 0 if val == "." else int(val)

    # verify if terminal has been reached
    def __verifyTerminalReached(self, a) -> bool:
        for y in range(self.Y_ROWS):
            for x in range(self.X_COLS):
                val = a[(y * self.Y_ROWS) + x]
                if self.sMap[y][x] != val:
                   return False 
        return True

    """
    NOTE TO CONTRIBUTORS:
    
    below is the section yall should mainly be focusing on, i.e. the uninformed function and heuristics function

    please if you got questions ask away yallsies
    """

    # uninformed function solve experiment
    def uninformedSolve(self, q, a):
        self.nodes_explored = 0
        self.backtracks = 0
        self.solve_time = 0.0
        sTime = time.perf_counter()

        self.__populateSudokuWorld(q)
        
        if not self.__verifyTerminalReached(a): # terminal state checker
            """
            implement uninformed function solver here
            do not 'interpret' results, just fill in new entries for each of these (MUST FILL FOR ALL OF THEM)
            self.expRes = { "isHeuristic": [bool],
                            "solveTimeSecs": [int],
                            "numOfOperations": [int],
                            "numOfBacktraces": [int],
                            "peakMemUsage": [int] }

            Increment self.nodes_explored on each attempted cell assignment.
            Increment self.backtracks each time the search undoes a placement.
            """
            print("do something")

        _, peak = tracemalloc.get_traced_memory()

        peakInMB = peak / 1024 / 1024

        self.solve_time = time.perf_counter() - sTime
        res = [False, self.solve_time, self.nodes_explored, self.backtracks, peakInMB]
        self.__addExpData(res)


    # Heuristics solve experiment
    def heuristicsSolve(self, q, a):
        self.nodes_explored = 0
        self.backtracks = 0
        self.solve_time = 0.0
        sTime = time.perf_counter()

        self.__populateSudokuWorld(q)
        
        if not self.__verifyTerminalReached(a): # terminal state checker
            """
            implement heuristics solver here
            do not 'interpret' results, just fill in new entries for each of these (MUST FILL FOR ALL OF THEM)
            self.expRes = { "isHeuristic": [bool],
                            "solveTimeSecs": [int],
                            "numOfOperations": [int],
                            "numOfBacktraces": [int],
                            "peakMemUsage": [int] }

            Increment self.nodes_explored on each attempted cell assignment.
            Increment self.backtracks each time the search undoes a placement.
            """
            print("do something")

        _, peak = tracemalloc.get_traced_memory()

        peakInMB = peak / 1024 / 1024

        self.solve_time = time.perf_counter() - sTime
        res = [True, self.solve_time, self.nodes_explored, self.backtracks, peakInMB]
        self.__addExpData(res)

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
