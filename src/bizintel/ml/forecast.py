"""Forecast generation utilities for BizIntel AI."""

import pandas as pd

from bizintel.ml.model import predict_ridge_model, train_ridge_model


def generate_next_month_ridge_forecast(
    forecasting_dataset: pd.DataFrame,
) -> pd.DataFrame:
    """Generate a Ridge forecast for the month after the dataset."""
    required_columns = {"month", "revenue"}

    missing_columns = required_columns - set(forecasting_dataset.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    if forecasting_dataset.empty:
        raise ValueError("forecasting_dataset must not be empty")

    if forecasting_dataset["month"].duplicated().any():
        raise ValueError("month values must be unique")

    data = (
        forecasting_dataset
        .sort_values("month")
        .reset_index(drop=True)
        .copy()
    )

    model = train_ridge_model(data)

    last_row = data.iloc[[-1]].copy()
    last_month = last_row["month"].iloc[0]

    forecast_month = last_month + 1

    forecast = predict_ridge_model(
        model,
        last_row,
    )

    forecast_value = float(forecast.iloc[0])

    return pd.DataFrame(
        {
            "forecast_month": pd.PeriodIndex(
                [forecast_month],
                freq="M",
            ),
            "forecast_revenue": [forecast_value],
        }
    )