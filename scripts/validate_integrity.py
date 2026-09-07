from pathlib import Path

from bizintel.data.integrity import validate_foreign_key
from bizintel.data.readers import read_csv_file

RAW_DATA_DIR = Path("data/raw")


DATASET_FILES = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
}


def main() -> None:
    """Validate referential integrity across core Olist datasets."""
    customers = read_csv_file(
        RAW_DATA_DIR / DATASET_FILES["customers"]
    )
    orders = read_csv_file(
        RAW_DATA_DIR / DATASET_FILES["orders"]
    )
    order_items = read_csv_file(
        RAW_DATA_DIR / DATASET_FILES["order_items"]
    )
    order_payments = read_csv_file(
        RAW_DATA_DIR / DATASET_FILES["order_payments"]
    )

    checks = [
        (
            "orders.customer_id -> customers.customer_id",
            orders,
            "customer_id",
            customers,
            "customer_id",
        ),
        (
            "order_items.order_id -> orders.order_id",
            order_items,
            "order_id",
            orders,
            "order_id",
        ),
        (
            "order_payments.order_id -> orders.order_id",
            order_payments,
            "order_id",
            orders,
            "order_id",
        ),
    ]

    all_valid = True

    for name, child, child_column, parent, parent_column in checks:
        result = validate_foreign_key(
            child,
            child_column,
            parent,
            parent_column,
        )

        print("\n" + "=" * 60)
        print(f"CHECK: {name}")
        print("=" * 60)
        print(f"Status: {'VALID' if result.is_valid else 'INVALID'}")
        print(f"Missing references: {result.missing_count}")
        print(f"Message: {result.message}")

        if not result.is_valid:
            all_valid = False

    print("\n" + "=" * 60)
    print(
        "OVERALL STATUS: "
        + ("VALID" if all_valid else "INVALID")
    )
    print("=" * 60)


if __name__ == "__main__":
    main()