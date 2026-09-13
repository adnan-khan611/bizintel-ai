"""Build and inspect the canonical order items dataset."""

from pathlib import Path

from bizintel.data.canonical import build_canonical_order_items
from bizintel.data.readers import read_csv_file

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def main() -> None:
    """Build and inspect canonical order items."""
    input_path = RAW_DATA_DIR / "olist_order_items_dataset.csv"

    raw_order_items = read_csv_file(input_path)
    canonical_order_items = build_canonical_order_items(
        raw_order_items
    )

    print("Raw order items:")
    print(f"  Rows: {len(raw_order_items):,}")
    print(f"  Columns: {len(raw_order_items.columns)}")

    print("\nCanonical order items:")
    print(f"  Rows: {len(canonical_order_items):,}")
    print(f"  Columns: {len(canonical_order_items.columns)}")

    print("\nCanonical columns:")
    for column in canonical_order_items.columns:
        print(f"  - {column}")

    print("\nComposite key uniqueness:")
    composite_key_unique = not canonical_order_items.duplicated(
        ["order_id", "order_item_id"]
    ).any()
    print(
        "  (order_id, order_item_id) unique: "
        f"{composite_key_unique}"
    )

    print("\nMissing values:")
    print(canonical_order_items.isna().sum())

    print("\nDtypes:")
    print(canonical_order_items.dtypes)

    print("\nMoney totals:")
    print(
        "  price_minor total: "
        f"{canonical_order_items['price_minor'].sum():,}"
    )
    print(
        "  freight_value_minor total: "
        f"{canonical_order_items['freight_value_minor'].sum():,}"
    )

    print("\nSample:")
    print(canonical_order_items.head())


if __name__ == "__main__":
    main()