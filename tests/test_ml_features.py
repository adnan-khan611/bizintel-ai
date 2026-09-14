"""Tests for forecasting feature engineering."""

import pandas as pd
import pytest

from bizintel.ml.features import build_forecasting_features


def create_monthly_dataset() -> pd.DataFrame:
    """Create a small monthly revenue dataset for testing."""
    return pd.DataFrame(
        {
            "month": pd.period_range(
                start="2023-01",
                periods=12,
                freq="M",
            ),
            "revenue": [
                1000,
                1100,
                1200,
                1300,
                1400,
                1500,
                1600,
                1700,
                1800,
                1900,
                2000,
                2100,
            ],
        }
    )


def test_build_forecasting_features_creates_expected_columns():
    dataset = create_monthly_dataset()

    result = build_forecasting_features(dataset)

    expected_columns = [
        "month",
        "revenue",
        "revenue_lag_1",
        "revenue_lag_2",
        "revenue_lag_3",
        "revenue_lag_6",
        "revenue_lag_12",
        "revenue_rolling_mean_3",
        "revenue_rolling_mean_6",
        "revenue_rolling_std_3",
        "revenue_rolling_std_6",
        "month_number",
        "quarter",
        "year",
    ]

    assert result.columns.tolist() == expected_columns


def test_lag_features_use_only_previous_revenue():
    dataset = create_monthly_dataset()

    result = build_forecasting_features(dataset)

    assert pd.isna(result.loc[0, "revenue_lag_1"])
    assert result.loc[1, "revenue_lag_1"] == 1000
    assert result.loc[2, "revenue_lag_2"] == 1000
    assert result.loc[3, "revenue_lag_3"] == 1000
    assert result.loc[6, "revenue_lag_6"] == 1000


def test_twelve_month_lag_is_created_correctly():
    dataset = create_monthly_dataset()

    extra_month = pd.DataFrame(
        {
            "month": [pd.Period("2024-01", freq="M")],
            "revenue": [2200],
        }
    )

    dataset = pd.concat(
        [dataset, extra_month],
        ignore_index=True,
    )

    result = build_forecasting_features(dataset)

    assert result.loc[12, "revenue_lag_12"] == 1000


def test_rolling_features_use_previous_months_only():
    dataset = create_monthly_dataset()

    result = build_forecasting_features(dataset)

    assert pd.isna(result.loc[0, "revenue_rolling_mean_3"])
    assert pd.isna(result.loc[1, "revenue_rolling_mean_3"])
    assert pd.isna(result.loc[2, "revenue_rolling_mean_3"])
    assert result.loc[3, "revenue_rolling_mean_3"] == 1100

    assert pd.isna(result.loc[0, "revenue_rolling_mean_6"])
    assert result.loc[6, "revenue_rolling_mean_6"] == 1250


def test_calendar_features_are_correct():
    dataset = create_monthly_dataset()

    result = build_forecasting_features(dataset)

    assert result.loc[0, "month_number"] == 1
    assert result.loc[2, "month_number"] == 3
    assert result.loc[0, "quarter"] == 1
    assert result.loc[3, "quarter"] == 2
    assert result.loc[0, "year"] == 2023
    assert result.loc[11, "year"] == 2023


def test_input_is_sorted_by_month():
    dataset = create_monthly_dataset().sample(
        frac=1,
        random_state=42,
    )

    result = build_forecasting_features(dataset)

    assert result["month"].is_monotonic_increasing


def test_original_dataset_is_not_modified():
    dataset = create_monthly_dataset()
    original = dataset.copy()

    build_forecasting_features(dataset)

    pd.testing.assert_frame_equal(dataset, original)


def test_missing_required_column_raises_error():
    dataset = create_monthly_dataset().drop(columns=["revenue"])

    with pytest.raises(
        ValueError,
        match="Missing required columns: revenue",
    ):
        build_forecasting_features(dataset)


def test_invalid_month_type_raises_error():
    dataset = create_monthly_dataset()
    dataset["month"] = dataset["month"].astype(str)

    with pytest.raises(
        TypeError,
        match="month must contain pandas Period values",
    ):
        build_forecasting_features(dataset)


def test_invalid_revenue_type_raises_error():
    dataset = create_monthly_dataset()
    dataset["revenue"] = dataset["revenue"].astype(str)

    with pytest.raises(
        TypeError,
        match="revenue must be numeric",
    ):
        build_forecasting_features(dataset)