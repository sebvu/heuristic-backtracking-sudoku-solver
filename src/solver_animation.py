"""
Create an animation that compares the uninformed and heuristic solving methods
to show the efficiency and effectiveness/difference between the methods

Since it would not be feasible to render every single frame, important ones are chosen
    - maxFrames set to 300
    - fps set to 12
    - Saves the animation to the figures folder
"""

# Imports needed to run the algorithms and create the frames/animation
from __future__ import annotations
from dataclasses import dataclass
import argparse
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from pathlib import Path
from io import BytesIO
from PIL import Image

from solver import SudokuSolver
from world import SudokuWorld

# The main constants to store the path and the animation info
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = REPO_ROOT / "data" / "test.csv"
DEFAULT_OUTPUT = REPO_ROOT / "figures" / "solver_animation.gif"
DEFAULT_MAX_FRAMES = 300
DEFAULT_FPS = 12

# Dataclass to store trace frame information for animation 
@dataclass
class TraceFrame:
    board: list[list[int]]
    action: str
    operations: int
    nodes_explored: int
    backtracks: int
    highlight: tuple[int, int] | None = None

# Deep copy of sudoku board at an instance for animation
def _copyBoard(board: list[list[int]]) -> list[list[int]]:
    return [row[:] for row in board]

# Inherited Sudoku class with modifications for the traces for animation
class TracingSudokuSolver(SudokuSolver):
    def __init__(self, world: SudokuWorld):
        super().__init__(world)
        self.trace: list[TraceFrame] = []

    # Snapshot of the sudoku board and metrics
    def _snapshot(
        self,
        action: str,
        *,
        highlight: tuple[int, int] | None = None,
        backtracks_override: int | None = None,
    ) -> None:
        self.trace.append(
            TraceFrame(
                board=_copyBoard(self.world.sMap),
                action=action,
                operations=self.numOfOps,
                nodes_explored=self.numOfNodesExplored,
                backtracks=self.numOfBtraces if backtracks_override is None else backtracks_override,
                highlight=highlight,
            )
        )

    # Overwritten methods to add snapshots to base methods
    def _placeValue(self, row, col, num):
        super()._placeValue(row, col, num)
        self._snapshot(
            f"place {num} at r{row + 1}c{col + 1}",
            highlight=(row, col),
        )

    def _clearValue(self, row, col):
        prev_value = self.world.sMap[row][col]
        super()._clearValue(row, col)
        self._snapshot(
            f"backtrack clear {prev_value} at r{row + 1}c{col + 1}",
            highlight=(row, col),
            backtracks_override=self.numOfBtraces + 1,
        )

    # Clear field for next trace
    def _prepareTrace(self, question: str) -> None:
        self._resetMetrics()
        self.trace = []
        self.world.populateSudokuWorld(question)
        self._snapshot("start")

    # Uninformed solve with trace
    def traceUninformed(self, question: str, answer: str) -> list[TraceFrame]:
        self._prepareTrace(question)
        if not self.world.verifyTerminalReached(answer):
            solved = self._backtrackUninformed()
            if not solved:
                raise ValueError("uninformed solver could not solve the puzzle")
        if not self.world.verifyTerminalReached(answer):
            raise ValueError("uninformed solver did not reach the expected terminal state")
        self._snapshot("solved")
        return self.trace

    # Heuristic solve with trace
    def traceHeuristic(self, question: str, answer: str) -> list[TraceFrame]:
        self._prepareTrace(question)
        if not self.world.verifyTerminalReached(answer):
            solved = self._backtrackHeuristic()
            if not solved:
                raise ValueError("heuristic solver could not solve the puzzle")
        if not self.world.verifyTerminalReached(answer):
            raise ValueError("heuristic solver did not reach the expected terminal state")
        self._snapshot("solved")
        return self.trace
    
# Load a sudoku puzzle for solving
def loadPuzzle(csvPath: Path, rowIndex: int) -> tuple[str, str]:
    with csvPath.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for idx, row in enumerate(reader):
            if idx == rowIndex:
                return str(row["question"]), str(row["answer"])
    raise IndexError(f"rowIndex {rowIndex} out of range for {csvPath}")

# Build and run uninformed and heuristic solve
def buildTraces(question: str, answer: str) -> tuple[list[TraceFrame], list[TraceFrame]]:
    uninformedWorld = SudokuWorld()
    heuristicWorld = SudokuWorld()

    uninformedSolver = TracingSudokuSolver(uninformedWorld)
    heuristicSolver = TracingSudokuSolver(heuristicWorld)

    return (
        uninformedSolver.traceUninformed(question, answer),
        heuristicSolver.traceHeuristic(question, answer)
    )

