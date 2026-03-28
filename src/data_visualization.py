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
import pandas as pd
from matplotlib import ticker

from world import SudokuWorld
from constants import RANDOM_STATE

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FIGURES_DIR = REPO_ROOT / "figures"

METRIC_LABELS = {
    "solveTimeSecs": "Solve time (s)",
    "numOfOperations": "Operations",
    "numOfBacktraces": "Backtraces",
    "peakMemUsage": "Peak memory (MB)",
    "numOfNodesExplored": "Nodes explored",
}

DEFAULT_CASES = 300
DEFAULT_SUMMARY_PATH = DEFAULT_FIGURES_DIR / "summary.txt"
LOG_METRICS = {"numOfOperations", "numOfBacktraces", "numOfNodesExplored"}


def _format_number(x: float | int | None, *, decimals: int = 6) -> str:
    if x is None:
        return "N/A"
    v = float(x)
    if abs(v) >= 1000:
        if abs(v - round(v)) < 1e-12:
            return f"{int(round(v)):,}"
        return f"{v:,.2f}"
    s = f"{v:.{decimals}f}".rstrip("0").rstrip(".")
    return "0" if s in {"", "-0"} else s


def _plain_axis_formatter(decimals: int = 3) -> ticker.FuncFormatter:
    def _fmt(x: float, _pos: int) -> str:
        if abs(x) >= 1000:
            if abs(x - round(x)) < 1e-12:
                return f"{int(round(x)):,}"
            return f"{x:,.1f}"
        s = f"{x:.{decimals}f}".rstrip("0").rstrip(".")
        return "0" if s in {"", "-0"} else s

    return ticker.FuncFormatter(_fmt)


def _apply_metric_scale(ax, metric: str) -> str:
    if metric in LOG_METRICS:
        ax.set_yscale("log")
        ax.yaxis.set_major_locator(ticker.LogLocator(base=10))
        ax.yaxis.set_major_formatter(
            ticker.FuncFormatter(
                lambda y, _pos: f"{int(y):,}" if y >= 1 and abs(y - round(y)) < 1e-12 else ""
            )
        )
        return "log scale"
    ax.set_yscale("linear")
    ax.yaxis.set_major_formatter(_plain_axis_formatter())
    return "linear scale"


