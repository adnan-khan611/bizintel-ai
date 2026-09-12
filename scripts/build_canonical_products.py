"""Build and inspect the canonical products dataset."""

from pathlib import Path

from bizintel.data.canonical import build_canonical_products
from bizintel.data.readers import read_csv_file

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def main() -> None:
    """Build and inspect canonical products."""
    input_path = RAW_DATA_DIR / "olist_products_dataset.csv"

    raw_products = read_csv_file(input_path)
    canonical_products = build_canonical_products(raw_products)

    print("Raw products:")
    print(f"  Rows: {len(raw_products):,}")
    print(f"  Columns: {len(raw_products.columns)}")

    print("\nCanonical products:")
    print(f"  Rows: {len(canonical_products):,}")
    print(f"  Columns: {len(canonical_products.columns)}")

    print("\nCanonical columns:")
    for column in canonical_products.columns:
        print(f"  - {column}")

    print("\nProduct ID uniqueness:")
    print(
        "  product_id unique: "
        f"{canonical_products['product_id'].is_unique}"
    )

    print("\nMissing values:")
    print(canonical_products.isna().sum())

    print("\nDtypes:")
    print(canonical_products.dtypes)

    print("\nSample:")
    print(canonical_products.head())


if __name__ == "__main__":
    main()