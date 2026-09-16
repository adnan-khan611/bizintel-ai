"""Real-data verification for the BizIntel AI Ridge forecasting model."""
from decimal import Decimal
from pathlib import Path

import pandas as pd

from bizintel.ml.dataset import build_monthly_revenue_dataset
from bizintel.ml.features import FEATURE_COLUMNS, build_forecasting_features
from bizintel.ml.model import predict_ridge_model, train_ridge_model

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ORDERS_PATH = PROJECT_ROOT / "data" / "raw" / "olist_orders_dataset.csv"
ORDER_ITEMS_PATH = (
    PROJECT_ROOT / "data" / "raw" / "olist_order_items_dataset.csv"
)


def main() -> None:
    """Run Ridge model verification against the real Olist dataset."""
    print("Loading Olist data...")

    orders = pd.read_csv(ORDERS_PATH)
    order_items = pd.read_csv(ORDER_ITEMS_PATH)

    orders["order_date"] = pd.to_datetime(
    orders["order_purchase_timestamp"],
    errors="coerce",
)

    order_items["price_minor"] = order_items["price"].map(
    lambda value: int(Decimal(str(value)) * 100)
)

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

    features = build_forecasting_features(monthly_dataset)

    complete_features = features.dropna(
        subset=FEATURE_COLUMNS
    ).reset_index(drop=True)

    print(f"Complete feature rows: {len(complete_features)}")

    model = train_ridge_model(complete_features)

    forecasts = predict_ridge_model(
        model,
        complete_features,
    )

    results = complete_features[
        ["month", "revenue"]
    ].copy()

    results["forecast"] = forecasts.to_numpy()
    results["error"] = results["revenue"] - results["forecast"]

    print("\nModel verification:")
    print(f"Training rows: {len(complete_features)}")
    print(f"Feature count: {len(FEATURE_COLUMNS)}")
    print(f"Predictions: {len(forecasts)}")

    print("\nForecast preview:")
    print(results.tail(5).to_string(index=False))

    print("\nVerification checks:")

    assert len(monthly_dataset) == 23
    assert monthly_dataset["month"].min() == pd.Period(
        "2016-10",
        freq="M",
    )
    assert monthly_dataset["month"].max() == pd.Period(
        "2018-08",
        freq="M",
    )
    assert len(complete_features) > 0
    assert len(forecasts) == len(complete_features)
    assert forecasts.notna().all()
    assert pd.api.types.is_numeric_dtype(forecasts)

    print("✓ 23-month forecasting window verified")
    print("✓ Complete feature rows verified")
    print("✓ Ridge model trained successfully")
    print("✓ Predictions generated successfully")
    print("✓ Predictions contain no missing values")
    print("\nReal-data Ridge verification PASSED.")


if __name__ == "__main__":
    main()