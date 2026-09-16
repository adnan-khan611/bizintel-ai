"""Tests for forecasting backtesting utilities."""

import pandas as pd
import pytest

from bizintel.ml.backtesting import run_expanding_window_backtest
from bizintel.ml.features import FEATURE_COLUMNS


def make_forecasting_dataset() -> pd.DataFrame:
    """Create a complete synthetic forecasting dataset."""
    months = pd.period_range(
        start="2018-01",
        periods=10,
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


def test_backtest_returns_fold_results() -> None:
    """Backtesting should return one result per validation fold."""
    dataset = make_forecasting_dataset()

    results, metrics = run_expanding_window_backtest(
        dataset,
        min_train_size=6,
    )

    assert len(results) == 4
    assert list(results["fold"]) == [1, 2, 3, 4]
    assert list(results["train_size"]) == [6, 7, 8, 9]


def test_backtest_uses_chronological_validation_months() -> None:
    """Validation months should follow chronological order."""
    dataset = make_forecasting_dataset()

    results, _ = run_expanding_window_backtest(
        dataset,
        min_train_size=6,
    )

    expected_months = pd.period_range(
        start="2018-07",
        periods=4,
        freq="M",
    )

    assert results["validation_month"].tolist() == (
        expected_months.tolist()
    )


def test_backtest_naive_forecast_uses_last_training_revenue() -> None:
    """Naive forecasts should use the latest training revenue."""
    dataset = make_forecasting_dataset()

    results, _ = run_expanding_window_backtest(
        dataset,
        min_train_size=6,
    )

    assert results["naive_forecast"].tolist() == [
        6000.0,
        7000.0,
        8000.0,
        9000.0,
    ]


def test_backtest_returns_model_metrics() -> None:
    """Backtesting should return metrics for both models."""
    dataset = make_forecasting_dataset()

    _, metrics = run_expanding_window_backtest(
        dataset,
        min_train_size=6,
    )

    assert set(metrics) == {"naive", "ridge"}

    for model_metrics in metrics.values():
        assert set(model_metrics) == {"mae", "rmse", "smape"}

        for value in model_metrics.values():
            assert value >= 0


def test_backtest_predictions_contain_no_missing_values() -> None:
    """Backtesting predictions should contain no missing values."""
    dataset = make_forecasting_dataset()

    results, _ = run_expanding_window_backtest(
        dataset,
        min_train_size=6,
    )

    assert results["actual"].notna().all()
    assert results["naive_forecast"].notna().all()
    assert results["ridge_forecast"].notna().all()


def test_backtest_rejects_missing_columns() -> None:
    """Backtesting should reject datasets missing required columns."""
    dataset = make_forecasting_dataset().drop(columns=["month"])

    with pytest.raises(
        ValueError,
        match="Missing required columns",
    ):
        run_expanding_window_backtest(dataset)


def test_backtest_rejects_invalid_train_size() -> None:
    """Backtesting should reject non-positive training size."""
    dataset = make_forecasting_dataset()

    with pytest.raises(
        ValueError,
        match="min_train_size must be greater than 0",
    ):
        run_expanding_window_backtest(
            dataset,
            min_train_size=0,
        )


def test_backtest_rejects_insufficient_observations() -> None:
    """Backtesting should require observations after the training window."""
    dataset = make_forecasting_dataset()

    with pytest.raises(
        ValueError,
        match="Not enough observations for backtesting",
    ):
        run_expanding_window_backtest(
            dataset,
            min_train_size=len(dataset),
        )


def test_backtest_rejects_duplicate_months() -> None:
    """Backtesting should reject duplicate months."""
    dataset = make_forecasting_dataset()
    dataset.loc[1, "month"] = dataset.loc[0, "month"]

    with pytest.raises(
        ValueError,
        match="month values must be unique",
    ):
        run_expanding_window_backtest(dataset)


def test_backtest_does_not_modify_input() -> None:
    """Backtesting should not modify the original dataset."""
    dataset = make_forecasting_dataset()
    original = dataset.copy(deep=True)

    run_expanding_window_backtest(
        dataset,
        min_train_size=6,
    )

    pd.testing.assert_frame_equal(dataset, original)