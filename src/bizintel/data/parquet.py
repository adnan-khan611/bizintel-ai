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

    file_path.parent.mkdir(parents=True, exist_ok=True)

    dataframe.to_parquet(
        file_path,
        engine="pyarrow",
        index=False,
    )