"""Build canonical datasets and write them to Parquet."""

from pathlib import Path

from bizintel.data.pipeline import build_and_write_canonical_datasets

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def main() -> None:
    """Build and write all MVP canonical datasets."""
    datasets = build_and_write_canonical_datasets(
        raw_data_dir=RAW_DATA_DIR,
        processed_data_dir=PROCESSED_DATA_DIR,
    )

    print("Canonical Parquet datasets created:")
    print("=" * 40)

    for dataset_name, dataframe in datasets.items():
        output_path = (
            PROCESSED_DATA_DIR
            / f"{dataset_name}.parquet"
        )

        print(f"\n{dataset_name}")
        print(f"  Rows: {len(dataframe):,}")
        print(f"  Columns: {len(dataframe.columns)}")
        print(f"  File: {output_path}")
        print(f"  Size: {output_path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()