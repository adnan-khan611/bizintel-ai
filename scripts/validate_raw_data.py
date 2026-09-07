from pathlib import Path

from bizintel.data.readers import read_csv_file
from bizintel.data.validators import validate_dataset

RAW_DATA_DIR = Path("data/raw")


DATASET_FILES = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
}


def print_validation_result(result) -> None:
    """Print validation errors and warnings."""
    if result.is_valid:
        print("Status: VALID")
    else:
        print("Status: INVALID")

    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"- {error}")

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"- {warning}")

    if not result.errors and not result.warnings:
        print("No validation issues found.")


def main() -> None:
    """Validate the core Olist datasets."""
    for dataset_name, filename in DATASET_FILES.items():
        file_path = RAW_DATA_DIR / filename

        print("\n" + "=" * 60)
        print(f"DATASET: {dataset_name}")
        print("=" * 60)

        dataframe = read_csv_file(file_path)
        result = validate_dataset(dataframe, dataset_name)

        print_validation_result(result)


if __name__ == "__main__":
    main()