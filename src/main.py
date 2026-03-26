import time
import tracemalloc
import pandas as pd

from data_visualization import (
    DEFAULT_CASES,
    DEFAULT_FIGURES_DIR,
    DEFAULT_SUMMARY_PATH,
    write_all_outputs,
)
from world import SudokuWorld
from solver import SudokuSolver
from constants import MAX_EXP_TIME_IN_SECS

def main():
    world = SudokuWorld()
    solver = SudokuSolver(world)

    world.clearExpData() # ensure the dict is set correctly

    df = pd.read_csv("data/test.csv", usecols=["question", "answer"])

    tracemalloc.start() # track memory alloc for function

    # test data for uninformed solve
    start = time.monotonic()
    for question, answer in zip(df["question"], df["answer"]):
        if time.monotonic() - start < MAX_EXP_TIME_IN_SECS:
            tracemalloc.reset_peak()
            solver.uninformedSolve(str(question), str(answer))

    # test data for heuristics solve
    start = time.monotonic()
    for question, answer in zip(df["question"], df["answer"]):
        if time.monotonic() - start < MAX_EXP_TIME_IN_SECS:
            tracemalloc.reset_peak()
            solver.heuristicsSolve(str(question), str(answer))

    tracemalloc.stop() # ensure tracemalloc is finished

    text, paths, summary_file = write_all_outputs(
        world,
        out_dir=DEFAULT_FIGURES_DIR,
        cases=DEFAULT_CASES,
        summary_path=DEFAULT_SUMMARY_PATH,
    )
    print(text)
    print(f"Wrote {summary_file}")
    for path in paths:
        print(f"Wrote {path}")

# main func
if __name__=="__main__":
    main()
