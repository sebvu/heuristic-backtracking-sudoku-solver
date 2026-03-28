"""
Compare uninformed vs heuristic solve on one puzzle: N runs each, means, bar charts.

Run from repository root: make benchmark  (or: set PYTHONPATH=src && python -m benchmark)
"""
import argparse
import os
import statistics
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import ticker

from solver import SudokuSolver
from world import SudokuWorld

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = REPO_ROOT / "data" / "test.csv"
FIGURES_DIR = REPO_ROOT / "figures"
def _plain_axis_formatter(decimals: int = 3) -> ticker.FuncFormatter:
    def _fmt(x: float, _pos: int) -> str:
        if abs(x) >= 1000:
            if abs(x - round(x)) < 1e-12:
                return f"{int(round(x)):,}"
            return f"{x:,.1f}"
        s = f"{x:.{decimals}f}".rstrip("0").rstrip(".")
        return "0" if s in {"", "-0"} else s

    return ticker.FuncFormatter(_fmt)


def _last_run_metrics(world: SudokuWorld) -> dict[str, float]:
    """Read metrics from the last row appended to expData by SudokuSolver."""
    ed = world.expData
    if not ed["solveTimeSecs"]:
        raise RuntimeError("expData has no rows after solve")
    i = len(ed["solveTimeSecs"]) - 1
    return {
        "solve_time": float(ed["solveTimeSecs"][i]),
        "operations": float(ed["numOfOperations"][i]),
        "backtracks": float(ed["numOfBacktraces"][i]),
        "peak_mb": float(ed["peakMemUsage"][i]),
        "nodes_explored": float(ed["numOfNodesExplored"][i]),
    }


def _trial(question: str, answer: str, *, heuristic: bool) -> dict[str, float]:
    world = SudokuWorld()
    solver = SudokuSolver(world)
    world.clearExpData()
    if heuristic:
        solver.heuristicsSolve(str(question), str(answer))
    else:
        solver.uninformedSolve(str(question), str(answer))
    return _last_run_metrics(world)


def run_battery(
    question: str,
    answer: str,
    *,
    n_runs: int = 3,
) -> tuple[list[dict[str, float]], list[dict[str, float]]]:
    uninformed_rows: list[dict[str, float]] = []
    heuristic_rows: list[dict[str, float]] = []
    for _ in range(n_runs):
        uninformed_rows.append(_trial(question, answer, heuristic=False))
    for _ in range(n_runs):
        heuristic_rows.append(_trial(question, answer, heuristic=True))
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
    u_o = [r["operations"] for r in uninformed_rows]
    h_o = [r["operations"] for r in heuristic_rows]
    u_b = [r["backtracks"] for r in uninformed_rows]
    h_b = [r["backtracks"] for r in heuristic_rows]
    u_n = [r["nodes_explored"] for r in uninformed_rows]
    h_n = [r["nodes_explored"] for r in heuristic_rows]

    def pct_improvement(baseline: float, improved: float) -> float | None:
        if baseline == 0:
            return None
        return 100.0 * (baseline - improved) / baseline

    return {
        "uninformed": {
            "mean_time": _mean(u_t),
            "stdev_time": _stdev(u_t),
            "mean_operations": _mean(u_o),
            "stdev_operations": _stdev(u_o),
            "mean_backtracks": _mean(u_b),
            "mean_nodes_explored": _mean(u_n),
            "stdev_nodes_explored": _stdev(u_n),
        },
        "heuristic": {
            "mean_time": _mean(h_t),
            "stdev_time": _stdev(h_t),
            "mean_operations": _mean(h_o),
            "stdev_operations": _stdev(h_o),
            "mean_backtracks": _mean(h_b),
            "mean_nodes_explored": _mean(h_n),
            "stdev_nodes_explored": _stdev(h_n),
        },
        "pct_faster_time": pct_improvement(_mean(u_t), _mean(h_t)),
        "pct_fewer_operations": pct_improvement(_mean(u_o), _mean(h_o)),
        "pct_fewer_backtracks": pct_improvement(_mean(u_b), _mean(h_b)),
        "pct_fewer_nodes_explored": pct_improvement(_mean(u_n), _mean(h_n)),
    }


