"""Verify forecasting model evaluation on the Olist dataset."""

from decimal import Decimal

import pandas as pd

from bizintel.ml.dataset import build_monthly_revenue_dataset
from bizintel.ml.evaluation import evaluate_forecast
from bizintel.ml.features import build_forecasting_features
from bizintel.ml.model import predict_ridge_model, train_ridge_model

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
    """Run real-data forecasting evaluation."""
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
        subset=["revenue"] + [
            column
            for column in forecasting_dataset.columns
            if column not in {"month", "revenue"}
        ]
    ).reset_index(drop=True)

    print(f"Complete feature rows: {len(complete_dataset)}")

    if len(complete_dataset) < 4:
        raise ValueError(
            "Not enough complete feature rows for time-aware evaluation"
        )

    validation_size = 4

    train_dataset = complete_dataset.iloc[:-validation_size].copy()
    validation_dataset = complete_dataset.iloc[-validation_size:].copy()

    print(f"Training rows: {len(train_dataset)}")
    print(f"Validation rows: {len(validation_dataset)}")

    # Naive baseline.
    naive_validation = validation_dataset["revenue"].shift(1)

    previous_training_revenue = train_dataset["revenue"].iloc[-1]

    naive_validation.iloc[0] = previous_training_revenue

    # Ridge model.
    model = train_ridge_model(train_dataset)

    ridge_validation = predict_ridge_model(
        model,
        validation_dataset,
    )

    actual = validation_dataset["revenue"]

    naive_metrics = evaluate_forecast(
        actual,
        naive_validation,
    )

    ridge_metrics = evaluate_forecast(
        actual,
        ridge_validation,
    )

    comparison = pd.DataFrame(
        {
            "metric": ["MAE", "RMSE", "sMAPE"],
            "naive": [
                naive_metrics["mae"],
                naive_metrics["rmse"],
                naive_metrics["smape"],
            ],
            "ridge": [
                ridge_metrics["mae"],
                ridge_metrics["rmse"],
                ridge_metrics["smape"],
            ],
        }
    )

    print("\nValidation period:")
    print(
        f"First month: {validation_dataset['month'].iloc[0]}"
    )
    print(
        f"Last month: {validation_dataset['month'].iloc[-1]}"
    )

    print("\nModel comparison:")
    print(comparison.to_string(index=False))

    print("\nValidation predictions:")

    prediction_table = pd.DataFrame(
        {
            "month": validation_dataset["month"],
            "actual": actual,
            "naive_forecast": naive_validation,
            "ridge_forecast": ridge_validation,
        }
    )

    prediction_table["naive_error"] = (
        prediction_table["actual"]
        - prediction_table["naive_forecast"]
    )

    prediction_table["ridge_error"] = (
        prediction_table["actual"]
        - prediction_table["ridge_forecast"]
    )

    print(prediction_table.to_string(index=False))

    # Basic verification checks.
    assert len(monthly_dataset) == 23
    assert len(complete_dataset) == 11
    assert len(train_dataset) == 7
    assert len(validation_dataset) == 4

    assert naive_validation.notna().all()
    assert ridge_validation.notna().all()

    assert all(
        value >= 0
        for value in naive_metrics.values()
    )

    assert all(
        value >= 0
        for value in ridge_metrics.values()
    )

    print("\nVerification checks:")
    print("✓ 23-month forecasting window verified")
    print("✓ 11 complete feature rows verified")
    print("✓ 7 training rows verified")
    print("✓ 4 validation rows verified")
    print("✓ Naive baseline evaluated successfully")
    print("✓ Ridge model evaluated successfully")
    print("✓ MAE, RMSE and sMAPE calculated successfully")
    print("✓ Validation predictions contain no missing values")

    print("\nReal-data forecasting evaluation PASSED.")


if __name__ == "__main__":
    main()