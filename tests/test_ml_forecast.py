"""Tests for forecast generation utilities."""

import pandas as pd
import pytest

from bizintel.ml.features import FEATURE_COLUMNS
from bizintel.ml.forecast import generate_next_month_ridge_forecast


def make_forecasting_dataset() -> pd.DataFrame:
    """Create a complete synthetic forecasting dataset."""
    months = pd.period_range(
        start="2018-01",
        periods=15,
        freq="M",
    )

    rows = []

    for index, month in enumerate(months):
        row = {
            "month": month,
            "revenue": float((index + 1) * 1000),
        }

        for feature_index, feature in enumerate(FEATURE_COLUMNS):
            row[feature] = float(index + feature_index + 1)

        rows.append(row)

    return pd.DataFrame(rows)


def test_generate_next_month_forecast_returns_dataframe() -> None:
    """Forecast generation should return a DataFrame."""
    dataset = make_forecasting_dataset()

    result = generate_next_month_ridge_forecast(dataset)

    assert isinstance(result, pd.DataFrame)


def test_generate_next_month_forecast_returns_expected_columns() -> None:
    """Forecast output should contain month and revenue columns."""
    dataset = make_forecasting_dataset()

    result = generate_next_month_ridge_forecast(dataset)

    assert list(result.columns) == [
        "forecast_month",
        "forecast_revenue",
    ]


def test_generate_next_month_forecast_returns_one_row() -> None:
    """Forecast output should contain exactly one future month."""
    dataset = make_forecasting_dataset()

    result = generate_next_month_ridge_forecast(dataset)

    assert len(result) == 1


def test_generate_next_month_forecast_uses_next_month() -> None:
    """Forecast month should be immediately after the last month."""
    dataset = make_forecasting_dataset()

    result = generate_next_month_ridge_forecast(dataset)

    assert result["forecast_month"].iloc[0] == pd.Period(
        "2019-04",
        freq="M",
    )


def test_generate_next_month_forecast_is_numeric() -> None:
    """Forecast revenue should be numeric and non-missing."""
    dataset = make_forecasting_dataset()

    result = generate_next_month_ridge_forecast(dataset)

    assert pd.api.types.is_numeric_dtype(
        result["forecast_revenue"]
    )
    assert result["forecast_revenue"].notna().all()


def test_generate_next_month_forecast_rejects_empty_dataset() -> None:
    """Forecast generation should reject an empty dataset."""
    dataset = pd.DataFrame(
        {
            "month": pd.PeriodIndex([], freq="M"),
            "revenue": pd.Series(dtype=float),
        }
    )

    with pytest.raises(
        ValueError,
        match="forecasting_dataset must not be empty",
    ):
        generate_next_month_ridge_forecast(dataset)


def test_generate_next_month_forecast_rejects_missing_columns() -> None:
    """Forecast generation should reject missing required columns."""
    dataset = make_forecasting_dataset().drop(
        columns=["revenue"]
    )

    with pytest.raises(
        ValueError,
        match="Missing required columns",
    ):
        generate_next_month_ridge_forecast(dataset)


def test_generate_next_month_forecast_rejects_duplicate_months() -> None:
    """Forecast generation should reject duplicate months."""
    dataset = make_forecasting_dataset()

    dataset.loc[1, "month"] = dataset.loc[0, "month"]

    with pytest.raises(
        ValueError,
        match="month values must be unique",
    ):
        generate_next_month_ridge_forecast(dataset)