# Choose traces when the trace is too long
def sampledIndices(length: int, maxFrames: int) -> list[int]:
    if length <= 0:
        return [0]
    if maxFrames <= 1:
        return [0 if length == 1 else length - 1]
    if length <= maxFrames:
        return list(range(length))
    last = length - 1
    return sorted({min(last, round(i * last / (maxFrames - 1))) for i in range(maxFrames)})

# Use matplotlib to draw the board at a frame
def drawBoard(ax, frame: TraceFrame, title: str) -> None:
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.set_aspect("equal")
    ax.axis("off")

    for row in range(9):
        for col in range(9):
            y = 8 - row
            facecolor = "#fbf7ef"
            if frame.highlight == (row, col):
                if frame.action.startswith("backtrack"):
                    facecolor = "#f7d6d6"
                else:
                    facecolor = "#d9f0d8"
            ax.add_patch(
                Rectangle((col, y), 1, 1, facecolor=facecolor, edgecolor="#d0d0d0", linewidth=0.6)
            )

    for idx in range(10):
        width = 2.2 if idx % 3 == 0 else 0.9
        ax.plot([idx, idx], [0, 9], color="black", linewidth=width)
        ax.plot([0, 9], [idx, idx], color="black", linewidth=width)

    for row in range(9):
        for col in range(9):
            value = frame.board[row][col]
            if value:
                ax.text(
                    col + 0.5,
                    8 - row + 0.5,
                    str(value),
                    ha="center",
                    va="center",
                    fontsize=18,
                    fontweight="bold",
                    color="#1f1f1f",
                )

    ax.set_title(title, fontsize=16, fontweight="bold", pad=10)
    ax.text(
        0.0,
        -0.18,
        "\n".join(
            [
                f"action: {frame.action}",
                f"ops: {frame.operations:,}",
                f"nodes: {frame.nodes_explored:,}",
                f"backtracks: {frame.backtracks:,}",
            ]
        ),
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=10,
        family="monospace",
    )

# Render the individual frames with boards side by side
def renderFrame(
    leftFrame: TraceFrame, 
    rightFrame: TraceFrame,
    *,
    frame_num: int,
    total_frames: int    
) -> bytes:
    fig, axes = plt.subplots(1, 2, figsize=(12, 7))
    fig.patch.set_facecolor("#f2efe8")
    fig.suptitle(
        f"Sudoku Solver Trace  |  Frame {frame_num + 1}/{total_frames}",
        fontsize=18,
        fontweight="bold",
        y=0.98,
    )
    drawBoard(axes[0], leftFrame, "Uninformed")
    drawBoard(axes[1], rightFrame, "Heuristic")
    fig.tight_layout(rect=[0.0, 0.05, 1.0, 0.95])

    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=140, bbox_inches="tight")
    plt.close(fig)
    return buf.getvalue()  

# Build the full gif/animation from the frames rendered
def writeAnimation(
    uninformedTrace: list[TraceFrame],
    heuristicTrace: list[TraceFrame],
    outputPath: Path,
    *,
    fps: int,
    total_frames: int
) -> Path:
    outputPath.parent.mkdir(parents=True, exist_ok=True)

    totalSteps = max(len(uninformedTrace), len(heuristicTrace))
    indices = sampledIndices(totalSteps, total_frames)

    rendered: list[bytes] = []
    for frameNum, stepIdx in enumerate(indices):
        leftFrame = uninformedTrace[min(stepIdx, len(uninformedTrace) - 1)]
        rightFrame = heuristicTrace[min(stepIdx, len(heuristicTrace) - 1)]
        rendered.append(
            renderFrame(leftFrame, rightFrame, frame_num=frameNum, total_frames=len(indices))
        )

    frames = [Image.open(BytesIO(png)).convert("P", palette=Image.ADAPTIVE) for png in rendered]
    frames[0].save(outputPath, save_all=True, append_images=frames[1:], duration=max(1, int(1000 / max(fps, 1))), loop=0)
    return outputPath

# Main function to run sudoku solves, render frames, and create the animation
def main() -> None:
    csvPath = DEFAULT_CSV
    row = 0
    outputPath = DEFAULT_OUTPUT
    fps = DEFAULT_FPS
    maxFrames = DEFAULT_MAX_FRAMES

    question, answer = loadPuzzle(csvPath, row)
    uninformedTrace, heuristicTrace = buildTraces(question, answer)
    writtenPath = writeAnimation(uninformedTrace, heuristicTrace, outputPath, fps=fps, total_frames=maxFrames)

    print(f"Built uninformed trace with {len(uninformedTrace)} states")
    print(f"Built heuristic trace with {len(heuristicTrace)} states")
    print(f"Wrote animation to {writtenPath}")


if __name__ == "__main__":
    main()
    
