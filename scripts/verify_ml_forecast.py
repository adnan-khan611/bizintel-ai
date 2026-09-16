"""Verify next-month forecasting on the Olist dataset."""

from decimal import Decimal

import pandas as pd

from bizintel.ml.dataset import build_monthly_revenue_dataset
from bizintel.ml.features import build_forecasting_features
from bizintel.ml.forecast import generate_next_month_ridge_forecast

RAW_DATA_DIR = "data/raw"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load the raw Olist orders and order items datasets."""
    print("Loading Olist data...")

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
        f"{RAW_DATA_DIR}/olist_order_items_dataset.csv"
    )

    order_items["price_minor"] = order_items["price"].map(
        lambda value: int(Decimal(str(value)) * 100)
    )

    orders = orders.rename(
        columns={
            "order_purchase_timestamp": "order_date",
        }
    )

    return orders, order_items


def main() -> None:
    """Run real-data next-month forecast verification."""
    orders, order_items = load_data()

    monthly_dataset = build_monthly_revenue_dataset(
        orders=orders,
        order_items=order_items,
        start_month="2016-10",
        end_month="2018-08",
        include_partial_months=True,
    )

    print(f"Monthly observations: {len(monthly_dataset)}")
    print(f"First month: {monthly_dataset['month'].min()}")
    print(f"Last month: {monthly_dataset['month'].max()}")

    forecasting_dataset = build_forecasting_features(
        monthly_dataset
    )

    complete_dataset = forecasting_dataset.dropna(
        subset=[
            column
            for column in forecasting_dataset.columns
            if column not in {"month", "revenue"}
        ]
    ).reset_index(drop=True)

    print(f"Complete feature rows: {len(complete_dataset)}")

    forecast = generate_next_month_ridge_forecast(
        complete_dataset
    )

    print("\nNext-month forecast:")
    print(forecast.to_string(index=False))

    forecast_month = forecast["forecast_month"].iloc[0]
    forecast_revenue = forecast["forecast_revenue"].iloc[0]

    print("\nVerification checks:")

    assert len(monthly_dataset) == 23
    assert len(complete_dataset) == 11
    assert len(forecast) == 1

    assert forecast_month == pd.Period(
        "2018-09",
        freq="M",
    )

    assert pd.notna(forecast_revenue)
    assert forecast_revenue >= 0

    print("✓ 23-month forecasting window verified")
    print("✓ 11 complete feature rows verified")
    print("✓ Next forecast month verified as 2018-09")
    print("✓ Forecast contains no missing value")
    print("✓ Forecast revenue is non-negative")

    print("\nReal-data next-month forecast verification PASSED.")


if __name__ == "__main__":
    main()