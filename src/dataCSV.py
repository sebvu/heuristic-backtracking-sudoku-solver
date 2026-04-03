import csv
from pathlib import Path

from world import SudokuWorld

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EXP_DATA_CSV_PATH = REPO_ROOT / "figures" / "exp_data.csv"

EXPDATA_COLUMNS = [
    "isHeuristic",
    "solveTimeSecs",
    "numOfOperations",
    "numOfBacktraces",
    "peakMemUsage",
    "numOfNodesExplored",
    "timedOut",
]


def write_expdata_csv(
    world: SudokuWorld,
    *,
    path: Path = DEFAULT_EXP_DATA_CSV_PATH,
) -> Path:
    """Write one CSV row per recorded experiment run."""
    path.parent.mkdir(parents=True, exist_ok=True)

    lengths = {col: len(world.expData[col]) for col in EXPDATA_COLUMNS}
    if len(set(lengths.values())) > 1:
        raise ValueError(f"expData columns have unequal lengths: {lengths}")

    run_numbers = {False: 0, True: 0}

    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "runNumber",
                "solver",
                *EXPDATA_COLUMNS,
            ],
        )
        writer.writeheader()

        rows = zip(*(world.expData[col] for col in EXPDATA_COLUMNS))
        for row in rows:
            row_data = dict(zip(EXPDATA_COLUMNS, row))
            is_heuristic = bool(row_data["isHeuristic"])
            run_numbers[is_heuristic] += 1

            writer.writerow(
                {
                    "runNumber": run_numbers[is_heuristic],
                    "solver": "heuristic" if is_heuristic else "uninformed",
                    **row_data,
                }
            )

    return path
