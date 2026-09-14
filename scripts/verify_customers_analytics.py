"""Verify customer analytics against the processed Olist datasets."""

from pathlib import Path

import pandas as pd

from bizintel.analytics.customers import (
    calculate_customer_order_distribution,
    calculate_orders_per_customer,
    calculate_top_customers_by_orders,
    calculate_unique_customers,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CUSTOMERS_FILE = PROJECT_ROOT / "data" / "processed" / "customers.parquet"
ORDERS_FILE = PROJECT_ROOT / "data" / "processed" / "orders.parquet"


def main() -> None:
    """Run customer analytics against the canonical datasets."""
    customers = pd.read_parquet(CUSTOMERS_FILE)
    orders = pd.read_parquet(ORDERS_FILE)

    unique_customers = calculate_unique_customers(customers)
    orders_per_customer = calculate_orders_per_customer(
        orders,
        customers,
    )
    order_distribution = calculate_customer_order_distribution(orders)
    top_customers = calculate_top_customers_by_orders(
        orders,
        limit=10,
    )

    print("Customers Analytics Verification")
    print("=" * 40)

    print(f"Unique Customers: {unique_customers:,}")
    print(f"Average Orders per Customer: {orders_per_customer:.4f}")

    print("\nCustomer Order Distribution:")
    for order_count, customer_count in order_distribution.items():
        print(
            f"  {order_count} order(s): "
            f"{customer_count:,} customer(s)"
        )

    print("\nTop 10 Customers by Orders:")
    for customer_id, order_count in top_customers.items():
        print(f"  {customer_id}: {order_count:,}")


if __name__ == "__main__":
    main()