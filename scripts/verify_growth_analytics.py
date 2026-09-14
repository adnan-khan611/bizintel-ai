"""Verify growth analytics against the processed Olist datasets."""

from pathlib import Path

import pandas as pd

from bizintel.analytics.growth import (
    calculate_monthly_orders,
    calculate_monthly_revenue,
    calculate_monthly_unique_customers,
    calculate_order_growth,
    calculate_revenue_growth,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ORDERS_FILE = PROJECT_ROOT / "data" / "processed" / "orders.parquet"
ORDER_ITEMS_FILE = (
    PROJECT_ROOT / "data" / "processed" / "order_items.parquet"
)


def main() -> None:
    """Run growth analytics against the canonical datasets."""
    orders = pd.read_parquet(ORDERS_FILE)
    order_items = pd.read_parquet(ORDER_ITEMS_FILE)

    monthly_revenue = calculate_monthly_revenue(
        orders,
        order_items,
    )
    monthly_orders = calculate_monthly_orders(orders)
    monthly_customers = calculate_monthly_unique_customers(orders)

    revenue_growth = calculate_revenue_growth(monthly_revenue)
    order_growth = calculate_order_growth(monthly_orders)

    print("Growth Analytics Verification")
    print("=" * 40)

    print(
        f"\nDate Range: "
        f"{orders['order_date'].min().date()} "
        f"to "
        f"{orders['order_date'].max().date()}"
    )

    print(f"\nNumber of Months: {len(monthly_revenue)}")

    print("\nMonthly Revenue:")
    for month, revenue_minor in monthly_revenue.items():
        revenue = revenue_minor / 100
        print(f"  {month}: R$ {revenue:,.2f}")

    print("\nMonthly Orders:")
    for month, order_count in monthly_orders.items():
        print(f"  {month}: {order_count:,}")

    print("\nMonthly Unique Customers:")
    for month, customer_count in monthly_customers.items():
        print(f"  {month}: {customer_count:,}")

    print("\nMonth-over-Month Revenue Growth:")
    for month, growth in revenue_growth.items():
        if pd.isna(growth):
            print(f"  {month}: N/A")
        else:
            print(f"  {month}: {growth:.2f}%")

    print("\nMonth-over-Month Order Growth:")
    for month, growth in order_growth.items():
        if pd.isna(growth):
            print(f"  {month}: N/A")
        else:
            print(f"  {month}: {growth:.2f}%")

    print("\nGrowth Analytics Summary:")
    print(f"  Revenue months: {len(monthly_revenue):,}")
    print(f"  Order months: {len(monthly_orders):,}")
    print(f"  Customer months: {len(monthly_customers):,}")
    print(
        "  First-month revenue growth: "
        f"{'N/A' if pd.isna(revenue_growth.iloc[0]) else revenue_growth.iloc[0]}"
    )
    print(
        "  First-month order growth: "
        f"{'N/A' if pd.isna(order_growth.iloc[0]) else order_growth.iloc[0]}"
    )


if __name__ == "__main__":
    main()