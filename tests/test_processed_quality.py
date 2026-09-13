import pandas as pd
from scripts.validate_processed_quality import (
    validate_composite_key,
    validate_dataset,
    validate_non_negative,
    validate_primary_key,
    validate_required_fields,
)


def test_valid_primary_key():
    dataframe = pd.DataFrame(
        {
            "customer_id": ["C1", "C2", "C3"],
        }
    )

    errors = validate_primary_key(
        dataframe,
        "customer_id",
        "customers",
    )

    assert errors == []


def test_duplicate_primary_key_is_detected():
    dataframe = pd.DataFrame(
        {
            "customer_id": ["C1", "C1", "C2"],
        }
    )

    errors = validate_primary_key(
        dataframe,
        "customer_id",
        "customers",
    )

    assert len(errors) == 1
    assert "duplicate" in errors[0].lower()


def test_null_required_field_is_detected():
    dataframe = pd.DataFrame(
        {
            "customer_id": ["C1", None, "C3"],
        }
    )

    errors = validate_required_fields(
        dataframe,
        ["customer_id"],
        "customers",
    )

    assert len(errors) == 1
    assert "null" in errors[0].lower()


def test_duplicate_composite_key_is_detected():
    dataframe = pd.DataFrame(
        {
            "order_id": ["O1", "O1", "O2"],
            "order_item_id": [1, 1, 1],
        }
    )

    errors = validate_composite_key(
        dataframe,
        ["order_id", "order_item_id"],
        "order_items",
    )

    assert len(errors) == 1
    assert "duplicate" in errors[0].lower()


def test_negative_value_is_detected():
    dataframe = pd.DataFrame(
        {
            "price_minor": [1000, -500, 2500],
        }
    )

    errors = validate_non_negative(
        dataframe,
        ["price_minor"],
        "order_items",
    )

    assert len(errors) == 1
    assert "negative" in errors[0].lower()


def test_valid_order_items_dataset():
    dataframe = pd.DataFrame(
        {
            "order_id": ["O1", "O2"],
            "order_item_id": [1, 1],
            "product_id": ["P1", "P2"],
            "price_minor": [1000, 2500],
            "freight_value_minor": [100, 200],
        }
    )

    errors = validate_dataset(
        "order_items",
        dataframe,
    )

    assert errors == []