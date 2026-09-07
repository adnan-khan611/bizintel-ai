import pandas as pd
import pytest

from bizintel.data.money import convert_to_minor_units


def test_decimal_money_is_converted_to_minor_units():
    """Test conversion of decimal monetary values."""
    series = pd.Series([10.50, 25.00, 0.85])

    result = convert_to_minor_units(series)

    assert result.tolist() == [1050, 2500, 85]
    assert result.dtype == "int64"


def test_zero_money_is_converted_correctly():
    """Test that zero remains zero."""
    series = pd.Series([0.0])

    result = convert_to_minor_units(series)

    assert result.tolist() == [0]


def test_missing_money_becomes_zero():
    """Test handling of missing monetary values."""
    series = pd.Series([10.50, None])

    result = convert_to_minor_units(series)

    assert result.tolist() == [1050, 0]


def test_invalid_money_value_raises_error():
    """Test that invalid monetary values raise an error."""
    series = pd.Series(["10.50", "invalid"])

    with pytest.raises(
        ValueError,
        match="Invalid monetary value",
    ):
        convert_to_minor_units(series)