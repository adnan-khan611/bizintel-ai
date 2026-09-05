from pathlib import Path

import pandas as pd

RAW_DATA_DIR = Path("data/raw")


def inspect_csv(file_path: Path) -> None:
    """Print basic information about a CSV dataset."""
    print("\n" + "=" * 80)
    print(f"FILE: {file_path.name}")
    print("=" * 80)

    df = pd.read_csv(file_path)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nData types:")
    print(df.dtypes.to_string())

    print("\nMissing values:")
    missing = df.isna().sum()
    missing = missing[missing > 0]

    if missing.empty:
        print("  No missing values")
    else:
        print(missing.to_string())

    print("\nDuplicate rows:")
    print(f"  {df.duplicated().sum():,}")


def main() -> None:
    """Inspect all CSV files in the raw data directory."""
    csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in {RAW_DATA_DIR}"
        )

    print(f"Found {len(csv_files)} CSV files.")

    for file_path in csv_files:
        inspect_csv(file_path)


if __name__ == "__main__":
    main()