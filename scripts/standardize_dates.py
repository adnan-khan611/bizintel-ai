from pathlib import Path

from bizintel.data.readers import read_csv_file
from bizintel.data.standardize_dates import standardize_datetime_column

RAW_DATA_DIR = Path("data/raw")


DATE_COLUMNS = {
    "orders": {
        "filename": "olist_orders_dataset.csv",
        "columns": [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    },
    "order_items": {
        "filename": "olist_order_items_dataset.csv",
        "columns": [
            "shipping_limit_date",
        ],
    },
}


def main() -> None:
    """Standardize datetime columns in core Olist datasets."""
    overall_invalid_count = 0

    for dataset_name, configuration in DATE_COLUMNS.items():
        file_path = RAW_DATA_DIR / configuration["filename"]
        dataframe = read_csv_file(file_path)

        print("\n" + "=" * 60)
        print(f"DATASET: {dataset_name}")
        print("=" * 60)

        for column in configuration["columns"]:
            result = standardize_datetime_column(
                dataframe,
                column,
            )

            dataframe = result.dataframe
            overall_invalid_count += result.invalid_count

            print(f"\nColumn: {column}")
            print(f"Invalid values: {result.invalid_count}")
            print(
                f"Final dtype: "
                f"{dataframe[column].dtype}"
            )

    print("\n" + "=" * 60)
    print(
        "TOTAL INVALID DATE VALUES: "
        f"{overall_invalid_count}"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()