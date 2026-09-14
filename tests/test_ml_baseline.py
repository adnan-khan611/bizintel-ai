"""Tests for baseline forecasting models."""

import pandas as pd
import pytest

from bizintel.ml.baseline import naive_forecast


def create_monthly_dataset() -> pd.DataFrame:
    """Create a small monthly revenue dataset for testing."""
    return pd.DataFrame(
        {
            "month": pd.period_range(
                start="2024-01",
                periods=4,
                freq="M",
            ),
            "revenue": [1000, 1200, 1500, 1400],
        }
    )


def test_naive_forecast_uses_previous_month_revenue():
    dataset = create_monthly_dataset()

    result = naive_forecast(dataset)

    expected = [None, 1000, 1200, 1500]

    assert result.iloc[0] != result.iloc[0]
    assert result.iloc[1:].tolist() == expected[1:]


def test_naive_forecast_returns_series_with_correct_name():
    dataset = create_monthly_dataset()

    result = naive_forecast(dataset)

    assert isinstance(result, pd.Series)
    assert result.name == "forecast"
    assert len(result) == len(dataset)


def test_naive_forecast_sorts_months_before_forecasting():
    dataset = create_monthly_dataset().sample(
        frac=1,
        random_state=42,
    )

    result = naive_forecast(dataset)

    assert result.iloc[1] == 1000
    assert result.iloc[2] == 1200
    assert result.iloc[3] == 1500


def test_naive_forecast_does_not_modify_input():
    dataset = create_monthly_dataset()
    original = dataset.copy()

    naive_forecast(dataset)

    pd.testing.assert_frame_equal(dataset, original)


def test_missing_month_column_raises_error():
    dataset = create_monthly_dataset().drop(columns=["month"])

    with pytest.raises(
        ValueError,
        match="Missing required columns: month",
    ):
        naive_forecast(dataset)


def test_missing_revenue_column_raises_error():
    dataset = create_monthly_dataset().drop(columns=["revenue"])

    with pytest.raises(
        ValueError,
        match="Missing required columns: revenue",
    ):
        naive_forecast(dataset)