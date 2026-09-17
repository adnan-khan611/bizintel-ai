"""Tests for leakage protection in forecasting features."""

import pandas as pd

from bizintel.ml.features import build_forecasting_features


def make_monthly_dataset() -> pd.DataFrame:
    """Create a deterministic monthly revenue dataset."""
    return pd.DataFrame(
        {
            "month": pd.period_range(
                start="2023-01",
                periods=18,
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
                2200,
                2300,
                2400,
                2500,
                2600,
                2700,
            ],
        }
    )


def test_lag_one_does_not_use_current_revenue() -> None:
    """Lag-1 must always reference the previous month."""
    dataset = make_monthly_dataset()

    result = build_forecasting_features(dataset)

    assert result.loc[5, "revenue_lag_1"] == 1400
    assert result.loc[5, "revenue_lag_1"] != result.loc[5, "revenue"]


def test_lag_two_does_not_use_current_or_next_month() -> None:
    """Lag-2 must reference revenue from two months earlier."""
    dataset = make_monthly_dataset()

    result = build_forecasting_features(dataset)

    assert result.loc[5, "revenue_lag_2"] == 1300
    assert result.loc[5, "revenue_lag_2"] != result.loc[5, "revenue"]
    assert result.loc[5, "revenue_lag_2"] != result.loc[6, "revenue"]


def test_rolling_mean_three_excludes_current_revenue() -> None:
    """Three-month rolling mean must use only previous months."""
    dataset = make_monthly_dataset()

    result = build_forecasting_features(dataset)

    expected_mean = (1200 + 1300 + 1400) / 3

    assert result.loc[5, "revenue_rolling_mean_3"] == expected_mean
    assert result.loc[5, "revenue_rolling_mean_3"] != (
        1300 + 1400 + 1500
    ) / 3


def test_rolling_std_three_excludes_current_revenue() -> None:
    """Three-month rolling std must use only previous months."""
    dataset = make_monthly_dataset()

    result = build_forecasting_features(dataset)

    expected_std = pd.Series(
        [1200, 1300, 1400],
        dtype="float64",
    ).std()

    assert result.loc[5, "revenue_rolling_std_3"] == expected_std


def test_future_revenue_change_does_not_change_past_features() -> None:
    """Changing future revenue must not affect earlier feature values."""
    original_dataset = make_monthly_dataset()
    modified_dataset = original_dataset.copy()

    modified_dataset.loc[17, "revenue"] = 999999

    original_result = build_forecasting_features(original_dataset)
    modified_result = build_forecasting_features(modified_dataset)

    feature_columns = [
        "revenue_lag_1",
        "revenue_lag_2",
        "revenue_lag_3",
        "revenue_lag_6",
        "revenue_lag_12",
        "revenue_rolling_mean_3",
        "revenue_rolling_mean_6",
        "revenue_rolling_std_3",
        "revenue_rolling_std_6",
    ]

    pd.testing.assert_frame_equal(
        original_result.loc[:16, feature_columns],
        modified_result.loc[:16, feature_columns],
    )


def test_future_revenue_does_not_change_current_features() -> None:
    """Future revenue must not influence the current month's features."""
    original_dataset = make_monthly_dataset()
    modified_dataset = original_dataset.copy()

    modified_dataset.loc[17, "revenue"] = 999999

    original_result = build_forecasting_features(original_dataset)
    modified_result = build_forecasting_features(modified_dataset)

    feature_columns = [
        "revenue_lag_1",
        "revenue_lag_2",
        "revenue_lag_3",
        "revenue_lag_6",
        "revenue_lag_12",
        "revenue_rolling_mean_3",
        "revenue_rolling_mean_6",
        "revenue_rolling_std_3",
        "revenue_rolling_std_6",
    ]

    pd.testing.assert_series_equal(
        original_result.loc[16, feature_columns],
        modified_result.loc[16, feature_columns],
    )