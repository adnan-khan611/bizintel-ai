import pandas as pd
import pytest

from bizintel.data.type_validation import validate_column_types


def test_valid_string_type():
    """Test that string-like columns pass."""
    dataframe = pd.DataFrame(
        {"customer_id": ["C001", "C002"]}
    )

    result = validate_column_types(
        dataframe,
        {"customer_id": "string"},
    )

    assert result.is_valid is True
    assert result.errors == ()


def test_valid_integer_type():
    """Test that integer columns pass."""
    dataframe = pd.DataFrame(
        {"order_item_id": [1, 2, 3]}
    )

    result = validate_column_types(
        dataframe,
        {"order_item_id": "integer"},
    )

    assert result.is_valid is True


def test_valid_float_type():
    """Test that float columns pass."""
    dataframe = pd.DataFrame(
        {"price": [10.5, 20.0]}
    )

    result = validate_column_types(
        dataframe,
        {"price": "float"},
    )

    assert result.is_valid is True


def test_valid_datetime_type():
    """Test that datetime columns pass."""
    dataframe = pd.DataFrame(
        {
            "order_date": pd.to_datetime(
                ["2018-01-01", "2018-01-02"]
            )
        }
    )

    result = validate_column_types(
        dataframe,
        {"order_date": "datetime"},
    )

    assert result.is_valid is True


def test_invalid_type_is_detected():
    """Test that an unexpected type is detected."""
    dataframe = pd.DataFrame(
        {"price": ["10.5", "20.0"]}
    )

    result = validate_column_types(
        dataframe,
        {"price": "float"},
    )

    assert result.is_valid is False
    assert len(result.errors) == 1


def test_missing_column_is_detected():
    """Test that a missing column is detected."""
    dataframe = pd.DataFrame(
        {"customer_id": ["C001"]}
    )

    result = validate_column_types(
        dataframe,
        {"order_id": "string"},
    )

    assert result.is_valid is False
    assert "Column not found: order_id" in result.errors


def test_unsupported_expected_type_raises_error():
    """Test that unsupported types raise an error."""
    dataframe = pd.DataFrame(
        {"customer_id": ["C001"]}
    )

    with pytest.raises(
        ValueError,
        match="Unsupported expected type",
    ):
        validate_column_types(
            dataframe,
            {"customer_id": "decimal"},
        )