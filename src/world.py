import sys
from typing import Any, Dict, List

import pandas as pd

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
        # Per-solve metrics (reset at start of each solve; solvers should increment as they search)
        self.nodes_explored = 0
        self.backtracks = 0
        self.solve_time = 0.0
        self.solve_timed_out = False
        self.expData = { "isHeuristic": [],
                        "solveTimeSecs": [],
                        "numOfOperations": [],
                        "numOfBacktraces": [],
                        "peakMemUsage": [],
                        "numOfNodesExplored": [],
                        "timedOut": [] }

    # Add new res list to expData
    def addExpData(self, res: List):
        keys = [
            "isHeuristic",
            "solveTimeSecs",
            "numOfOperations",
            "numOfBacktraces",
            "peakMemUsage",
            "numOfNodesExplored",
            "timedOut",
        ]
        bool_keys = {"isHeuristic", "timedOut"}

        if len(res) != len(keys):
            raise ValueError(f"Expected {len(keys)} values for res, got {len(res)}: {res}")

        for k, r in zip(keys, res):
            if k in bool_keys and type(r) is bool:
                self.expData[k].append(r)
            elif k not in bool_keys and (type(r) is int or type(r) is float):
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
        self.solve_timed_out = False
        self.expData = { "isHeuristic": [],
                        "solveTimeSecs": [],
                        "numOfOperations": [],
                        "numOfBacktraces": [],
                        "peakMemUsage": [],
                        "numOfNodesExplored": [],
                        "timedOut": [] }

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
    
    def interpretExpData(self) -> Dict[str, Any]:
        """
        only use self.expData

        must interpret the following for both HEURISTICS and UNINFORMED functions SEPERATELY
        - worst, best, average solve time
        - worst, best, avg # of ops
        - worst, best, avg # of nodes explored
        - worst, best, avg # of backtraces
        - worst, best, avg mem usage

        compare the BOTH
        - how much % faster
        - how much % decreased operation usage
        - how much % decreased nodes explored
        - how much % # of backtraces decreased
        - how much % of memory efficiency

        Returns:
            dict with keys:
            - "uninformed", "heuristic": each maps metric name -> {"min","max","mean"} (None if no rows)
            - "comparison_pct": metric -> float percent (uninformed mean as baseline); positive means
              heuristic is lower/faster on that metric. None if baseline missing or zero.
            - "n_uninformed", "n_heuristic": row counts
        Heuristic vs uninformed % are meaningful only once the heuristic solver populates data.
        """
        keys = list(self.expData.keys())
        lengths = {k: len(self.expData[k]) for k in keys}
        if len(set(lengths.values())) > 1:
            raise ValueError(f"expData columns have unequal lengths: {lengths}")

        # return empty stats if there is no valid expdata
        n = lengths[keys[0]]
        if n == 0:
            metrics = [
                "solveTimeSecs",
                "numOfOperations",
                "numOfBacktraces",
                "peakMemUsage",
                "numOfNodesExplored",
            ]
            empty_stats = {m: {"min": None, "max": None, "mean": None} for m in metrics}
            return {
                "uninformed": empty_stats,
                "heuristic": empty_stats,
                "comparison_pct": {m: None for m in metrics},
                "n_uninformed": 0,
                "n_heuristic": 0,
                "n_uninformed_completed": 0,
                "n_heuristic_completed": 0,
                "total_uninformed_solve_time": 0,
                "total_heuristic_solve_time": 0,
                "timeout_counts": {"uninformed": 0, "heuristic": 0},
            }

        df = pd.DataFrame(self.expData)
        if "timedOut" not in df.columns:
            df["timedOut"] = False
        df["timedOut"] = df["timedOut"].astype(bool)
        metrics = [
            "solveTimeSecs",
            "numOfOperations",
            "numOfBacktraces",
            "peakMemUsage",
            "numOfNodesExplored",
        ]

        # per metric, solve for min, max and mean if applicable
        def stats_for(sub: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
            out: Dict[str, Dict[str, Any]] = {}
            for m in metrics:
                if sub.empty:
                    out[m] = {"min": None, "max": None, "mean": None}
                else:
                    out[m] = {
                        "min": float(sub[m].min()),
                        "max": float(sub[m].max()),
                        "mean": float(sub[m].mean()),
                    }
            return out

        df_u = df.loc[~df["isHeuristic"]]
        df_h = df.loc[df["isHeuristic"]]
        timeout_counts = {
            "uninformed": int(df_u["timedOut"].sum()),
            "heuristic": int(df_h["timedOut"].sum()),
        }
        df_u_completed = df_u.loc[~df_u["timedOut"]]
        df_h_completed = df_h.loc[~df_h["timedOut"]]

        uninformed = stats_for(df_u_completed)
        heuristic = stats_for(df_h_completed)

        # actual comparison of both means
        # calc pct of how much heuristic mean is better than uninformed mean
        comparison_pct: Dict[str, Any] = {}
        for m in metrics:
            u_mean = uninformed[m]["mean"]
            h_mean = heuristic[m]["mean"]
            if u_mean is None or h_mean is None or u_mean == 0:
                comparison_pct[m] = None
            else:
                comparison_pct[m] = 100.0 * (u_mean - h_mean) / u_mean

        return {
            "uninformed": uninformed,
            "heuristic": heuristic,
            "comparison_pct": comparison_pct,
            "n_uninformed": int(len(df_u)),
            "n_heuristic": int(len(df_h)),
            "n_uninformed_completed": int(len(df_u_completed)),
            "n_heuristic_completed": int(len(df_h_completed)),
            "total_uninformed_solve_time": round(sum(df_u_completed["solveTimeSecs"]), 2),
            "total_heuristic_solve_time": round(sum(df_h_completed["solveTimeSecs"]), 2),
            "timeout_counts": timeout_counts,
        }
