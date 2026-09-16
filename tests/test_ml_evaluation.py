"""Tests for forecasting evaluation metrics."""

import pandas as pd
import pytest

from bizintel.ml.evaluation import (
    evaluate_forecast,
    mean_absolute_error,
    root_mean_squared_error,
    symmetric_mean_absolute_percentage_error,
)


def test_mean_absolute_error() -> None:
    """MAE should calculate the average absolute error."""
    actual = pd.Series([100.0, 200.0, 300.0])
    forecast = pd.Series([90.0, 210.0, 330.0])

    result = mean_absolute_error(actual, forecast)

    assert result == pytest.approx(16.6666667)


def test_root_mean_squared_error() -> None:
    """RMSE should calculate the root mean squared error."""
    actual = pd.Series([100.0, 200.0, 300.0])
    forecast = pd.Series([90.0, 210.0, 330.0])

    result = root_mean_squared_error(actual, forecast)

    assert result == pytest.approx(19.1485422)


def test_smape() -> None:
    """sMAPE should calculate symmetric percentage error."""
    actual = pd.Series([100.0, 200.0])
    forecast = pd.Series([90.0, 220.0])

    result = symmetric_mean_absolute_percentage_error(
        actual,
        forecast,
    )

    assert result == pytest.approx(10.0250627)


def test_evaluate_forecast_returns_all_metrics() -> None:
    """Forecast evaluation should return all supported metrics."""
    actual = pd.Series([100.0, 200.0, 300.0])
    forecast = pd.Series([90.0, 210.0, 330.0])

    result = evaluate_forecast(actual, forecast)

    assert set(result) == {"mae", "rmse", "smape"}

    assert result["mae"] == pytest.approx(16.6666667)
    assert result["rmse"] == pytest.approx(19.1485422)
    assert result["smape"] == pytest.approx(8.3093914)


def test_evaluation_rejects_non_series_actual() -> None:
    """Evaluation should require pandas Series inputs."""
    forecast = pd.Series([100.0, 200.0])

    with pytest.raises(TypeError, match="actual must be a pandas Series"):
        mean_absolute_error([100.0, 200.0], forecast)


def test_evaluation_rejects_non_series_forecast() -> None:
    """Evaluation should require a pandas Series forecast."""
    actual = pd.Series([100.0, 200.0])

    with pytest.raises(
        TypeError,
        match="forecast must be a pandas Series",
    ):
        mean_absolute_error(actual, [100.0, 200.0])


def test_evaluation_rejects_different_lengths() -> None:
    """Evaluation should reject inputs with different lengths."""
    actual = pd.Series([100.0, 200.0])
    forecast = pd.Series([100.0])

    with pytest.raises(
        ValueError,
        match="actual and forecast must have the same length",
    ):
        mean_absolute_error(actual, forecast)


def test_evaluation_rejects_empty_series() -> None:
    """Evaluation should reject empty inputs."""
    actual = pd.Series(dtype=float)
    forecast = pd.Series(dtype=float)

    with pytest.raises(
        ValueError,
        match="actual and forecast must not be empty",
    ):
        mean_absolute_error(actual, forecast)


def test_evaluation_rejects_non_finite_values() -> None:
    """Evaluation should reject NaN and infinite values."""
    actual = pd.Series([100.0, float("nan")])
    forecast = pd.Series([100.0, 110.0])

    with pytest.raises(
        ValueError,
        match="actual contains non-finite values",
    ):
        mean_absolute_error(actual, forecast)


def test_smape_handles_both_zero_values() -> None:
    """sMAPE should return zero when both values are zero."""
    actual = pd.Series([0.0, 100.0])
    forecast = pd.Series([0.0, 100.0])

    result = symmetric_mean_absolute_percentage_error(
        actual,
        forecast,
    )

    assert result == 0.0