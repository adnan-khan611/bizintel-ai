import pandas as pd

from bizintel.data.datetime_utils import parse_datetime_column


def test_valid_datetime_values_are_parsed():
    """Test that valid datetime strings are parsed."""
    series = pd.Series(
        ["2018-01-01 10:30:00", "2018-01-02 12:45:00"]
    )

    result = parse_datetime_column(series)

    assert pd.api.types.is_datetime64_any_dtype(result)
    assert result.notna().all()


def test_invalid_datetime_becomes_nat():
    """Test that invalid datetime values become NaT."""
    series = pd.Series(
        ["2018-01-01 10:30:00", "invalid-date"]
    )

    result = parse_datetime_column(series)

    assert result.notna().sum() == 1
    assert pd.isna(result.iloc[1])


def test_missing_datetime_remains_nat():
    """Test that missing datetime values remain NaT."""
    series = pd.Series(
        ["2018-01-01 10:30:00", None]
    )

    result = parse_datetime_column(series)

    assert result.notna().sum() == 1
    assert pd.isna(result.iloc[1])