def _bar_chart_baseline(ax, values: list[float]) -> None:
    ax.axhline(0, color="gray", linewidth=0.8, zorder=0)
    lo, hi = min(values), max(values)
    if lo >= 0:
        ax.set_ylim(0, max(hi * 1.15, 1e-9))
    else:
        pad = (hi - lo) * 0.1 + 1e-9
        ax.set_ylim(lo - pad, hi + pad)
    ax.yaxis.set_major_formatter(_plain_axis_formatter())


def plot_bars(
    summary: dict[str, Any],
    *,
    n_runs: int,
    out_dir: Path,
) -> tuple[Path, Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    labels = ["Uninformed", "Heuristic"]
    u = summary["uninformed"]
    h = summary["heuristic"]

    fig, ax = plt.subplots(figsize=(6, 4))
    times = [u["mean_time"], h["mean_time"]]
    ax.bar(labels, times, color=["#4c72b0", "#55a868"])
    _bar_chart_baseline(ax, times)
    ax.set_ylabel("Mean solve time (s)")
    ax.set_title(f"Solve time (mean of {n_runs} runs, same puzzle)")
    fig.tight_layout()
    p_time = out_dir / "mean_solve_time.png"
    fig.savefig(p_time, dpi=150, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    ops = [u["mean_operations"], h["mean_operations"]]
    ax.bar(labels, ops, color=["#4c72b0", "#55a868"])
    _bar_chart_baseline(ax, ops)
    ax.set_ylabel("Mean operations")
    ax.set_title(f"Search effort (mean of {n_runs} runs, same puzzle)")
    fig.tight_layout()
    p_ops = out_dir / "mean_operations.png"
    fig.savefig(p_ops, dpi=150, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    nodes = [u["mean_nodes_explored"], h["mean_nodes_explored"]]
    ax.bar(labels, nodes, color=["#4c72b0", "#55a868"])
    _bar_chart_baseline(ax, nodes)
    ax.set_ylabel("Mean nodes explored")
    ax.set_title(f"Search tree size (mean of {n_runs} runs, same puzzle)")
    fig.tight_layout()
    p_nodes = out_dir / "mean_nodes_explored.png"
    fig.savefig(p_nodes, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return p_time, p_ops, p_nodes


def load_puzzle(csv_path: Path, row_index: int) -> tuple[str, str]:
    df = pd.read_csv(csv_path, usecols=["question", "answer"])
    if row_index < 0 or row_index >= len(df):
        raise IndexError(f"row_index {row_index} out of range for {csv_path} (len={len(df)})")
    row = df.iloc[row_index]
    return str(row["question"]), str(row["answer"])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Benchmark uninformed vs heuristic SudokuSolver on one CSV row."
    )
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
    print("  Uninformed - mean operations:", summary["uninformed"]["mean_operations"])
    print("  Heuristic  - mean operations:", summary["heuristic"]["mean_operations"])
    print("  Uninformed - mean nodes explored:", summary["uninformed"]["mean_nodes_explored"])
    print("  Heuristic  - mean nodes explored:", summary["heuristic"]["mean_nodes_explored"])
    if summary["pct_faster_time"] is not None:
        print(f"  Heuristic ~{summary['pct_faster_time']:.1f}% faster (time) vs uninformed mean")
    else:
        print("  Time % improvement: N/A (zero uninformed mean time)")
    if summary["pct_fewer_operations"] is not None:
        print(
            f"  Heuristic ~{summary['pct_fewer_operations']:.1f}% fewer operations vs uninformed mean"
        )
    else:
        print("  Operations % improvement: N/A (zero uninformed mean operations)")
    if summary["pct_fewer_nodes_explored"] is not None:
        print(
            "  Heuristic "
            + f"~{summary['pct_fewer_nodes_explored']:.1f}% fewer nodes explored vs uninformed mean"
        )
    else:
        print("  Nodes explored % improvement: N/A (zero uninformed mean nodes explored)")
    if summary["pct_fewer_backtracks"] is not None:
        print(
            f"  Heuristic ~{summary['pct_fewer_backtracks']:.1f}% fewer backtracks vs uninformed mean"
        )
    else:
        print("  Backtracks % improvement: N/A (zero uninformed mean backtracks)")

    p_time, p_ops, p_nodes = plot_bars(summary, n_runs=args.runs, out_dir=args.figures_dir)
    print(f"\nWrote {p_time}")
    print(f"Wrote {p_ops}")
    print(f"Wrote {p_nodes}")


if __name__ == "__main__":
    main()
