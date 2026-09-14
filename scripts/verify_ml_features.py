"""Verify forecasting features against the processed Olist datasets."""

from pathlib import Path

import pandas as pd

from bizintel.ml.dataset import build_monthly_revenue_dataset
from bizintel.ml.features import build_forecasting_features

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ORDERS_FILE = PROJECT_ROOT / "data" / "processed" / "orders.parquet"
ORDER_ITEMS_FILE = (
    PROJECT_ROOT / "data" / "processed" / "order_items.parquet"
)


def main() -> None:
    """Run feature engineering verification on canonical datasets."""

    orders = pd.read_parquet(ORDERS_FILE)
    order_items = pd.read_parquet(ORDER_ITEMS_FILE)

    monthly_dataset = build_monthly_revenue_dataset(
        orders=orders,
        order_items=order_items,
    )

    features = build_forecasting_features(monthly_dataset)

    print("ML Feature Engineering Verification")
    print("=" * 60)

    print("\nSource Dataset:")
    print(f"  Months: {len(monthly_dataset):,}")
    print(f"  First Month: {monthly_dataset['month'].min()}")
    print(f"  Last Month: {monthly_dataset['month'].max()}")

    print("\nFeature Dataset:")
    print(f"  Rows: {len(features):,}")
    print(f"  Columns: {len(features.columns):,}")

    print("\nFeature Columns:")
    for column in features.columns:
        print(f"  - {column}")

    print("\nFeature Preview:")
    print(features.to_string(index=False))

    print("\nMissing Values:")
    print(features.isna().sum())

    print("\nFeature Readiness:")
    print(
        f"  Lag 1 available from row 1: "
        f"{pd.notna(features.loc[1, 'revenue_lag_1'])}"
    )
    print(
        f"  Lag 12 available from row 12: "
        f"{pd.notna(features.loc[12, 'revenue_lag_12'])}"
    )
    print(
        f"  Rolling mean 3 available from row 3: "
        f"{pd.notna(features.loc[3, 'revenue_rolling_mean_3'])}"
    )
    print(
        f"  Rolling mean 6 available from row 6: "
        f"{pd.notna(features.loc[6, 'revenue_rolling_mean_6'])}"
    )

    print("\nCalendar Features:")
    print(
        f"  Month range: "
        f"{features['month_number'].min()}-"
        f"{features['month_number'].max()}"
    )
    print(
        f"  Quarter range: "
        f"{features['quarter'].min()}-"
        f"{features['quarter'].max()}"
    )
    print(
        f"  Year range: "
        f"{features['year'].min()}-"
        f"{features['year'].max()}"
    )

    print("\nData Integrity:")
    print(
        f"  Duplicate Months: "
        f"{features['month'].duplicated().sum()}"
    )
    print(
        f"  Revenue Data Type: "
        f"{features['revenue'].dtype}"
    )
    print(
        f"  Chronologically Sorted: "
        f"{features['month'].is_monotonic_increasing}"
    )


if __name__ == "__main__":
    main()