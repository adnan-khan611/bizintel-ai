import pandas as pd
import pytest

from bizintel.data.standardize_dates import (
    standardize_datetime_column,
)


def test_datetime_column_is_standardized():
    """Test that valid dates are converted to datetime."""
    dataframe = pd.DataFrame(
        {
            "order_date": [
                "2018-01-01 10:30:00",
                "2018-01-02 12:45:00",
            ]
        }
    )

    result = standardize_datetime_column(
        dataframe,
        "order_date",
    )

    assert pd.api.types.is_datetime64_any_dtype(
        result.dataframe["order_date"]
    )
    assert result.invalid_count == 0


def test_invalid_date_is_reported():
    """Test that invalid dates are counted."""
    dataframe = pd.DataFrame(
        {
            "order_date": [
                "2018-01-01 10:30:00",
                "invalid-date",
            ]
        }
    )

    result = standardize_datetime_column(
        dataframe,
        "order_date",
    )

    assert result.invalid_count == 1
    assert result.dataframe["order_date"].notna().sum() == 1


def test_existing_missing_date_is_not_invalid():
    """Test that existing missing dates are not counted as invalid."""
    dataframe = pd.DataFrame(
        {
            "order_date": [
                "2018-01-01 10:30:00",
                None,
            ]
        }
    )

    result = standardize_datetime_column(
        dataframe,
        "order_date",
    )

    assert result.invalid_count == 0
    assert pd.isna(result.dataframe["order_date"].iloc[1])


def test_missing_column_raises_error():
    """Test that a missing column raises an error."""
    dataframe = pd.DataFrame(
        {"wrong_column": ["2018-01-01"]}
    )

    with pytest.raises(
        ValueError,
        match="Column not found",
    ):
        standardize_datetime_column(
            dataframe,
            "order_date",
        )