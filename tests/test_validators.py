import pandas as pd
import pytest

from bizintel.data.validators import validate_dataset


def test_valid_customers_dataset():
    """Test that a valid customers dataset passes validation."""
    dataframe = pd.DataFrame(
        {
            "customer_id": ["C001", "C002"],
            "customer_unique_id": ["U001", "U002"],
            "customer_zip_code_prefix": [1000, 2000],
            "customer_city": ["City A", "City B"],
            "customer_state": ["SP", "RJ"],
        }
    )

    result = validate_dataset(dataframe, "customers")

    assert result.is_valid is True
    assert result.errors == ()


def test_missing_required_column():
    """Test that a missing required column is detected."""
    dataframe = pd.DataFrame(
        {
            "customer_id": ["C001"],
            "customer_unique_id": ["U001"],
            "customer_zip_code_prefix": [1000],
            "customer_city": ["City A"],
        }
    )

    result = validate_dataset(dataframe, "customers")

    assert result.is_valid is False
    assert "Missing required column: customer_state" in result.errors


def test_missing_required_field():
    """Test that missing values in critical fields are detected."""
    dataframe = pd.DataFrame(
        {
            "customer_id": ["C001", None],
            "customer_unique_id": ["U001", "U002"],
            "customer_zip_code_prefix": [1000, 2000],
            "customer_city": ["City A", "City B"],
            "customer_state": ["SP", "RJ"],
        }
    )

    result = validate_dataset(dataframe, "customers")

    assert result.is_valid is False
    assert any(
        "Required field 'customer_id' contains 1 missing values."
        in error
        for error in result.errors
    )


def test_duplicate_business_key():
    """Test that duplicate customer IDs are detected."""
    dataframe = pd.DataFrame(
        {
            "customer_id": ["C001", "C001"],
            "customer_unique_id": ["U001", "U002"],
            "customer_zip_code_prefix": [1000, 2000],
            "customer_city": ["City A", "City B"],
            "customer_state": ["SP", "RJ"],
        }
    )

    result = validate_dataset(dataframe, "customers")

    assert result.is_valid is False
    assert any(
        "duplicate records for key: customer_id" in error
        for error in result.errors
    )


def test_unsupported_dataset():
    """Test that unsupported dataset names raise an error."""
    dataframe = pd.DataFrame({"id": [1]})

    with pytest.raises(ValueError, match="Unsupported dataset"):
        validate_dataset(dataframe, "unknown_dataset")


def test_negative_price_is_error():
    """Test that negative product price is rejected."""
    dataframe = pd.DataFrame(
        {
            "order_id": ["O001"],
            "order_item_id": [1],
            "product_id": ["P001"],
            "seller_id": ["S001"],
            "shipping_limit_date": ["2018-01-01"],
            "price": [-10.0],
            "freight_value": [5.0],
        }
    )

    result = validate_dataset(dataframe, "order_items")

    assert result.is_valid is False
    assert "negative price" in result.errors[0]


def test_negative_freight_value_is_error():
    """Test that negative freight value is rejected."""
    dataframe = pd.DataFrame(
        {
            "order_id": ["O001"],
            "order_item_id": [1],
            "product_id": ["P001"],
            "seller_id": ["S001"],
            "shipping_limit_date": ["2018-01-01"],
            "price": [100.0],
            "freight_value": [-5.0],
        }
    )

    result = validate_dataset(dataframe, "order_items")

    assert result.is_valid is False
    assert "negative freight value" in result.errors[0]


def test_negative_payment_value_is_error():
    """Test that negative payment value is rejected."""
    dataframe = pd.DataFrame(
        {
            "order_id": ["O001"],
            "payment_sequential": [1],
            "payment_type": ["credit_card"],
            "payment_installments": [1],
            "payment_value": [-50.0],
        }
    )

    result = validate_dataset(dataframe, "order_payments")

    assert result.is_valid is False
    assert "negative payment value" in result.errors[0]


def test_negative_payment_installments_is_error():
    """Test that negative installments are rejected."""
    dataframe = pd.DataFrame(
        {
            "order_id": ["O001"],
            "payment_sequential": [1],
            "payment_type": ["credit_card"],
            "payment_installments": [-1],
            "payment_value": [100.0],
        }
    )

    result = validate_dataset(dataframe, "order_payments")

    assert result.is_valid is False
    assert "negative payment installments" in result.errors[0]


def test_zero_payment_installments_is_warning():
    """Test that zero installments produce a warning, not an error."""
    dataframe = pd.DataFrame(
        {
            "order_id": ["O001"],
            "payment_sequential": [1],
            "payment_type": ["credit_card"],
            "payment_installments": [0],
            "payment_value": [100.0],
        }
    )

    result = validate_dataset(dataframe, "order_payments")

    assert result.is_valid is True
    assert result.errors == ()
    assert any(
        "payment_installments = 0" in warning
        for warning in result.warnings
    )


def test_carrier_before_purchase_is_warning():
    """Test that carrier date before purchase produces a warning."""
    dataframe = pd.DataFrame(
        {
            "order_id": ["O001"],
            "customer_id": ["C001"],
            "order_status": ["shipped"],
            "order_purchase_timestamp": ["2018-01-02 10:00:00"],
            "order_approved_at": ["2018-01-02 11:00:00"],
            "order_delivered_carrier_date": ["2018-01-02 09:00:00"],
            "order_delivered_customer_date": [None],
            "order_estimated_delivery_date": ["2018-01-10"],
        }
    )

    result = validate_dataset(dataframe, "orders")

    assert result.is_valid is True
    assert result.errors == ()
    assert any(
        "carrier date is before purchase date" in warning
        for warning in result.warnings
    )