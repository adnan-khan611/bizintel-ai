"""Verify forecasting model artifact save and load with real Olist data."""

from decimal import Decimal
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from bizintel.ml.artifacts import load_model_artifact, save_model_artifact
from bizintel.ml.features import FEATURE_COLUMNS, build_forecasting_features
from bizintel.ml.training import train_forecasting_model

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ORDERS_PATH = (
    PROJECT_ROOT / "data" / "raw" / "olist_orders_dataset.csv"
)

ORDER_ITEMS_PATH = (
    PROJECT_ROOT / "data" / "raw" / "olist_order_items_dataset.csv"
)

ARTIFACT_PATH = (
    PROJECT_ROOT / "artifacts" / "forecasting_ridge.joblib"
)


def main() -> None:
    """Train, save, load, and verify the forecasting model artifact."""
    print("Loading Olist data...")

    orders = pd.read_csv(
        ORDERS_PATH,
        parse_dates=["order_purchase_timestamp"],
    )

    order_items = pd.read_csv(ORDER_ITEMS_PATH)

    order_items["price_minor"] = order_items["price"].map(
        lambda value: int(Decimal(str(value)) * 100)
    )

    orders = orders.rename(
        columns={
            "order_purchase_timestamp": "order_date",
        }
    )

    monthly_dataset = build_monthly_revenue_dataset(
        orders,
        order_items,
    )

    forecasting_dataset = build_forecasting_features(
        monthly_dataset
    )

    complete_dataset = forecasting_dataset.dropna(
        subset=FEATURE_COLUMNS + ["revenue"]
    ).reset_index(drop=True)

    print(f"Monthly observations: {len(monthly_dataset)}")
    print(
        f"Forecasting window: "
        f"{monthly_dataset['month'].min()} "
        f"to {monthly_dataset['month'].max()}"
    )
    print(f"Complete training rows: {len(complete_dataset)}")

    print("Training forecasting model...")

    model = train_forecasting_model(
        monthly_dataset,
        min_training_rows=10,
    )

    if not isinstance(model, Pipeline):
        raise AssertionError(
            "Training workflow did not return a Pipeline"
        )

    print("Saving model artifact...")

    saved_path = save_model_artifact(
        model,
        ARTIFACT_PATH,
    )

    if saved_path != ARTIFACT_PATH:
        raise AssertionError(
            "Returned artifact path does not match expected path"
        )

    if not ARTIFACT_PATH.exists():
        raise AssertionError(
            "Model artifact file was not created"
        )

    print(f"Artifact saved: {ARTIFACT_PATH}")

    print("Loading model artifact...")

    loaded_model = load_model_artifact(
        ARTIFACT_PATH
    )

    if not isinstance(loaded_model, Pipeline):
        raise AssertionError(
            "Loaded artifact is not a Pipeline"
        )

    original_predictions = model.predict(
        complete_dataset[FEATURE_COLUMNS]
    )

    loaded_predictions = loaded_model.predict(
        complete_dataset[FEATURE_COLUMNS]
    )

    np.testing.assert_allclose(
        original_predictions,
        loaded_predictions,
    )

    print(
        f"Verified predictions: {len(original_predictions)} rows"
    )
    print(
        "Original and loaded model predictions match."
    )
    print("ML artifact verification PASSED.")


def build_monthly_revenue_dataset(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
) -> pd.DataFrame:
    """Build the verified complete monthly forecasting dataset."""
    data = orders[["order_id", "order_date"]].copy()
    data["month"] = data["order_date"].dt.to_period("M")

    data = data[
        (data["month"] >= pd.Period("2016-10", freq="M"))
        & (data["month"] <= pd.Period("2018-08", freq="M"))
    ]

    merged = data.merge(
        order_items[["order_id", "price_minor"]],
        on="order_id",
        how="inner",
    )

    monthly_revenue = (
        merged.groupby("month", as_index=False)["price_minor"]
        .sum()
        .rename(columns={"price_minor": "revenue"})
    )

    complete_month_index = pd.period_range(
        start="2016-10",
        end="2018-08",
        freq="M",
    )

    monthly_revenue = (
        monthly_revenue.set_index("month")
        .reindex(complete_month_index, fill_value=0)
        .rename_axis("month")
        .reset_index()
    )

    monthly_revenue["revenue"] = monthly_revenue[
        "revenue"
    ].astype("int64")

    return monthly_revenue


if __name__ == "__main__":
    main()