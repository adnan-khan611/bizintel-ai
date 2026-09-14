"""Verify revenue analytics using processed Olist data."""

from pathlib import Path

import pandas as pd

from bizintel.analytics.revenue import (
    calculate_freight_value,
    calculate_merchandise_revenue,
    calculate_payment_value,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


def main() -> None:
    """Verify revenue metrics using processed Parquet datasets."""
    order_items_path = (
        PROCESSED_DATA_DIR / "order_items.parquet"
    )
    payments_path = (
        PROCESSED_DATA_DIR / "order_payments.parquet"
    )

    order_items = pd.read_parquet(
        order_items_path,
        engine="pyarrow",
    )

    payments = pd.read_parquet(
        payments_path,
        engine="pyarrow",
    )

    merchandise_revenue = calculate_merchandise_revenue(
        order_items
    )
    freight_value = calculate_freight_value(
        order_items
    )
    payment_value = calculate_payment_value(
        payments
    )

    print("Revenue Analytics Verification")
    print("=" * 40)

    print("\nMerchandise Revenue")
    print(f"  Minor units: {merchandise_revenue:,}")
    print(
        "  Amount: "
        f"R$ {merchandise_revenue / 100:,.2f}"
    )

    print("\nFreight Value")
    print(f"  Minor units: {freight_value:,}")
    print(
        "  Amount: "
        f"R$ {freight_value / 100:,.2f}"
    )

    print("\nPayment Value")
    print(f"  Minor units: {payment_value:,}")
    print(
        "  Amount: "
        f"R$ {payment_value / 100:,.2f}"
    )


if __name__ == "__main__":
    main()