"""Verify order analytics against the processed Olist dataset."""

from pathlib import Path

import pandas as pd

from bizintel.analytics.orders import (
    calculate_canceled_orders,
    calculate_delivered_orders,
    calculate_orders_by_status,
    calculate_total_orders,
    calculate_unavailable_orders,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORDERS_FILE = PROJECT_ROOT / "data" / "processed" / "orders.parquet"


def main() -> None:
    """Run order analytics against the canonical orders dataset."""
    orders = pd.read_parquet(ORDERS_FILE)

    total_orders = calculate_total_orders(orders)
    orders_by_status = calculate_orders_by_status(orders)
    delivered_orders = calculate_delivered_orders(orders)
    canceled_orders = calculate_canceled_orders(orders)
    unavailable_orders = calculate_unavailable_orders(orders)

    print("Orders Analytics Verification")
    print("=" * 40)

    print(f"Total Orders: {total_orders:,}")
    print(f"Delivered Orders: {delivered_orders:,}")
    print(f"Canceled Orders: {canceled_orders:,}")
    print(f"Unavailable Orders: {unavailable_orders:,}")

    print("\nOrders by Status:")
    for status, count in orders_by_status.items():
        print(f"  {status}: {count:,}")


if __name__ == "__main__":
    main()