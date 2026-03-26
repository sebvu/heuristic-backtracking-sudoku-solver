"""
Plots and tables from interpretExpData() output. Does not modify solvers.

Run from repo root with PYTHONPATH=src:
  python -m data_visualization --demo
After main.py has filled expData, you can also import save_interpretation_figures from elsewhere.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from world import SudokuWorld

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FIGURES_DIR = REPO_ROOT / "figures"

METRIC_LABELS = {
    "solveTimeSecs": "Solve time (s)",
    "numOfOperations": "Operations",
    "numOfBacktraces": "Backtraces",
    "peakMemUsage": "Peak memory (MB)",
}


def format_interpretation_text(result: dict[str, Any]) -> str:
    """Human-readable summary for console or logs."""
    lines: list[str] = []
    lines.append(
        f"Runs: uninformed={result['n_uninformed']}, heuristic={result['n_heuristic']}"
    )
    for label, key in ("Uninformed", "uninformed"), ("Heuristic", "heuristic"):
        lines.append(f"\n{label} (best / worst / mean):")
        block = result[key]
        for m, title in METRIC_LABELS.items():
            s = block[m]
            if s["mean"] is None:
                lines.append(f"  {title}: (no data)")
            else:
                lines.append(
                    f"  {title}: min={s['min']:.6g} max={s['max']:.6g} mean={s['mean']:.6g}"
                )
    lines.append("\nHeuristic vs uninformed (mean baseline %; positive => heuristic lower/faster):")
    for m, title in METRIC_LABELS.items():
        p = result["comparison_pct"][m]
        if p is None:
            lines.append(f"  {title}: N/A")
        else:
            lines.append(f"  {title}: {p:+.2f}%")
    return "\n".join(lines)


def save_interpretation_figures(
    result: dict[str, Any],
    *,
    out_dir: Path | None = None,
) -> list[Path]:
    """
    Write PNGs: side-by-side means per metric, and comparison % bar chart.
    Skips metrics with missing means.
    """
    out_dir = out_dir or DEFAULT_FIGURES_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    labels = ["Uninformed", "Heuristic"]
    for m, title in METRIC_LABELS.items():
        u = result["uninformed"][m]["mean"]
        h = result["heuristic"][m]["mean"]
        if u is None and h is None:
            continue
        u_val = 0.0 if u is None else u
        h_val = 0.0 if h is None else h
        fig, ax = plt.subplots(figsize=(6, 4))
        vals = [u_val, h_val]
        ax.bar(labels, vals, color=["#4c72b0", "#55a868"])
        ax.axhline(0, color="gray", linewidth=0.8, zorder=0)
        lo, hi = min(vals), max(vals)
        if lo >= 0:
            ax.set_ylim(0, max(hi * 1.15, 1e-12))
        else:
            pad = (hi - lo) * 0.1 + 1e-12
            ax.set_ylim(lo - pad, hi + pad)
        ax.set_ylabel(title)
        ax.set_title(f"{title} (mean)")
        fig.tight_layout()
        path = out_dir / f"interpret_{m}.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        written.append(path)

    pct = result["comparison_pct"]
    keys = [k for k in METRIC_LABELS if pct.get(k) is not None]
    if keys:
        fig, ax = plt.subplots(figsize=(7, 4))
        vals = [pct[k] for k in keys]
        short = [METRIC_LABELS[k].split("(")[0].strip() for k in keys]
        ax.barh(short, vals, color="#8172b3")
        lo = min(vals)
        hi = max(vals)
        pad = (hi - lo) * 0.08 + 1e-6
        ax.set_xlim(min(lo, 0) - pad, max(hi, 0) + pad)
        ax.axvline(0, color="gray", linewidth=0.8)
        ax.set_xlabel("% vs uninformed mean (positive => heuristic better)")
        ax.set_title("Heuristic vs uninformed (mean-based)")
        fig.tight_layout()
        path = out_dir / "interpret_comparison_pct.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        written.append(path)

    return written


def _demo_synthetic_world() -> SudokuWorld:
    w = SudokuWorld()
    w.clearExpData()
    # Two uninformed rows, two heuristic rows (synthetic)
    w.addExpData([False, 0.1, 100, 5, 1.0])
    w.addExpData([False, 0.2, 120, 8, 1.2])
    w.addExpData([True, 0.05, 40, 2, 0.8])
    w.addExpData([True, 0.08, 50, 3, 0.9])
    return w


def main() -> None:
    parser = argparse.ArgumentParser(description="Interpret expData and write figures.")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run synthetic expData and print/save (no solver run).",
    )
    parser.add_argument(
        "--figures-dir",
        type=Path,
        default=DEFAULT_FIGURES_DIR,
        help="Output directory for PNGs",
    )
    args = parser.parse_args()

    if args.demo:
        world = _demo_synthetic_world()
        result = world.interpretExpData()
        print(format_interpretation_text(result))
        paths = save_interpretation_figures(result, out_dir=args.figures_dir)
        for p in paths:
            print(f"Wrote {p}")
    else:
        parser.print_help()
        print("\nUse --demo to verify interpretation + plots without running main.")


if __name__ == "__main__":
    main()
