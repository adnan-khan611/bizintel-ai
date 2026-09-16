"""Evaluation metrics for BizIntel AI forecasting models."""

import numpy as np
import pandas as pd


def mean_absolute_error(
    actual: pd.Series,
    forecast: pd.Series,
) -> float:
    """Calculate mean absolute error."""
    actual_values, forecast_values = _validate_inputs(actual, forecast)

    return float(np.mean(np.abs(actual_values - forecast_values)))


def root_mean_squared_error(
    actual: pd.Series,
    forecast: pd.Series,
) -> float:
    """Calculate root mean squared error."""
    actual_values, forecast_values = _validate_inputs(actual, forecast)

    return float(
        np.sqrt(np.mean((actual_values - forecast_values) ** 2))
    )


def symmetric_mean_absolute_percentage_error(
    actual: pd.Series,
    forecast: pd.Series,
) -> float:
    """Calculate symmetric mean absolute percentage error."""
    actual_values, forecast_values = _validate_inputs(actual, forecast)

    denominator = np.abs(actual_values) + np.abs(forecast_values)

    valid = denominator != 0

    if not np.any(valid):
        return 0.0

    percentage_error = (
        2
        * np.abs(actual_values[valid] - forecast_values[valid])
        / denominator[valid]
    )

    return float(np.mean(percentage_error) * 100)


def evaluate_forecast(
    actual: pd.Series,
    forecast: pd.Series,
) -> dict[str, float]:
    """Calculate all supported forecasting metrics."""
    return {
        "mae": mean_absolute_error(actual, forecast),
        "rmse": root_mean_squared_error(actual, forecast),
        "smape": symmetric_mean_absolute_percentage_error(
            actual,
            forecast,
        ),
    }


def _validate_inputs(
    actual: pd.Series,
    forecast: pd.Series,
) -> tuple[np.ndarray, np.ndarray]:
    """Validate and convert actual and forecast values."""
    if not isinstance(actual, pd.Series):
        raise TypeError("actual must be a pandas Series")

    if not isinstance(forecast, pd.Series):
        raise TypeError("forecast must be a pandas Series")

    if len(actual) != len(forecast):
        raise ValueError("actual and forecast must have the same length")

    if len(actual) == 0:
        raise ValueError("actual and forecast must not be empty")

    actual_values = actual.to_numpy(dtype=float)
    forecast_values = forecast.to_numpy(dtype=float)

    if not np.isfinite(actual_values).all():
        raise ValueError("actual contains non-finite values")

    if not np.isfinite(forecast_values).all():
        raise ValueError("forecast contains non-finite values")

    return actual_values, forecast_values