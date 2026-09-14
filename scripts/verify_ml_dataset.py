"""Verify forecasting dataset against the processed Olist datasets."""

from pathlib import Path

import pandas as pd

from bizintel.ml.dataset import build_monthly_revenue_dataset

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ORDERS_FILE = PROJECT_ROOT / "data" / "processed" / "orders.parquet"
ORDER_ITEMS_FILE = (
    PROJECT_ROOT / "data" / "processed" / "order_items.parquet"
)


def main() -> None:
    """Run forecasting dataset verification on canonical datasets."""

    orders = pd.read_parquet(ORDERS_FILE)
    order_items = pd.read_parquet(ORDER_ITEMS_FILE)

    monthly_dataset = build_monthly_revenue_dataset(
        orders=orders,
        order_items=order_items,
        start_month="2016-10",
        end_month="2018-08",
        include_partial_months=True,
    )

    print("ML Dataset Verification")
    print("=" * 60)

    print("\nDataset:")
    print(f"  Months: {len(monthly_dataset):,}")
    print(f"  First Month: {monthly_dataset['month'].min()}")
    print(f"  Last Month: {monthly_dataset['month'].max()}")

    print("\nRevenue:")
    print(
        f"  Total Revenue: "
        f"R$ {monthly_dataset['revenue'].sum() / 100:,.2f}"
    )

    print(
        f"  Minimum Monthly Revenue: "
        f"R$ {monthly_dataset['revenue'].min() / 100:,.2f}"
    )

    print(
        f"  Maximum Monthly Revenue: "
        f"R$ {monthly_dataset['revenue'].max() / 100:,.2f}"
    )

    print("\nData Integrity:")
    print(
        f"  Duplicate Months: "
        f"{monthly_dataset['month'].duplicated().sum()}"
    )

    print(
        f"  Missing Revenue Values: "
        f"{monthly_dataset['revenue'].isna().sum()}"
    )

    print(
        f"  Revenue Data Type: "
        f"{monthly_dataset['revenue'].dtype}"
    )

    print(
        f"  Chronologically Sorted: "
        f"{monthly_dataset['month'].is_monotonic_increasing}"
    )

    expected_months = pd.period_range(
        start="2016-10",
        end="2018-08",
        freq="M",
    )

    print(
        f"  Continuous Months: "
        f"{monthly_dataset['month'].tolist() == expected_months.tolist()}"
    )

    print("\nBoundary Checks:")
    print(
        f"  Contains 2016-09: "
        f"{pd.Period('2016-09', freq='M') in monthly_dataset['month'].values}"
    )

    print(
        f"  Contains 2018-09: "
        f"{pd.Period('2018-09', freq='M') in monthly_dataset['month'].values}"
    )

    print(
        f"  Contains 2018-10: "
        f"{pd.Period('2018-10', freq='M') in monthly_dataset['month'].values}"
    )

    print("\nDataset Preview:")
    print(monthly_dataset.head().to_string(index=False))

    print("\nDataset Tail:")
    print(monthly_dataset.tail().to_string(index=False))


if __name__ == "__main__":
    main()