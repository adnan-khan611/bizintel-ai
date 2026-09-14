"""Verify the forecasting dataset against the processed Olist datasets."""

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
    )

    print("ML Forecasting Dataset Verification")
    print("=" * 50)

    print("\nSource Data:")
    print(f"  Orders: {len(orders):,}")
    print(f"  Order Items: {len(order_items):,}")

    print("\nForecasting Dataset:")
    print(f"  Months: {len(monthly_dataset):,}")
    print(
        f"  First Complete Month: "
        f"{monthly_dataset['month'].min()}"
    )
    print(
        f"  Last Complete Month: "
        f"{monthly_dataset['month'].max()}"
    )

    print("\nDataset Columns:")
    for column in monthly_dataset.columns:
        print(f"  - {column}")

    print("\nMonthly Revenue:")
    for _, row in monthly_dataset.iterrows():
        print(
            f"  {row['month']}: "
            f"{row['revenue']:,} minor units "
            f"(R$ {row['revenue'] / 100:,.2f})"
        )

    print("\nDataset Checks:")
    print(
        f"  Missing Values: "
        f"{monthly_dataset.isna().sum().sum()}"
    )
    print(
        f"  Duplicate Months: "
        f"{monthly_dataset['month'].duplicated().sum()}"
    )
    print(
        f"  Zero-Revenue Months: "
        f"{(monthly_dataset['revenue'] == 0).sum()}"
    )
    print(
        f"  Revenue Data Type: "
        f"{monthly_dataset['revenue'].dtype}"
    )

    expected_months = pd.period_range(
        start=monthly_dataset["month"].min(),
        end=monthly_dataset["month"].max(),
        freq="M",
    )

    expected_months_series = pd.Series(
        expected_months,
        name="month",
    ).reset_index(drop=True)

    actual_months_series = monthly_dataset["month"].reset_index(
        drop=True
    )

    print(
        f"  Continuous Calendar Months: "
        f"{actual_months_series.equals(expected_months_series)}"
    )


if __name__ == "__main__":
    main()