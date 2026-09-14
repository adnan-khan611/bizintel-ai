"""Baseline forecasting models for BizIntel AI."""

import pandas as pd


def naive_forecast(monthly_dataset: pd.DataFrame) -> pd.Series:
    """Forecast each month using the previous month's revenue."""
    required_columns = {"month", "revenue"}
    missing_columns = required_columns - set(monthly_dataset.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    data = monthly_dataset[["month", "revenue"]].copy()
    data = data.sort_values("month").reset_index(drop=True)

    return data["revenue"].shift(1).rename("forecast")