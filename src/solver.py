import time
import tracemalloc
from world import SudokuWorld


"""
Class SudokuSolver
    - Class to take in a sudoku puzzle in the class format and perform solving
    algorithms on the puzzles
    - It will record data metrics and store the information for interpretation later
    
Functions:
    uninformedSolve(q, a)
    - takes in q (the initial sudoku world) and a (the terminal state) and solves 
    using an uninformed algorithm, will put data, res, in expData

    heuristicsSolve(q, a)
    - takes in q (the initial sudoku world) and a (the terminal state) and solves 
    using an heuristics algorithm, will put data, res, in expData
"""

class SudokuSolver:
    def __init__(self, world: SudokuWorld):
        self.world = world

    def _recordExperiment(self, isHeuristic, startTime, numOfOps, numOfBtraces):
        peak = tracemalloc.get_traced_memory()[1] if tracemalloc.is_tracing() else 0
        peakInMB = peak / 1024 / 1024
        res = [isHeuristic, time.monotonic() - startTime, numOfOps, numOfBtraces, peakInMB]
        self.world.addExpData(res)

    # uninformed function solve experiment
    def uninformedSolve(self, q, a):
        sTime = time.monotonic()
        numOfOps = 0
        numOfBtraces = 0

        self.world.populateSudokuWorld(q)
        
        if not self.world.verifyTerminalReached(a): # terminal state checker
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

        self._recordExperiment(False, sTime, numOfOps, numOfBtraces)


    # Heuristics solve experiment
    def heuristicsSolve(self, q, a):
        sTime = time.monotonic()
        numOfOps = 0
        numOfBtraces = 0

        self.world.populateSudokuWorld(q)
        
        if not self.world.verifyTerminalReached(a): # terminal state checker
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

        self._recordExperiment(True, sTime, numOfOps, numOfBtraces)


SudokuSolve = SudokuSolver
