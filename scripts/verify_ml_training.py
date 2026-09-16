"""Verify the forecasting training workflow on the Olist dataset."""

from decimal import Decimal

import pandas as pd

from bizintel.ml.dataset import build_monthly_revenue_dataset
from bizintel.ml.features import FEATURE_COLUMNS, build_forecasting_features
from bizintel.ml.training import train_forecasting_model

RAW_DATA_DIR = "data/raw"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load the Olist orders and order-items datasets."""
    orders = pd.read_csv(
        f"{RAW_DATA_DIR}/olist_orders_dataset.csv",
        parse_dates=[
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
    )

    order_items = pd.read_csv(
        f"{RAW_DATA_DIR}/olist_order_items_dataset.csv",
    )

    order_items["price_minor"] = order_items["price"].map(
        lambda value: int(Decimal(str(value)) * 100)
    )

    orders = orders.rename(
        columns={"order_purchase_timestamp": "order_date"}
    )

    return orders, order_items


def main() -> None:
    """Run real-data verification for the training workflow."""
    print("Loading Olist data...")
    orders, order_items = load_data()

    monthly_dataset = build_monthly_revenue_dataset(
        orders=orders,
        order_items=order_items,
        start_month="2016-10",
        end_month="2018-08",
        include_partial_months=True,
    )

    print(f"Monthly observations: {len(monthly_dataset)}")
    print(f"First month: {monthly_dataset['month'].iloc[0]}")
    print(f"Last month: {monthly_dataset['month'].iloc[-1]}")

    forecasting_dataset = build_forecasting_features(
        monthly_dataset
    )

    complete_dataset = forecasting_dataset.dropna(
        subset=FEATURE_COLUMNS + ["revenue"]
    ).reset_index(drop=True)

    print(f"Complete training rows: {len(complete_dataset)}")

    model = train_forecasting_model(
        monthly_dataset=monthly_dataset,
        min_training_rows=10,
    )

    print("Model type:", type(model).__name__)
    print("Pipeline steps:", list(model.named_steps))
    print("Ridge alpha:", model.named_steps["ridge"].alpha)

    ridge = model.named_steps["ridge"]

    assert hasattr(ridge, "coef_")
    assert len(ridge.coef_) == len(FEATURE_COLUMNS)
    assert len(complete_dataset) >= 10

    print("Training workflow verification PASSED.")


if __name__ == "__main__":
    main()