# COSC4368 Group Project

**Topic:** Heuristic Backtracking Sudoku Solver

## Members
- Jester Santos
- Zachary Tassin
- Mazin Safer
- Samuel Sabu
- Joel Saji

## Project Description

This is a group project for COSC4368, in which the mission is to show obvious performance boosts on different metrics i.e. solve time, # of operations, backtraces, memory usage.. between an uninformed approach and a heuristics approach to a sudoku world.

There are 423k sudoku examples used in a data.csv file, provided from [sapientinc/sudoku-extreme](https://huggingface.co/datasets/sapientinc/sudoku-extreme).

## How do you run?

There is a provided Makefile to this project. It'll automatically detect the OS you're in, and run accordingly. If there are issues with it, please raise it!

Run the following. **ALWAYS CHECK WHAT A MAKEFILE IS EXECUTING ON YOUR COMPUTER.**

```shell
make install
make run
```

### Interpretation demo (figures only, no CSV run)

From the repo root, with `PYTHONPATH=src` set (see Makefile for how this project runs modules):

```shell
make viz-demo
```

On systems without `make`, use: `PYTHONPATH=src python -m data_visualization --demo`. This regenerates the summary printout and PNGs under `figures/`. See `docs/SUBMISSION_NOTES.md` for details.

**Note:** `figures/*.png` is gitignored—each developer generates plots locally.

| Command | Purpose | Main outputs under `figures/` |
|--------|---------|-------------------------------|
| `make run` | Full CSV experiment (time-capped) + interpretation | `interpret_*.png` |
| `make benchmark` | Same puzzle, N runs per solver (quick sanity check) | `mean_solve_time.png`, `mean_operations.png` |
| `make viz-demo` | Synthetic data only; tests interpret + plots | `interpret_*.png` |

`viz-demo` is not the main experiment. `benchmark` is not a rewrite of `make run`—it is a small, repeatable single-row comparison.

## How do you contribute?

To the few members on this project.. you need to install **git lfs** locally **on your computer** (THIS IS NOT THE SAME AS THE `git lfs install` COMMAND!). This project uses git lfs to store the large test.csv file on this repository.

```shell
git lfs install
git clone <repo>
cd <repo>
git lfs pull
```

You must also ensure you have all the requirements.

```shell
make install
```

then you can `make run`.

> [!NOTE]
> You most likely will encounter an issue where 'the environment is externally managed.' The best approach is to create a python venv.

```
cd <repo>
python -m venv .venv
source ./venv/bin/activate
```

Once you have done this, then you should be able to run `make install` then `make run`.

Every time you access the project directory through a new terminal instance, **you have to do source ./venv/bin/activate**
