# Visualization QA Gap Report

Date: 2026-03-25

## Pass/Fail Matrix

| Check | Status | Evidence | Remediation |
|---|---|---|---|
| Required metrics present (time, operations, backtraces, memory) | PASS | `python -m main` and `python -m data_visualization --demo` both emit all four interpretation families plus comparison output | None |
| `%` comparison definition is consistent (`100 * (u - h) / u`) | PASS | Shared interpretation pipeline uses one formula for summary text and percent plots | None |
| Scientific notation removed from user-facing summary artifact | PASS | `figures/summary.txt` contains zero `e+` / `e-` matches | None |
| Scale policy: log only for operations/backtraces | PASS | Trend/distribution rendering keeps log scale to `numOfOperations` and `numOfBacktraces`; time/memory remain linear | None |
| Human-readable chart labels/ticks | PASS | Shared axis formatting applied across visualization outputs and benchmark figures | None |
| Demo run reliability | PASS | `python -m data_visualization --demo` completes and writes full artifact set | None |
| Benchmark run reliability | PASS | `python -m benchmark` completes and writes benchmark figures with readable axes | None |
| Main run reliability | PASS (with caveat) | `python -m main` completes and writes summary + all figure families | Keep caveat below in teammate-facing discussion |
| Docs clarity (`run` vs `benchmark` vs `viz-demo`) | PASS | README command matrix and interpretation notes are aligned with generated outputs | None |
| Artifact policy clarity (`figures/*.png` ignored) | PASS | `.gitignore` policy + docs note local regeneration behavior | None |

## Remaining Caveat (Non-blocking)

- Heuristic path still appears degenerate in current project state (`heuristicsSolve` behavior). This can produce flat/near-empty percent trends for real runs even when plotting logic is correct.
- Team-facing wording should state that visualization plumbing is validated and readable, while final comparative meaning depends on completed heuristic implementation.

## Suggested Team Response

- "I applied readability fixes and QA checks end-to-end: no scientific notation in summary artifacts, log scale only for operations/backtraces, linear for time/memory, and consistent labels across main/demo/benchmark outputs."
- "If a percent trend looks flat in real runs, that is currently from degenerate heuristic data, not a plotting bug; demo runs with non-degenerate synthetic values show expected non-flat behavior."
