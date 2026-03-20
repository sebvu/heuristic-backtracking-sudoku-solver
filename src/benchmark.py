"""
Compare uninformed vs heuristic solve on one puzzle: N runs each, means, bar charts.

Run from repository root: make benchmark  (or: set PYTHONPATH=src && python -m benchmark)
"""
import argparse
import os
import statistics
import tracemalloc
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from world import SudokuWorld

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = REPO_ROOT / "data" / "test.csv"
FIGURES_DIR = REPO_ROOT / "figures"


def _trial(question: str, answer: str, *, heuristic: bool) -> dict[str, float]:
    world = SudokuWorld()
    tracemalloc.reset_peak()
    if heuristic:
        world.heuristicsSolve(str(question), str(answer))
    else:
        world.uninformedSolve(str(question), str(answer))
    _, peak = tracemalloc.get_traced_memory()
    return {
        "solve_time": float(world.solve_time),
        "nodes_explored": float(world.nodes_explored),
        "backtracks": float(world.backtracks),
        "peak_mb": peak / 1024 / 1024,
    }


def run_battery(
    question: str,
    answer: str,
    *,
    n_runs: int = 3,
) -> tuple[list[dict[str, float]], list[dict[str, float]]]:
    uninformed_rows: list[dict[str, float]] = []
    heuristic_rows: list[dict[str, float]] = []
    tracemalloc.start()
    try:
        for _ in range(n_runs):
            uninformed_rows.append(_trial(question, answer, heuristic=False))
        for _ in range(n_runs):
            heuristic_rows.append(_trial(question, answer, heuristic=True))
    finally:
        tracemalloc.stop()
    return uninformed_rows, heuristic_rows


def _mean(xs: list[float]) -> float:
    return float(statistics.mean(xs)) if xs else 0.0


def _stdev(xs: list[float]) -> float:
    return float(statistics.stdev(xs)) if len(xs) > 1 else 0.0


def summarize(
    uninformed_rows: list[dict[str, float]],
    heuristic_rows: list[dict[str, float]],
) -> dict[str, Any]:
    u_t = [r["solve_time"] for r in uninformed_rows]
    h_t = [r["solve_time"] for r in heuristic_rows]
    u_n = [r["nodes_explored"] for r in uninformed_rows]
    h_n = [r["nodes_explored"] for r in heuristic_rows]
    u_b = [r["backtracks"] for r in uninformed_rows]
    h_b = [r["backtracks"] for r in heuristic_rows]

    def pct_improvement(baseline: float, improved: float) -> float | None:
        if baseline == 0:
            return None
        return 100.0 * (baseline - improved) / baseline

    return {
        "uninformed": {
            "mean_time": _mean(u_t),
            "stdev_time": _stdev(u_t),
            "mean_nodes": _mean(u_n),
            "stdev_nodes": _stdev(u_n),
            "mean_backtracks": _mean(u_b),
        },
        "heuristic": {
            "mean_time": _mean(h_t),
            "stdev_time": _stdev(h_t),
            "mean_nodes": _mean(h_n),
            "stdev_nodes": _stdev(h_n),
            "mean_backtracks": _mean(h_b),
        },
        "pct_faster_time": pct_improvement(_mean(u_t), _mean(h_t)),
        "pct_fewer_nodes": pct_improvement(_mean(u_n), _mean(h_n)),
        "pct_fewer_backtracks": pct_improvement(_mean(u_b), _mean(h_b)),
    }


def plot_bars(
    summary: dict[str, Any],
    *,
    n_runs: int,
    out_dir: Path,
) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    labels = ["Uninformed", "Heuristic"]
    u = summary["uninformed"]
    h = summary["heuristic"]

    fig, ax = plt.subplots(figsize=(6, 4))
    times = [u["mean_time"], h["mean_time"]]
    ax.bar(labels, times, color=["#4c72b0", "#55a868"])
    ax.set_ylabel("Mean solve time (s)")
    ax.set_title(f"Solve time (mean of {n_runs} runs, same puzzle)")
    fig.tight_layout()
    p_time = out_dir / "mean_solve_time.png"
    fig.savefig(p_time, dpi=150, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    nodes = [u["mean_nodes"], h["mean_nodes"]]
    ax.bar(labels, nodes, color=["#4c72b0", "#55a868"])
    ax.set_ylabel("Mean nodes explored")
    ax.set_title(f"Search effort (mean of {n_runs} runs, same puzzle)")
    fig.tight_layout()
    p_nodes = out_dir / "mean_nodes_explored.png"
    fig.savefig(p_nodes, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return p_time, p_nodes


def load_puzzle(csv_path: Path, row_index: int) -> tuple[str, str]:
    df = pd.read_csv(csv_path, usecols=["question", "answer"])
    if row_index < 0 or row_index >= len(df):
        raise IndexError(f"row_index {row_index} out of range for {csv_path} (len={len(df)})")
    row = df.iloc[row_index]
    return str(row["question"]), str(row["answer"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark uninformed vs heuristic SudokuWorld solvers.")
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="Path to test CSV")
    parser.add_argument("--row", type=int, default=0, help="0-based row index in CSV")
    parser.add_argument("--runs", type=int, default=3, help="Runs per algorithm")
    parser.add_argument(
        "--figures-dir",
        type=Path,
        default=FIGURES_DIR,
        help="Directory for PNG outputs",
    )
    args = parser.parse_args()

    os.chdir(REPO_ROOT)
    q, a = load_puzzle(args.csv, args.row)
    print(f"Using row {args.row} from {args.csv} ({args.runs} runs per algorithm)")

    uninformed_rows, heuristic_rows = run_battery(q, a, n_runs=args.runs)
    summary = summarize(uninformed_rows, heuristic_rows)

    print("\nPer-run (uninformed):", uninformed_rows)
    print("Per-run (heuristic):", heuristic_rows)
    print("\nSummary:")
    print("  Uninformed - mean time:", summary["uninformed"]["mean_time"], "s")
    print("  Heuristic  - mean time:", summary["heuristic"]["mean_time"], "s")
    print("  Uninformed - mean nodes:", summary["uninformed"]["mean_nodes"])
    print("  Heuristic  - mean nodes:", summary["heuristic"]["mean_nodes"])
    if summary["pct_faster_time"] is not None:
        print(f"  Heuristic ~{summary['pct_faster_time']:.1f}% faster (time) vs uninformed mean")
    else:
        print("  Time % improvement: N/A (zero uninformed mean time)")
    if summary["pct_fewer_nodes"] is not None:
        print(f"  Heuristic ~{summary['pct_fewer_nodes']:.1f}% fewer nodes vs uninformed mean")
    else:
        print("  Nodes % improvement: N/A (zero uninformed mean nodes)")

    p_time, p_nodes = plot_bars(summary, n_runs=args.runs, out_dir=args.figures_dir)
    print(f"\nWrote {p_time}")
    print(f"Wrote {p_nodes}")


if __name__ == "__main__":
    main()
