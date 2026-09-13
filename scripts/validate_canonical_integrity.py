"""Validate referential integrity across canonical datasets."""

from pathlib import Path

from bizintel.data.canonical import (
    build_canonical_customers,
    build_canonical_order_items,
    build_canonical_order_payments,
    build_canonical_orders,
    build_canonical_products,
)
from bizintel.data.integrity import validate_foreign_key
from bizintel.data.readers import read_csv_file

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def main() -> None:
    """Build canonical datasets and validate their relationships."""
    customers = read_csv_file(
        RAW_DATA_DIR / "olist_customers_dataset.csv"
    )
    products = read_csv_file(
        RAW_DATA_DIR / "olist_products_dataset.csv"
    )
    orders = read_csv_file(
        RAW_DATA_DIR / "olist_orders_dataset.csv"
    )
    order_items = read_csv_file(
        RAW_DATA_DIR / "olist_order_items_dataset.csv"
    )
    payments = read_csv_file(
        RAW_DATA_DIR / "olist_order_payments_dataset.csv"
    )

    canonical_customers = build_canonical_customers(customers)
    canonical_products = build_canonical_products(products)
    canonical_orders = build_canonical_orders(
        orders,
        customers,
    )
    canonical_order_items = build_canonical_order_items(order_items)
    canonical_payments = build_canonical_order_payments(payments)

    checks = [
        (
            "Orders → Customers",
            validate_foreign_key(
                canonical_orders,
                "customer_id",
                canonical_customers,
                "customer_id",
            ),
        ),
        (
            "Order Items → Orders",
            validate_foreign_key(
                canonical_order_items,
                "order_id",
                canonical_orders,
                "order_id",
            ),
        ),
        (
            "Order Items → Products",
            validate_foreign_key(
                canonical_order_items,
                "product_id",
                canonical_products,
                "product_id",
            ),
        ),
        (
            "Payments → Orders",
            validate_foreign_key(
                canonical_payments,
                "order_id",
                canonical_orders,
                "order_id",
            ),
        ),
    ]

    print("Canonical Referential Integrity")
    print("=" * 40)

    overall_valid = True

    for check_name, result in checks:
        status = "VALID" if result.is_valid else "INVALID"

        print(f"\n{check_name}: {status}")
        print(f"  Missing references: {result.missing_count:,}")
        print(f"  Message: {result.message}")

        if not result.is_valid:
            overall_valid = False

    print("\nOverall:")
    print("  VALID" if overall_valid else "  INVALID")


if __name__ == "__main__":
    main()