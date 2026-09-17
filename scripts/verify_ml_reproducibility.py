"""Verify forecasting model reproducibility on the Olist dataset."""

from pathlib import Path

import numpy as np
import pandas as pd

from bizintel.ml.dataset import build_monthly_revenue_dataset
from bizintel.ml.features import (
    FEATURE_COLUMNS,
    build_forecasting_features,
)
from bizintel.ml.training import train_forecasting_model

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ORDERS_PATH = PROJECT_ROOT / "data" / "raw" / "olist_orders_dataset.csv"
ORDER_ITEMS_PATH = (
    PROJECT_ROOT / "data" / "raw" / "olist_order_items_dataset.csv"
)


def main() -> None:
    """Verify deterministic model training on the real Olist dataset."""
    print("Loading Olist data...")

    orders = pd.read_csv(
        ORDERS_PATH,
        parse_dates=["order_purchase_timestamp"],
    )

    order_items = pd.read_csv(ORDER_ITEMS_PATH)

    order_items["price_minor"] = (
        order_items["price"].mul(100).round().astype("int64")
    )

    orders = orders.rename(
        columns={"order_purchase_timestamp": "order_date"}
    )

    monthly_dataset = build_monthly_revenue_dataset(
    orders,
    order_items,
    include_partial_months=True,
    start_month="2016-10",
    end_month="2018-08",
    )

    print(f"Monthly observations: {len(monthly_dataset)}")
    print(f"Training window: {monthly_dataset['month'].min()}")
    print(f"Training window: {monthly_dataset['month'].max()}")

    forecasting_dataset = build_forecasting_features(
        monthly_dataset
    )

    complete_dataset = forecasting_dataset.dropna(
        subset=FEATURE_COLUMNS + ["revenue"]
    ).reset_index(drop=True)

    print(f"Complete training rows: {len(complete_dataset)}")

    print("Training model one...")
    model_one = train_forecasting_model(
        monthly_dataset,
        alpha=1.0,
        min_training_rows=1,
    )

    print("Training model two...")
    model_two = train_forecasting_model(
        monthly_dataset,
        alpha=1.0,
        min_training_rows=1,
    )

    ridge_one = model_one.named_steps["ridge"]
    ridge_two = model_two.named_steps["ridge"]

    np.testing.assert_array_equal(
        ridge_one.coef_,
        ridge_two.coef_,
    )

    assert ridge_one.intercept_ == ridge_two.intercept_

    X = complete_dataset[FEATURE_COLUMNS]

    predictions_one = model_one.predict(X)
    predictions_two = model_two.predict(X)

    np.testing.assert_array_equal(
        predictions_one,
        predictions_two,
    )

    print("Model coefficients match exactly.")
    print("Model intercepts match exactly.")
    print("Predictions match exactly.")
    print("ML reproducibility verification PASSED.")


if __name__ == "__main__":
    main()