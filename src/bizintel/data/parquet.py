"""Parquet data utilities for BizIntel AI."""

from pathlib import Path

import pandas as pd


def write_parquet_file(
    dataframe: pd.DataFrame,
    file_path: Path,
) -> None:
    """Write a DataFrame to a Parquet file."""
    if file_path.suffix.lower() != ".parquet":
        raise ValueError(
            f"Expected a Parquet file, got: {file_path.name}"
        )

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_parquet(
        file_path,
        engine="pyarrow",
        index=False,
    )


def read_parquet_file(
    file_path: Path,
) -> pd.DataFrame:
    """Read a DataFrame from a Parquet file."""
    if file_path.suffix.lower() != ".parquet":
        raise ValueError(
            f"Expected a Parquet file, got: {file_path.name}"
        )

    if not file_path.exists():
        raise FileNotFoundError(
            f"Parquet file not found: {file_path}"
        )

    return pd.read_parquet(
        file_path,
        engine="pyarrow",
    )