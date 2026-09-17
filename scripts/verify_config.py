"""Verify environment-based configuration with the forecasting workflow."""

from os import environ
from pathlib import Path

import pandas as pd

from bizintel.config import Settings
from bizintel.ml.features import build_forecasting_features
from bizintel.ml.training import train_forecasting_model

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ORDERS_PATH = PROJECT_ROOT / "data" / "raw" / "olist_orders_dataset.csv"
ORDER_ITEMS_PATH = (
    PROJECT_ROOT / "data" / "raw" / "olist_order_items_dataset.csv"
)


def main() -> None:
    """Verify configuration and its effect on model training."""
    print("Setting test environment variables...")

    environ["FORECASTING_MODEL_VERSION"] = "2.0.0"
    environ["FORECASTING_RIDGE_ALPHA"] = "2.5"
    environ["FORECASTING_MIN_TRAINING_ROWS"] = "10"

    settings = Settings()

    print(f"Model version: {settings.forecasting_model_version}")
    print(f"Ridge alpha: {settings.forecasting_ridge_alpha}")
    print(
        "Minimum training rows: "
        f"{settings.forecasting_min_training_rows}"
    )

    if settings.forecasting_model_version != "2.0.0":
        raise AssertionError("Model version configuration was not applied")

    if settings.forecasting_ridge_alpha != 2.5:
        raise AssertionError("Ridge alpha configuration was not applied")

    if settings.forecasting_min_training_rows != 10:
        raise AssertionError(
            "Minimum training rows configuration was not applied"
        )

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

    forecasting_dataset = build_forecasting_features(
        monthly_dataset
    )

    complete_dataset = forecasting_dataset.dropna(
        subset=["revenue"]
    ).copy()

    print(f"Monthly observations: {len(monthly_dataset)}")
    print(
        f"Complete feature rows: "
        f"{len(complete_dataset.dropna())}"
    )

    print("Training forecasting model with configured alpha...")

    model = train_forecasting_model(
        monthly_dataset,
        alpha=settings.forecasting_ridge_alpha,
        min_training_rows=settings.forecasting_min_training_rows,
    )

    actual_alpha = model.named_steps["ridge"].alpha

    print(f"Trained Ridge alpha: {actual_alpha}")

    if actual_alpha != settings.forecasting_ridge_alpha:
        raise AssertionError(
            "Trained model did not use configured Ridge alpha"
        )

    print("Configuration is correctly applied to model training.")
    print("Configuration verification PASSED.")


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