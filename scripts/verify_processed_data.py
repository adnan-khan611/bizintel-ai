"""Verify processed Parquet datasets."""

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


EXPECTED_DATASETS = {
    "customers": {
        "rows": 96_096,
        "columns": [
            "customer_id",
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state",
        ],
    },
    "products": {
        "rows": 32_951,
        "columns": [
            "product_id",
            "product_category_name",
            "product_name_length",
            "product_description_length",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm",
        ],
    },
    "orders": {
        "rows": 99_441,
        "columns": [
            "order_id",
            "customer_id",
            "order_status",
            "order_date",
            "order_approved_at",
            "order_delivered_carrier_at",
            "order_delivered_customer_at",
            "order_estimated_delivery_at",
        ],
    },
    "order_items": {
        "rows": 112_650,
        "columns": [
            "order_id",
            "order_item_id",
            "product_id",
            "seller_id",
            "shipping_limit_at",
            "price_minor",
            "freight_value_minor",
        ],
    },
    "order_payments": {
        "rows": 103_886,
        "columns": [
            "payment_id",
            "order_id",
            "payment_sequential",
            "payment_type",
            "payment_installments",
            "payment_value_minor",
        ],
    },
}


def verify_dataset(
    dataset_name: str,
    expected_rows: int,
    expected_columns: list[str],
) -> None:
    """Verify one processed Parquet dataset."""
    file_path = (
        PROCESSED_DATA_DIR
        / f"{dataset_name}.parquet"
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {file_path}"
        )

    dataframe = pd.read_parquet(
        file_path,
        engine="pyarrow",
    )

    if len(dataframe) != expected_rows:
        raise ValueError(
            f"{dataset_name}: expected "
            f"{expected_rows:,} rows, got "
            f"{len(dataframe):,}."
        )

    if list(dataframe.columns) != expected_columns:
        raise ValueError(
            f"{dataset_name}: column schema mismatch.\n"
            f"Expected: {expected_columns}\n"
            f"Actual: {list(dataframe.columns)}"
        )

    print(f"\n{dataset_name}: VALID")
    print(f"  Rows: {len(dataframe):,}")
    print(f"  Columns: {len(dataframe.columns)}")
    print(f"  File size: {file_path.stat().st_size:,} bytes")
    print("  Schema: correct")


def main() -> None:
    """Verify all processed Parquet datasets."""
    print("Processed Data Verification")
    print("=" * 40)

    for dataset_name, expected in EXPECTED_DATASETS.items():
        verify_dataset(
            dataset_name,
            expected["rows"],
            expected["columns"],
        )

    print("\nOverall:")
    print("  VALID")


if __name__ == "__main__":
    main()