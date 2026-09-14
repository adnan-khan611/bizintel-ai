"""Feature engineering utilities for BizIntel AI forecasting."""

import pandas as pd

FEATURE_COLUMNS = [
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


def build_forecasting_features(
    monthly_dataset: pd.DataFrame,
) -> pd.DataFrame:
    """Build time-series features from monthly revenue data."""
    required_columns = {"month", "revenue"}
    missing_columns = required_columns - set(monthly_dataset.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    if not isinstance(monthly_dataset["month"].dtype, pd.PeriodDtype):
        raise TypeError("month must contain pandas Period values")

    if not pd.api.types.is_numeric_dtype(monthly_dataset["revenue"]):
        raise TypeError("revenue must be numeric")

    data = monthly_dataset[["month", "revenue"]].copy()
    data = data.sort_values("month").reset_index(drop=True)

    data["revenue_lag_1"] = data["revenue"].shift(1)
    data["revenue_lag_2"] = data["revenue"].shift(2)
    data["revenue_lag_3"] = data["revenue"].shift(3)
    data["revenue_lag_6"] = data["revenue"].shift(6)
    data["revenue_lag_12"] = data["revenue"].shift(12)

    data["revenue_rolling_mean_3"] = (
        data["revenue"].shift(1).rolling(window=3).mean()
    )
    data["revenue_rolling_mean_6"] = (
        data["revenue"].shift(1).rolling(window=6).mean()
    )

    data["revenue_rolling_std_3"] = (
        data["revenue"].shift(1).rolling(window=3).std()
    )
    data["revenue_rolling_std_6"] = (
        data["revenue"].shift(1).rolling(window=6).std()
    )

    data["month_number"] = data["month"].dt.month.astype("int64")
    data["quarter"] = data["month"].dt.quarter.astype("int64")
    data["year"] = data["month"].dt.year.astype("int64")

    return data