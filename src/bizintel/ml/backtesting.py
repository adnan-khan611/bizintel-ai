"""Backtesting utilities for BizIntel AI forecasting models."""

import pandas as pd

from bizintel.ml.evaluation import evaluate_forecast
from bizintel.ml.model import predict_ridge_model, train_ridge_model

REQUIRED_COLUMNS = {
    "month",
    "revenue",
}


def run_expanding_window_backtest(
    forecasting_dataset: pd.DataFrame,
    min_train_size: int = 7,
) -> tuple[pd.DataFrame, dict[str, dict[str, float]]]:
    """Run one-step-ahead expanding-window backtesting.

    Each fold trains the Ridge model on all observations available before
    the validation month and evaluates the following month. The naive
    baseline uses the last observed training revenue.
    """
    missing_columns = REQUIRED_COLUMNS - set(forecasting_dataset.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    if min_train_size < 1:
        raise ValueError("min_train_size must be greater than 0")

    data = (
        forecasting_dataset
        .sort_values("month")
        .reset_index(drop=True)
        .copy()
    )

    if len(data) <= min_train_size:
        raise ValueError(
            "Not enough observations for backtesting"
        )

    if data["month"].duplicated().any():
        raise ValueError("month values must be unique")

    if data["revenue"].isna().any():
        raise ValueError("revenue contains missing values")

    feature_columns = [
        column
        for column in data.columns
        if column not in {"month", "revenue"}
    ]

    if not feature_columns:
        raise ValueError("No forecasting features available")

    if data[feature_columns].isna().any().any():
        raise ValueError("Forecasting features contain missing values")

    fold_results = []

    for validation_index in range(
        min_train_size,
        len(data),
    ):
        train_dataset = data.iloc[:validation_index].copy()
        validation_dataset = data.iloc[
            validation_index : validation_index + 1
        ].copy()

        actual = validation_dataset["revenue"]

        naive_prediction = pd.Series(
            [train_dataset["revenue"].iloc[-1]],
            index=actual.index,
            name="forecast",
            dtype=float,
        )

        model = train_ridge_model(train_dataset)

        ridge_prediction = predict_ridge_model(
            model,
            validation_dataset,
        )

        fold_results.append(
            {
                "fold": len(fold_results) + 1,
                "train_size": len(train_dataset),
                "train_end": train_dataset["month"].iloc[-1],
                "validation_month": validation_dataset["month"].iloc[0],
                "actual": float(actual.iloc[0]),
                "naive_forecast": float(naive_prediction.iloc[0]),
                "ridge_forecast": float(ridge_prediction.iloc[0]),
            }
        )

    results = pd.DataFrame(fold_results)

    naive_metrics = evaluate_forecast(
        results["actual"],
        results["naive_forecast"],
    )

    ridge_metrics = evaluate_forecast(
        results["actual"],
        results["ridge_forecast"],
    )

    metrics = {
        "naive": naive_metrics,
        "ridge": ridge_metrics,
    }

    return results, metrics