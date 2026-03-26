# Data interpretation and visualization (course submission notes)

## What `interpretExpData` returns

A single `dict` (see `SudokuWorld.interpretExpData` in `src/world.py`):

| Key | Meaning |
|-----|---------|
| `uninformed` | Per-metric stats for rows where `isHeuristic` is false: each of `solveTimeSecs`, `numOfOperations`, `numOfBacktraces`, `peakMemUsage` maps to `min`, `max`, `mean` (or all `None` if no rows). |
| `heuristic` | Same structure for heuristic rows. |
| `comparison_pct` | Per metric: percent vs **uninformed mean** as baseline: `100 * (u_mean - h_mean) / u_mean`. Positive means heuristic mean is lower on that metric. `None` if not computable. |
| `n_uninformed`, `n_heuristic` | Row counts in each bucket. |

## What gets printed

`format_interpretation_text` (in `src/data_visualization.py`) turns that dict into a human-readable block: run counts, min/max/mean per side, then four comparison lines (or `N/A`).

## What gets written to disk

`save_interpretation_figures` writes PNGs under `figures/` (repo root by default):

- `interpret_solveTimeSecs.png`, `interpret_numOfOperations.png`, `interpret_numOfBacktraces.png`, `interpret_peakMemUsage.png` — bar charts of **mean** uninformed vs heuristic.
- `interpret_comparison_pct.png` — horizontal bar chart of the `%` values.

## How to reproduce (no full dataset required)

From repo root, with dependencies installed:

```powershell
$env:PYTHONPATH="src"
python -m data_visualization --demo
```

Or with GNU Make: `make viz-demo`

A sample console capture is in `docs/interpret_demo_console.txt`.

## Caveat for reports

Meaningful **heuristic vs uninformed** comparisons require real work in `heuristicsSolve` in `src/solver.py`. Until that is implemented, prefer the `--demo` output for slides, or label full `python -m main` runs as provisional.

## Git wrap-up (agent run)

- Branch `samuel-data-analysis` was pushed to `origin` after sync with `origin/main` (no extra merge was needed: branch already contained `origin/main`).
