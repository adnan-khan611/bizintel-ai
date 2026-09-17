"""Verify forecasting model metadata with real Olist data."""

from pathlib import Path

import pandas as pd

from bizintel.ml.features import FEATURE_COLUMNS
from bizintel.ml.metadata import (
    create_model_metadata,
    load_model_metadata,
    save_model_metadata,
)
from bizintel.ml.training import train_forecasting_model

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ORDERS_PATH = (
    PROJECT_ROOT / "data" / "raw" / "olist_orders_dataset.csv"
)

ORDER_ITEMS_PATH = (
    PROJECT_ROOT / "data" / "raw" / "olist_order_items_dataset.csv"
)

METADATA_PATH = (
    PROJECT_ROOT / "artifacts" / "forecasting_ridge.json"
)


def main() -> None:
    """Create, save, load, and verify forecasting model metadata."""
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
        columns={
            "order_purchase_timestamp": "order_date",
        }
    )

    monthly_dataset = build_monthly_revenue_dataset(
        orders,
        order_items,
    )

    print(f"Monthly observations: {len(monthly_dataset)}")
    print(
        f"Training window: "
        f"{monthly_dataset['month'].min()} "
        f"to {monthly_dataset['month'].max()}"
    )

    print("Training forecasting model...")

    model = train_forecasting_model(
        monthly_dataset,
        alpha=1.0,
        min_training_rows=10,
    )

    if model.named_steps["ridge"].alpha != 1.0:
        raise AssertionError("Unexpected Ridge alpha")

    print("Creating model metadata...")

    metadata = create_model_metadata(
        model_name="revenue_forecasting",
        model_version="1.0.0",
        model_type="ridge",
        target="monthly_merchandise_revenue",
        feature_columns=FEATURE_COLUMNS,
        training_start=str(monthly_dataset["month"].min()),
        training_end=str(monthly_dataset["month"].max()),
        hyperparameters={
            "alpha": 1.0,
        },
    )

    print("Saving metadata...")

    saved_path = save_model_metadata(
        metadata,
        METADATA_PATH,
    )

    if saved_path != METADATA_PATH:
        raise AssertionError(
            "Returned metadata path does not match expected path"
        )

    if not METADATA_PATH.exists():
        raise AssertionError(
            "Metadata JSON file was not created"
        )

    print(f"Metadata saved: {METADATA_PATH}")

    print("Loading metadata...")

    loaded_metadata = load_model_metadata(
        METADATA_PATH,
    )

    if loaded_metadata != metadata:
        raise AssertionError(
            "Loaded metadata does not match original metadata"
        )

    if loaded_metadata.model_version != "1.0.0":
        raise AssertionError("Unexpected model version")

    if loaded_metadata.model_type != "ridge":
        raise AssertionError("Unexpected model type")

    if loaded_metadata.target != "monthly_merchandise_revenue":
        raise AssertionError("Unexpected target")

    if loaded_metadata.feature_columns != FEATURE_COLUMNS:
        raise AssertionError(
            "Metadata feature columns do not match feature contract"
        )

    if loaded_metadata.training_start != "2016-10":
        raise AssertionError("Unexpected training start")

    if loaded_metadata.training_end != "2018-08":
        raise AssertionError("Unexpected training end")

    if loaded_metadata.hyperparameters != {"alpha": 1.0}:
        raise AssertionError("Unexpected hyperparameters")

    print("Metadata content verified.")
    print("ML metadata verification PASSED.")


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