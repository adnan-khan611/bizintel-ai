from dataclasses import dataclass
from typing import Final

import pandas as pd

from bizintel.data.schemas import DATASET_SCHEMAS

REQUIRED_COLUMNS: Final = {
    "customers": {
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
    },
    "orders": {
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_estimated_delivery_date",
    },
    "order_items": {
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value",
    },
    "order_payments": {
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value",
    },
}


REQUIRED_FIELDS: Final = {
    "customers": ["customer_id", "customer_unique_id"],
    "orders": ["order_id", "customer_id", "order_purchase_timestamp"],
    "order_items": ["order_id", "product_id", "seller_id"],
    "order_payments": ["order_id"],
}


KEY_COLUMNS: Final = {
    "customers": ["customer_id"],
    "orders": ["order_id"],
    "order_items": ["order_id", "order_item_id"],
    "order_payments": ["order_id", "payment_sequential"],
}


@dataclass(frozen=True)
class ValidationResult:
    """Represent the result of validating a dataset."""

    dataset_name: str
    is_valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...] = ()


def validate_dataset_name(dataset_name: str) -> None:
    """Validate that the dataset name is supported."""
    if dataset_name not in DATASET_SCHEMAS:
        raise ValueError(f"Unsupported dataset: {dataset_name}")


def validate_columns(
    dataframe: pd.DataFrame,
    dataset_name: str,
) -> list[str]:
    """Return errors for missing required columns."""
    validate_dataset_name(dataset_name)

    required_columns = REQUIRED_COLUMNS[dataset_name]
    actual_columns = set(dataframe.columns)

    missing_columns = sorted(required_columns - actual_columns)

    return [
        f"Missing required column: {column}"
        for column in missing_columns
    ]


def validate_required_fields(
    dataframe: pd.DataFrame,
    dataset_name: str,
) -> list[str]:
    """Return errors for missing values in critical fields."""
    validate_dataset_name(dataset_name)

    errors: list[str] = []

    for column in REQUIRED_FIELDS[dataset_name]:
        if column not in dataframe.columns:
            continue

        missing_count = int(dataframe[column].isna().sum())

        if missing_count > 0:
            errors.append(
                f"Required field '{column}' contains "
                f"{missing_count:,} missing values."
            )

    return errors


def validate_duplicates(
    dataframe: pd.DataFrame,
    dataset_name: str,
) -> list[str]:
    """Return errors for duplicate records using the dataset key."""
    validate_dataset_name(dataset_name)

    key_columns = KEY_COLUMNS[dataset_name]

    if not all(column in dataframe.columns for column in key_columns):
        return []

    duplicate_count = int(
        dataframe.duplicated(subset=key_columns).sum()
    )

    if duplicate_count == 0:
        return []

    key_name = ", ".join(key_columns)

    return [
        f"Found {duplicate_count:,} duplicate records "
        f"for key: {key_name}."
    ]


def validate_numeric_rules(
    dataframe: pd.DataFrame,
    dataset_name: str,
) -> list[str]:
    """Return errors for invalid numeric business rules."""
    validate_dataset_name(dataset_name)

    errors: list[str] = []

    if dataset_name == "order_items":
        if "price" in dataframe.columns:
            negative_price = int((dataframe["price"] < 0).sum())

            if negative_price > 0:
                errors.append(
                    f"Found {negative_price:,} records with "
                    "negative price."
                )

        if "freight_value" in dataframe.columns:
            negative_freight = int(
                (dataframe["freight_value"] < 0).sum()
            )

            if negative_freight > 0:
                errors.append(
                    f"Found {negative_freight:,} records with "
                    "negative freight value."
                )

    if dataset_name == "order_payments":
        if "payment_value" in dataframe.columns:
            negative_payment = int(
                (dataframe["payment_value"] < 0).sum()
            )

            if negative_payment > 0:
                errors.append(
                    f"Found {negative_payment:,} records with "
                    "negative payment value."
                )

        if "payment_installments" in dataframe.columns:
            negative_installments = int(
                (dataframe["payment_installments"] < 0).sum()
            )

            if negative_installments > 0:
                errors.append(
                    f"Found {negative_installments:,} records with "
                    "negative payment installments."
                )

    return errors


def validate_business_warnings(
    dataframe: pd.DataFrame,
    dataset_name: str,
) -> list[str]:
    """Return warnings for suspicious but allowed source values."""
    validate_dataset_name(dataset_name)

    warnings: list[str] = []

    if (
        dataset_name == "order_payments"
        and "payment_installments" in dataframe.columns
    ):
        zero_installments = int(
            (dataframe["payment_installments"] == 0).sum()
        )

        if zero_installments > 0:
            warnings.append(
                f"Found {zero_installments:,} records with "
                "payment_installments = 0."
            )

    if dataset_name == "orders":
        purchase = pd.to_datetime(
            dataframe["order_purchase_timestamp"],
            errors="coerce",
        )

        carrier = pd.to_datetime(
            dataframe["order_delivered_carrier_date"],
            errors="coerce",
        )

        carrier_before_purchase = (
            carrier.notna()
            & purchase.notna()
            & (carrier < purchase)
        )

        anomaly_count = int(carrier_before_purchase.sum())

        if anomaly_count > 0:
            warnings.append(
                f"Found {anomaly_count:,} records where "
                "carrier date is before purchase date."
            )

    return warnings


def validate_dataset(
    dataframe: pd.DataFrame,
    dataset_name: str,
) -> ValidationResult:
    """Run all initial validation and business-rule checks."""
    validate_dataset_name(dataset_name)

    errors: list[str] = []
    warnings: list[str] = []

    column_errors = validate_columns(dataframe, dataset_name)
    errors.extend(column_errors)

    if not column_errors:
        errors.extend(
            validate_required_fields(dataframe, dataset_name)
        )
        errors.extend(
            validate_duplicates(dataframe, dataset_name)
        )
        errors.extend(
            validate_numeric_rules(dataframe, dataset_name)
        )
        warnings.extend(
            validate_business_warnings(dataframe, dataset_name)
        )

    return ValidationResult(
        dataset_name=dataset_name,
        is_valid=not errors,
        errors=tuple(errors),
        warnings=tuple(warnings),
    )