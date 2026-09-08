"""Build and inspect the canonical customers dataset."""

from pathlib import Path

from bizintel.data.canonical import build_canonical_customers
from bizintel.data.readers import read_csv_file

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def main() -> None:
    """Build and inspect canonical customers."""
    input_path = RAW_DATA_DIR / "olist_customers_dataset.csv"

    raw_customers = read_csv_file(input_path)
    canonical_customers = build_canonical_customers(raw_customers)

    print("Raw customers:")
    print(f"  Rows: {len(raw_customers):,}")
    print(f"  Columns: {len(raw_customers.columns)}")

    print("\nRaw customer identity:")
    print(
        "  Unique customer_unique_id: "
        f"{raw_customers['customer_unique_id'].nunique():,}"
    )

    print("\nCanonical customers:")
    print(f"  Rows: {len(canonical_customers):,}")
    print(f"  Columns: {len(canonical_customers.columns)}")

    print("\nCanonical columns:")
    for column in canonical_customers.columns:
        print(f"  - {column}")

    print("\nCustomer ID uniqueness:")
    print(
        "  customer_id unique: "
        f"{canonical_customers['customer_id'].is_unique}"
    )

    print("\nMissing values:")
    print(canonical_customers.isna().sum())

    print("\nSample:")
    print(canonical_customers.head())


if __name__ == "__main__":
    main()