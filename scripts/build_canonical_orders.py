"""Build and inspect the canonical orders dataset."""

from pathlib import Path

from bizintel.data.canonical import build_canonical_orders
from bizintel.data.readers import read_csv_file

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def main() -> None:
    """Build and inspect canonical orders."""
    orders_path = RAW_DATA_DIR / "olist_orders_dataset.csv"
    customers_path = RAW_DATA_DIR / "olist_customers_dataset.csv"

    raw_orders = read_csv_file(orders_path)
    raw_customers = read_csv_file(customers_path)

    canonical_orders = build_canonical_orders(
        raw_orders,
        raw_customers,
    )

    print("Raw orders:")
    print(f"  Rows: {len(raw_orders):,}")
    print(f"  Columns: {len(raw_orders.columns)}")

    print("\nCanonical orders:")
    print(f"  Rows: {len(canonical_orders):,}")
    print(f"  Columns: {len(canonical_orders.columns)}")

    print("\nCanonical columns:")
    for column in canonical_orders.columns:
        print(f"  - {column}")

    print("\nOrder ID uniqueness:")
    print(
        "  order_id unique: "
        f"{canonical_orders['order_id'].is_unique}"
    )

    print("\nCustomer ID missing:")
    print(
        "  Missing customer_id: "
        f"{canonical_orders['customer_id'].isna().sum():,}"
    )

    print("\nMissing values:")
    print(canonical_orders.isna().sum())

    print("\nDtypes:")
    print(canonical_orders.dtypes)

    print("\nSample:")
    print(canonical_orders.head())


if __name__ == "__main__":
    main()