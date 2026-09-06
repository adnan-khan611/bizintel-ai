from pathlib import Path

import pandas as pd


def read_csv_file(file_path: Path) -> pd.DataFrame:
    """Read a CSV file into a pandas DataFrame."""
    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    if file_path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a CSV file, got: {file_path.name}")

    return pd.read_csv(file_path)