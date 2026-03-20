import time
import tracemalloc
import pandas as pd

from sudoku.world import SudokuWorld
from sudoku.constants import MAX_EXP_TIME_IN_SECS

def main():
    s = SudokuWorld()

    s.clearExpData() # ensure the dict is set correctly

    print(s.sMap)

    df = pd.read_csv("data/test.csv", usecols=["question", "answer"])

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