def write_summary_txt(text: str, *, path: Path = DEFAULT_SUMMARY_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _expdata_frame(world: SudokuWorld) -> pd.DataFrame:
    ed = world.expData
    df = pd.DataFrame(ed)
    if df.empty:
        return df
    for col in (
        "solveTimeSecs",
        "numOfOperations",
        "numOfBacktraces",
        "peakMemUsage",
        "numOfNodesExplored",
    ):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def _split_cases(df: pd.DataFrame, *, max_cases: int) -> tuple[pd.DataFrame, pd.DataFrame, int]:
    """Return (uninformed, heuristic, n_used) aligned by case index."""
    if df.empty:
        return df, df, 0
    u = df.loc[~df["isHeuristic"]].copy()
    h = df.loc[df["isHeuristic"]].copy()
    u["case"] = range(1, len(u) + 1)
    h["case"] = range(1, len(h) + 1)
    n = min(len(u), len(h), max_cases)
    return u.iloc[:n].reset_index(drop=True), h.iloc[:n].reset_index(drop=True), int(n)


def save_distribution_figures(
    world: SudokuWorld,
    *,
    out_dir: Path = DEFAULT_FIGURES_DIR,
    cases: int = DEFAULT_CASES,
) -> list[Path]:
    """Boxplots per metric (log only for count-based search metrics)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    df = _expdata_frame(world)
    u, h, n = _split_cases(df, max_cases=cases)
    written: list[Path] = []
    if n == 0:
        return written

    for m, title in METRIC_LABELS.items():
        u_vals, h_vals = _metric_series_pair(u, h, m)
        if u_vals.empty or h_vals.empty:
            continue
        
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.boxplot(
            [u_vals.values, h_vals.values],
            tick_labels=["Uninformed", "Heuristic"],
            showfliers=False,
        )
        scale_label = _apply_metric_scale(ax, m)
        ax.set_ylabel(title)
        ax.set_title(f"{title} distribution (first {n} cases, {scale_label})")
        fig.tight_layout()
        path = out_dir / f"dist_{m}.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        written.append(path)
    return written


def _cummean(xs: pd.Series) -> pd.Series:
    return xs.expanding(min_periods=1).mean()


def _metric_series_pair(
    u: pd.DataFrame,
    h: pd.DataFrame,
    metric: str,
) -> tuple[pd.Series, pd.Series]:
    return u[metric].dropna(), h[metric].dropna()


def save_trend_figures_log(
    world: SudokuWorld,
    *,
    out_dir: Path = DEFAULT_FIGURES_DIR,
    cases: int = DEFAULT_CASES,
) -> list[Path]:
    """Cumulative mean trends (log only for count-based search metrics)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    df = _expdata_frame(world)
    u, h, n = _split_cases(df, max_cases=cases)
    written: list[Path] = []
    if n == 0:
        return written

    x = range(1, n + 1)
    for m, title in METRIC_LABELS.items():
        u_vals, h_vals = _metric_series_pair(u, h, m)
        if u_vals.empty or h_vals.empty:
            continue
        
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(x, _cummean(u[m]).values, label="Uninformed", color="#4c72b0")
        ax.plot(x, _cummean(h[m]).values, label="Heuristic", color="#55a868")
        scale_label = _apply_metric_scale(ax, m)
        ax.set_xlabel("Case # (aligned)")
        ax.set_ylabel(f"Cumulative mean {title}")
        ax.set_title(f"Cumulative mean over cases ({scale_label}) — {title}")
        ax.legend()
        fig.tight_layout()
        path = out_dir / f"trend_cummean_{m}.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        written.append(path)
    return written


def save_trend_figures_pct_improvement(
    world: SudokuWorld,
    *,
    out_dir: Path = DEFAULT_FIGURES_DIR,
    cases: int = DEFAULT_CASES,
) -> list[Path]:
    """Cumulative mean % improvement vs uninformed baseline over cases."""
    out_dir.mkdir(parents=True, exist_ok=True)
    df = _expdata_frame(world)
    u, h, n = _split_cases(df, max_cases=cases)
    written: list[Path] = []
    if n == 0:
        return written

    x = range(1, n + 1)
    for m, title in METRIC_LABELS.items():
        u_vals, h_vals = _metric_series_pair(u, h, m)
        if u_vals.empty or h_vals.empty:
            continue
        
        u_c = _cummean(u[m])
        h_c = _cummean(h[m])
        pct = pd.Series([None] * n, dtype="float64")
        mask = u_c != 0
        pct.loc[mask] = 100.0 * (u_c.loc[mask] - h_c.loc[mask]) / u_c.loc[mask]

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(x, pct.values, color="#8172b3")
        ax.axhline(0, color="gray", linewidth=0.8)
        ax.set_xlabel("Case # (aligned)")
        ax.set_ylabel("% improvement vs uninformed (cumulative mean)")
        ax.set_title(f"% improvement over time — {title}")
        ax.yaxis.set_major_formatter(_plain_axis_formatter(decimals=2))
        finite = pct.dropna()
        if not finite.empty:
            lo = float(finite.min())
            hi = float(finite.max())
            pad = (hi - lo) * 0.1 + 1e-6
            ax.set_ylim(min(lo, 0) - pad, max(hi, 0) + pad)
        fig.tight_layout()
        path = out_dir / f"trend_pct_improvement_{m}.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        written.append(path)
    return written


def write_all_outputs(
    world: SudokuWorld,
    *,
    out_dir: Path = DEFAULT_FIGURES_DIR,
    cases: int = DEFAULT_CASES,
    summary_path: Path = DEFAULT_SUMMARY_PATH,
) -> tuple[str, list[Path], Path]:
    """One-stop: interpret, write summary.txt, and write all figures."""
    result = world.interpretExpData()
    text = format_interpretation_text(result)
    summary_file = write_summary_txt(text, path=summary_path)
    written: list[Path] = []
    written += save_interpretation_figures(result, out_dir=out_dir)
    written += save_distribution_figures(world, out_dir=out_dir, cases=cases)
    written += save_trend_figures_log(world, out_dir=out_dir, cases=cases)
    written += save_trend_figures_pct_improvement(world, out_dir=out_dir, cases=cases)
    return text, written, summary_file


def format_interpretation_text(result: dict[str, Any]) -> str:
    """Human-readable summary for console or logs."""
    lines: list[str] = []
    lines.append(
        f"Runs: uninformed={result['n_uninformed']}, heuristic={result['n_heuristic']}"
    )
    lines.append(f"\n Random Seed Used: {RANDOM_STATE}")
    for label, key in ("Uninformed", "uninformed"), ("Heuristic", "heuristic"):
        lines.append(f"\n{label} (best / worst / mean):")
        block = result[key]
        for m, title in METRIC_LABELS.items():
            s = block[m]
            if s["mean"] is None:
                lines.append(f"  {title}: (no data)")
            else:
                lines.append(
                    "  "
                    + f"{title}: min={_format_number(s['min'])} "
                    + f"max={_format_number(s['max'])} "
                    + f"mean={_format_number(s['mean'])}"
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
        if u is None or h is None:
            continue
        
        fig, ax = plt.subplots(figsize=(6, 4))
        vals = [u, h]
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
        ax.yaxis.set_major_formatter(_plain_axis_formatter())
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
        ax.xaxis.set_major_formatter(_plain_axis_formatter(decimals=2))
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
    w.addExpData([False, 0.1, 100, 5, 1.0, 30])
    w.addExpData([False, 0.2, 120, 8, 1.2, 36])
    w.addExpData([True, 0.05, 40, 2, 0.8, 12])
    w.addExpData([True, 0.08, 50, 3, 0.9, 15])
    return w


def main() -> None:
    parser = argparse.ArgumentParser(description="Interpret expData and write figures.")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run synthetic expData and print/save (no solver run).",
    )
    parser.add_argument(
        "--cases",
        type=int,
        default=DEFAULT_CASES,
        help=f"Aligned cases to use for dist/trend plots (default: {DEFAULT_CASES})",
    )
    parser.add_argument(
        "--figures-dir",
        type=Path,
        default=DEFAULT_FIGURES_DIR,
        help="Output directory for PNGs",
    )
    parser.add_argument(
        "--summary-path",
        type=Path,
        default=DEFAULT_SUMMARY_PATH,
        help="Path for summary.txt output",
    )
    args = parser.parse_args()

    if args.demo:
        world = _demo_synthetic_world()
        text, paths, summary_file = write_all_outputs(
            world,
            out_dir=args.figures_dir,
            cases=int(args.cases),
            summary_path=args.summary_path,
        )
        print(text)
        print(f"Wrote {summary_file}")
        for p in paths:
            print(f"Wrote {p}")
    else:
        parser.print_help()
        print("\nUse --demo to verify interpretation + plots without running main.")


if __name__ == "__main__":
    main()
