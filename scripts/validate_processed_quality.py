"""Validate the quality of processed Parquet datasets."""

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def validate_primary_key(
    dataframe: pd.DataFrame,
    column: str,
    dataset_name: str,
) -> list[str]:
    """Validate a single-column primary key."""
    errors = []

    if dataframe[column].isna().any():
        errors.append(
            f"{dataset_name}: {column} contains null values."
        )

    if dataframe[column].duplicated().any():
        duplicate_count = int(
            dataframe[column].duplicated().sum()
        )
        errors.append(
            f"{dataset_name}: {column} has "
            f"{duplicate_count:,} duplicate values."
        )

    return errors


def validate_composite_key(
    dataframe: pd.DataFrame,
    columns: list[str],
    dataset_name: str,
) -> list[str]:
    """Validate a composite primary key."""
    errors = []

    if dataframe[columns].isna().any().any():
        errors.append(
            f"{dataset_name}: composite key contains null values."
        )

    if dataframe.duplicated(columns).any():
        duplicate_count = int(
            dataframe.duplicated(columns).sum()
        )
        errors.append(
            f"{dataset_name}: composite key has "
            f"{duplicate_count:,} duplicate records."
        )

    return errors


def validate_required_fields(
    dataframe: pd.DataFrame,
    columns: list[str],
    dataset_name: str,
) -> list[str]:
    """Validate that required fields contain no null values."""
    errors = []

    for column in columns:
        if dataframe[column].isna().any():
            null_count = int(dataframe[column].isna().sum())
            errors.append(
                f"{dataset_name}: {column} has "
                f"{null_count:,} null values."
            )

    return errors


def validate_non_negative(
    dataframe: pd.DataFrame,
    columns: list[str],
    dataset_name: str,
) -> list[str]:
    """Validate that numeric business values are non-negative."""
    errors = []

    for column in columns:
        negative_count = int(
            (dataframe[column] < 0).sum()
        )

        if negative_count > 0:
            errors.append(
                f"{dataset_name}: {column} has "
                f"{negative_count:,} negative values."
            )

    return errors


def validate_dataset(
    dataset_name: str,
    dataframe: pd.DataFrame,
) -> list[str]:
    """Run quality checks for one processed dataset."""
    errors = []

    if dataset_name == "customers":
        errors.extend(
            validate_primary_key(
                dataframe,
                "customer_id",
                dataset_name,
            )
        )
        errors.extend(
            validate_required_fields(
                dataframe,
                [
                    "customer_id",
                    "customer_zip_code_prefix",
                    "customer_city",
                    "customer_state",
                ],
                dataset_name,
            )
        )

    elif dataset_name == "products":
        errors.extend(
            validate_primary_key(
                dataframe,
                "product_id",
                dataset_name,
            )
        )
        errors.extend(
            validate_required_fields(
                dataframe,
                ["product_id"],
                dataset_name,
            )
        )

    elif dataset_name == "orders":
        errors.extend(
            validate_primary_key(
                dataframe,
                "order_id",
                dataset_name,
            )
        )
        errors.extend(
            validate_required_fields(
                dataframe,
                [
                    "order_id",
                    "customer_id",
                    "order_status",
                    "order_date",
                    "order_estimated_delivery_at",
                ],
                dataset_name,
            )
        )

    elif dataset_name == "order_items":
        errors.extend(
            validate_composite_key(
                dataframe,
                ["order_id", "order_item_id"],
                dataset_name,
            )
        )
        errors.extend(
            validate_required_fields(
                dataframe,
                [
                    "order_id",
                    "order_item_id",
                    "product_id",
                    "price_minor",
                    "freight_value_minor",
                ],
                dataset_name,
            )
        )
        errors.extend(
            validate_non_negative(
                dataframe,
                [
                    "price_minor",
                    "freight_value_minor",
                ],
                dataset_name,
            )
        )

    elif dataset_name == "order_payments":
        errors.extend(
            validate_primary_key(
                dataframe,
                "payment_id",
                dataset_name,
            )
        )
        errors.extend(
            validate_required_fields(
                dataframe,
                [
                    "payment_id",
                    "order_id",
                    "payment_sequential",
                    "payment_type",
                    "payment_installments",
                    "payment_value_minor",
                ],
                dataset_name,
            )
        )
        errors.extend(
            validate_non_negative(
                dataframe,
                [
                    "payment_installments",
                    "payment_value_minor",
                ],
                dataset_name,
            )
        )

    else:
        errors.append(
            f"Unknown dataset: {dataset_name}"
        )

    return errors


def main() -> None:
    """Validate all processed datasets."""
    datasets = [
        "customers",
        "products",
        "orders",
        "order_items",
        "order_payments",
    ]

    overall_errors = []

    print("Processed Data Quality Validation")
    print("=" * 40)

    for dataset_name in datasets:
        file_path = (
            PROCESSED_DATA_DIR
            / f"{dataset_name}.parquet"
        )

        dataframe = pd.read_parquet(
            file_path,
            engine="pyarrow",
        )

        errors = validate_dataset(
            dataset_name,
            dataframe,
        )

        if errors:
            print(f"\n{dataset_name}: INVALID")

            for error in errors:
                print(f"  ERROR: {error}")

            overall_errors.extend(errors)

        else:
            print(f"\n{dataset_name}: VALID")

    print("\nOverall:")

    if overall_errors:
        print("  INVALID")
        raise SystemExit(1)

    print("  VALID")


if __name__ == "__main__":
    main()