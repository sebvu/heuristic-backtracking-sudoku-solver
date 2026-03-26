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
    
    # Init with world, and also initialize numOfOps and numOfBtraces to 0
    def __init__(self, world: SudokuWorld):
        self.world = world
        self.numOfOps = 0
        self.numOfBtraces = 0

    # Helper function to reset numOfOps and numOfBtraces to 0 before each solve
    def _resetMetrics(self):
        self.numOfOps = 0
        self.numOfBtraces = 0

    # Helper function to check if a number can be placed in a given position according to sudoku rules
    def _isValid(self, row, col, num):
        for x in range(self.world.X_COLS):
            if self.world.sMap[row][x] == num:
                return False

        for y in range(self.world.Y_ROWS):
            if self.world.sMap[y][col] == num:
                return False

        box_row = 3 * (row // 3)
        box_col = 3 * (col // 3)
        for y in range(box_row, box_row + 3):
            for x in range(box_col, box_col + 3):
                if self.world.sMap[y][x] == num:
                    return False

        return True

    # Helper function to find the next empty cell in the sudoku board, returns (row, col)
    # or None if no empty cells
    def _findNextEmpty(self):
        for y in range(self.world.Y_ROWS):
            for x in range(self.world.X_COLS):
                if self.world.sMap[y][x] == 0:
                    return (y, x)

        return None

    # Backtracking algorithm for uninformed solve
    def _backtrackUninformed(self):
        pos = self._findNextEmpty()
        if pos is None:
            return True

        row, col = pos

        for num in range(1, 10):
            self.numOfOps += 1
            if self._isValid(row, col, num):
                self.world.sMap[row][col] = num
                if self._backtrackUninformed():
                    return True

                self.world.sMap[row][col] = 0
                self.numOfBtraces += 1

        return False

    # Helper function to record experiment data into world.expData
    def _recordExperiment(self, isHeuristic, startTime, numOfOps, numOfBtraces):
        peak = tracemalloc.get_traced_memory()[1] if tracemalloc.is_tracing() else 0
        peakInMB = peak / 1024 / 1024
        res = [isHeuristic, time.monotonic() - startTime, numOfOps, numOfBtraces, peakInMB]
        self.world.addExpData(res)

    # uninformed function solve experiment
    def uninformedSolve(self, q, a):
        sTime = time.monotonic()
        self._resetMetrics()

        self.world.populateSudokuWorld(q)
            
        if not self.world.verifyTerminalReached(a):
            solved = self._backtrackUninformed()
            if not solved:
                print("uninformed solver could not solve the puzzle")

        self._recordExperiment(False, sTime, self.numOfOps, self.numOfBtraces)


    # Helper function to get the set of legal values for a given empty cell
    def _getLegalValues(self, row, col):
        used = set()
        for x in range(self.world.X_COLS):
            if self.world.sMap[row][x] != 0:
                used.add(self.world.sMap[row][x])
        for y in range(self.world.Y_ROWS):
            if self.world.sMap[y][col] != 0:
                used.add(self.world.sMap[y][col])
        box_row = 3 * (row // 3)
        box_col = 3 * (col // 3)
        for y in range(box_row, box_row + 3):
            for x in range(box_col, box_col + 3):
                if self.world.sMap[y][x] != 0:
                    used.add(self.world.sMap[y][x])
        return set(range(1, 10)) - used

    # MRV heuristic: find the empty cell with the fewest legal values remaining
    def _findNextEmptyMRV(self):
        min_count = 10
        best_pos = None
        for y in range(self.world.Y_ROWS):
            for x in range(self.world.X_COLS):
                if self.world.sMap[y][x] == 0:
                    count = len(self._getLegalValues(y, x))
                    if count == 0:
                        return (y, x)  # dead end — fail fast
                    if count < min_count:
                        min_count = count
                        best_pos = (y, x)
        return best_pos

    # LCV heuristic: count how many peer options a given value eliminates (lower = less constraining)
    def _countEliminations(self, row, col, num):
        peers = set()
        for x in range(self.world.X_COLS):
            if self.world.sMap[row][x] == 0 and x != col:
                peers.add((row, x))
        for y in range(self.world.Y_ROWS):
            if self.world.sMap[y][col] == 0 and y != row:
                peers.add((y, col))
        box_row = 3 * (row // 3)
        box_col = 3 * (col // 3)
        for y in range(box_row, box_row + 3):
            for x in range(box_col, box_col + 3):
                if self.world.sMap[y][x] == 0 and (y, x) != (row, col):
                    peers.add((y, x))
        return sum(1 for (pr, pc) in peers if num in self._getLegalValues(pr, pc))

    # Backtracking algorithm using MRV (cell selection) and LCV (value ordering)
    def _backtrackHeuristic(self):
        pos = self._findNextEmptyMRV()
        if pos is None:
            return True

        row, col = pos
        legal_values = self._getLegalValues(row, col)

        # LCV: try the value that eliminates the fewest peer options first
        ordered_values = sorted(legal_values, key=lambda num: self._countEliminations(row, col, num))

        for num in ordered_values:
            self.numOfOps += 1
            self.world.sMap[row][col] = num
            if self._backtrackHeuristic():
                return True
            self.world.sMap[row][col] = 0
            self.numOfBtraces += 1

        return False

    # Heuristics solve experiment
    def heuristicsSolve(self, q, a):
        sTime = time.monotonic()
        self._resetMetrics()

        self.world.populateSudokuWorld(q)

        if not self.world.verifyTerminalReached(a):
            solved = self._backtrackHeuristic()
            if not solved:
                print("heuristic solver could not solve the puzzle")

        self._recordExperiment(True, sTime, self.numOfOps, self.numOfBtraces)
