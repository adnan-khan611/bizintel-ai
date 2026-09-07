from pathlib import Path

from bizintel.data.money import convert_to_minor_units
from bizintel.data.readers import read_csv_file

RAW_DATA_DIR = Path("data/raw")


MONEY_COLUMNS = {
    "order_items": {
        "filename": "olist_order_items_dataset.csv",
        "columns": [
            "price",
            "freight_value",
        ],
    },
    "order_payments": {
        "filename": "olist_order_payments_dataset.csv",
        "columns": [
            "payment_value",
        ],
    },
}


def main() -> None:
    """Validate and standardize monetary values in Olist data."""
    for dataset_name, configuration in MONEY_COLUMNS.items():
        file_path = RAW_DATA_DIR / configuration["filename"]
        dataframe = read_csv_file(file_path)

        print("\n" + "=" * 60)
        print(f"DATASET: {dataset_name}")
        print("=" * 60)

        for column in configuration["columns"]:
            series = dataframe[column]

            negative_count = int((series < 0).sum())
            missing_count = int(series.isna().sum())
            zero_count = int((series == 0).sum())

            standardized = convert_to_minor_units(series)

            print(f"\nColumn: {column}")
            print(f"Rows: {len(series):,}")
            print(f"Missing values: {missing_count:,}")
            print(f"Zero values: {zero_count:,}")
            print(f"Negative values: {negative_count:,}")
            print(f"Original dtype: {series.dtype}")
            print(f"Standardized dtype: {standardized.dtype}")
            print(
                f"Original total: {series.sum():,.2f}"
            )
            print(
                f"Minor-unit total: {standardized.sum():,}"
            )


if __name__ == "__main__":
    main()