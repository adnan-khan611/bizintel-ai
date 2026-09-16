"""Verify forecasting backtesting on the Olist dataset."""

from decimal import Decimal

import pandas as pd

from bizintel.ml.backtesting import run_expanding_window_backtest
from bizintel.ml.dataset import build_monthly_revenue_dataset
from bizintel.ml.features import build_forecasting_features

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
    """Run real-data expanding-window backtesting."""
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

    results, metrics = run_expanding_window_backtest(
        complete_dataset,
        min_train_size=7,
    )

    print("\nBacktesting configuration:")
    print("Strategy: Expanding window")
    print("Forecast horizon: 1 month")
    print("Minimum training rows: 7")
    print(f"Backtest folds: {len(results)}")

    print("\nFold results:")
    print(results.to_string(index=False))

    print("\nAggregate metrics:")

    comparison = pd.DataFrame(
        {
            "metric": ["MAE", "RMSE", "sMAPE"],
            "naive": [
                metrics["naive"]["mae"],
                metrics["naive"]["rmse"],
                metrics["naive"]["smape"],
            ],
            "ridge": [
                metrics["ridge"]["mae"],
                metrics["ridge"]["rmse"],
                metrics["ridge"]["smape"],
            ],
        }
    )

    print(comparison.to_string(index=False))

    print("\nVerification checks:")
    assert len(monthly_dataset) == 23
    assert len(complete_dataset) == 11
    assert len(results) == 4

    assert results["train_size"].tolist() == [
        7,
        8,
        9,
        10,
    ]

    assert results["validation_month"].tolist() == (
        pd.period_range(
            start="2018-05",
            end="2018-08",
            freq="M",
        ).tolist()
    )

    assert results["actual"].notna().all()
    assert results["naive_forecast"].notna().all()
    assert results["ridge_forecast"].notna().all()

    assert all(
        value >= 0
        for model_metrics in metrics.values()
        for value in model_metrics.values()
    )

    print("✓ 23-month forecasting window verified")
    print("✓ 11 complete feature rows verified")
    print("✓ 4 expanding-window folds verified")
    print("✓ One-month-ahead validation verified")
    print("✓ Naive baseline evaluated across all folds")
    print("✓ Ridge model evaluated across all folds")
    print("✓ Aggregate MAE, RMSE and sMAPE calculated")
    print("✓ Backtest predictions contain no missing values")

    print("\nReal-data forecasting backtesting PASSED.")


if __name__ == "__main__":
    main()