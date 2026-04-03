# COSC4368 Group Project

**Topic:** Uninformed and Heuristic Backtracking Sudoku Solver

## Members
- Jester Santos
- Zachary Tassin
- Mason Caldwell
- Mazin Safer
- Samuel Sabu
- Joel Saji

## Project Description

This is a group project for COSC4368, in which the mission is to show obvious performance boosts on different metrics i.e. solve time, # of operations, backtraces, memory usage.. between an uninformed approach and a heuristics approach to a sudoku world.

There are 423k sudoku examples used in a data.csv file, provided from [sapientinc/sudoku-extreme](https://huggingface.co/datasets/sapientinc/sudoku-extreme).

## How to Run

This project uses a provided `Makefile` to simplify execution. It automatically handles OS differences and sets `PYTHONPATH=src` so modules run correctly.

### Setup

```bash
make install
```

Installs the Python packages listed in `requirements.txt`.

### Make Commands

```bash
make run
```

Runs the main experiment pipeline in `src/main.py`. This samples puzzles, runs both solvers, and writes the summary and figures output.

```bash
make benchmark
```

Runs the benchmark module in `src/benchmark.py` for a solver comparison workflow.

```bash
make viz-demo
```

Runs the visualization demo in `src/data_visualization.py --demo`. This uses synthetic `expData` to test the interpretation and plotting code without running the full solver pipeline.

```bash
make animation
```

Runs the animation script in `src/solver_animation.py` to generate a solver comparison animation.

```bash
make install
```

Installs or updates the project dependencies from `requirements.txt`.

### Project Settings

Located in `src/constants.py` there are three configuration variables that you can use.

| Config Variable | Default Value (int) | Description |
| --------------- | --------------- | --------------- |
| MAX_EXP_TIME_IN_SECS | 150 | Max amount of allocated time for each test case |
| MAX_RUNS_PER_ALGO | 30 | Total random test cases select for run |
| RANDOM_STATE | 5 | Seed number to select the random test cases |

## Analysis of Results

In figures there is a wide set of graphs that will be generated after running the program once with whatever settings. It will reflect the following metrics;

```
- dist_numOfBacktraces (box chart)
- dist_numOfNodesExplored (box chart)
- dist_numOfOperations (box chart)
- dist_peakMemUsage (box chart)
- dist_solveTimeSecs (box chart)
- exp_data.csv (csv file of raw data from experiments)
- interpret_comparison_pct (bar chart)
- interpret_numOfBacktraces (column chart)
- interpret_numOfNodesExplored (column chart)
- interpret_numOfOperations (column chart)
- interpret_numOfOperations (column chart)
- interpret_peakMemUsage (column chart)
- interpret_solveTimeSecs (column chart)
- mean_nodes_explored (column chart) *(faulty chart)*
- mean_operations (column chart)
- mean_solve_time (column chart)
- summary.txt (A numerical summary between heuristics and uninformed)
- trend_cummean_numOfBacktraces (line graph)
- trend_cummean_numOfNodesExplored (line graph)
- trend_cummean_numOfOperations (line graph)
- trend_cummean_peakMemUsage (line graph)
- trend_cummean_solveTimeSeconds (line graph)
- trend_pct_improvement_numOfBacktraces (line graph)
- trend_pct_improvement_numOfNodesExplored (line graph)
- trend_pct_improvement_numOfOperations (line graph)
- trend_pct_improvement_peakMemUsage (line graph)
- trend_pct_improvement_solveTimeSecs (line graph)
```


## How do you contribute?

To the few members on this project.. you need to install **git lfs** locally **on your computer** (THIS IS NOT THE SAME AS THE `git lfs install` COMMAND!). This project uses git lfs to store the large test.csv file on this repository.

```bash
git lfs install
git clone <repo>
cd <repo>
git lfs pull
```

You must also ensure you have all the requirements.

```bash
make install
```

then you can `make run`.

> [!NOTE]
> You most likely will encounter an issue where 'the environment is externally managed.' The best approach is to create a python venv.

```bash
cd <repo>
python3 -m venv .venv
source .venv/bin/activate
```

Once you have done this, then you should be able to run `make install` then `make run`.

Every time you access the project directory through a new terminal instance, **you have to do `source .venv/bin/activate`**
