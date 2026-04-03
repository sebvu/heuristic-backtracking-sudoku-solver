import time
import tracemalloc
import pandas as pd

from data_visualization import (
    DEFAULT_CASES,
    DEFAULT_FIGURES_DIR,
    DEFAULT_SUMMARY_PATH,
    write_all_outputs,
)
from dataCSV import DEFAULT_EXP_DATA_CSV_PATH, write_expdata_csv
from world import SudokuWorld
from solver import SudokuSolver
from constants import MAX_RUNS_PER_ALGO, RANDOM_STATE, MAX_EXP_TIME_IN_SECS


def main():
    world = SudokuWorld()
    solver = SudokuSolver(world)

    world.clearExpData() # ensure the dict is set correctly

    df = pd.read_csv("data/test.csv", usecols=["question", "answer"])
    
    # Selects 10 random samples from dataset, random_state makes it reproducible
    sample_df = df.sample(n=MAX_RUNS_PER_ALGO, random_state=RANDOM_STATE)
    print(f"Per-run timeout: {MAX_EXP_TIME_IN_SECS} seconds")

    print("Uninformed Solve: ")
    # test data for uninformed solve

    i = 1
    for question, answer in zip(sample_df["question"], sample_df["answer"]):
        print("      Running Uninformed Solve " + str(i))
        solver.uninformedSolve(str(question), str(answer))
        i += 1

    print("\nHeuristic Solve: ")
    # test data for heuristics solve
    i = 1;
    for question, answer in zip(sample_df["question"], sample_df["answer"]):
        print("      Running Heuristic Solve " + str(i))
        solver.heuristicsSolve(str(question), str(answer))
        i += 1
        
    print("\n")

    text, paths, summary_file = write_all_outputs(
        world,
        out_dir=DEFAULT_FIGURES_DIR,
        cases=DEFAULT_CASES,
        summary_path=DEFAULT_SUMMARY_PATH,
    )
    exp_data_csv = write_expdata_csv(world, path=DEFAULT_EXP_DATA_CSV_PATH)
    print(text)
    print(f"Wrote {summary_file}")
    print(f"Wrote {exp_data_csv}")
    for path in paths:
        print(f"Wrote {path}")

# main func
if __name__=="__main__":
    main()
