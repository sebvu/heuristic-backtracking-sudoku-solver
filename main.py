import sys
import math
from typing import List
# from tkinter import *
import pandas as pd
import time
import tracemalloc

"""
TERMINOLOGY:
    cell: a 3x3 grid
    sMap = the sudoku map
    expRes = dict to interpret experiment data
    terminalState: if sMap == current answer
"""

class SudokuWorld:
    def __init__(self):
        self.X_COLS = 9
        self.Y_ROWS = 9
        self.sMap = [[0] * self.X_COLS] * self.Y_ROWS
        self.expData = { "isHeuristic": [],
                        "solveTimeSecs": [],
                        "numOfOperations": [],
                        "numOfBacktraces": [],
                        "peakMemUsage": [] }

    # Add new res list to expData
    def __addExpData(self, res: List):
        for k, z in zip(self.expData.keys(), range(5)):
            if (type(z) is bool and z == 0) or (type(z) is int):
                self.expData[k].append(z)
            else:
                raise TypeError("Faulty type detected for res")

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

    """
    NOTE TO CONTRIBUTORS:
    
    below is the section yall should mainly be focusing on, i.e. the uninformed function and heuristics function

    please if you got questions ask away yallsies
    """

    # uninformed function solve experiment
    def uninformedSolve(self, q, a):
        sTime = time.monotonic()
        numOfOps = 0
        numOfBtraces = 0
        
        if q != a: # terminal state checker
            """
            implement uninformed function solver here
            do not 'interpret' results, just fill in new entries for each of these (MUST FILL FOR ALL OF THEM)
            self.expRes = { "isHeuristic": [bool],
                            "solveTimeSecs": [int],
                            "numOfOperations": [int],
                            "numOfBacktraces": [int],
                            "peakMemUsage": [int] }
            """
            print("do something")

        _, peak, = tracemalloc.get_traced_memory()

        peakInMB = peak / 1024 / 1024

        """
        vvv make sure numOfOps and numOfBtraces are counted vvv
        """
        res = [False, time.monotonic() - sTime, numOfOps, numOfBtraces, peakInMB]
        self.__addExpData(res)


    # Heuristics solve experiment
    def heuristicsSolve(self, q, a):
        sTime = time.monotonic()
        numOfOps = 0
        numOfBtraces = 0

        if q != a: # terminal state checker
            """
            implement heuristics solver here
            do not 'interpret' results, just fill in new entries for each of these (MUST FILL FOR ALL OF THEM)
            self.expRes = { "isHeuristic": [bool],
                            "solveTimeSecs": [int],
                            "numOfOperations": [int],
                            "numOfBacktraces": [int],
                            "peakMemUsage": [int] }
            """
            print("do something")

        _, peak, = tracemalloc.get_traced_memory()

        peakInMB = peak / 1024 / 1024

        """
        vvv make sure numOfOps and numOfBtraces are counted vvv
        """
        res = [True, time.monotonic() - sTime, numOfOps, numOfBtraces, peakInMB]
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

def main():
    s = SudokuWorld()

    s.clearExpData() # ensure the dict is set correctly

    # max amount of allocated time for each experiment
    MAX_EXP_TIME_IN_SECS = 30

    print(s.sMap)

    df = pd.read_csv("cases/test.csv", usecols=["question", "answer"])

    tracemalloc.start() # track memory alloc for function

    # test data for uninformed solve
    start = time.monotonic()
    for question, answer in zip(df["question"], df["answer"]):
        if time.monotonic() - start < MAX_EXP_TIME_IN_SECS:
            tracemalloc.reset_peak()
            s.uninformedSolve(question, answer)

    # test data for heuristics solve
    start = time.monotonic()
    for question, answer in zip(df["question"], df["answer"]):
        if time.monotonic() - start < MAX_EXP_TIME_IN_SECS:
            tracemalloc.reset_peak()
            s.heuristicsSolve(question, answer)

    tracemalloc.stop() # ensure tracemalloc is finished

# main func
if __name__=="__main__":
    main()
