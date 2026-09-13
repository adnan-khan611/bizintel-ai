"""Build and inspect the canonical order payments dataset."""

from pathlib import Path

from bizintel.data.canonical import build_canonical_order_payments
from bizintel.data.readers import read_csv_file

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def main() -> None:
    """Build and inspect canonical order payments."""
    input_path = RAW_DATA_DIR / "olist_order_payments_dataset.csv"

    raw_payments = read_csv_file(input_path)

    canonical_payments = build_canonical_order_payments(
        raw_payments
    )

    print("Raw order payments:")
    print(f"  Rows: {len(raw_payments):,}")
    print(f"  Columns: {len(raw_payments.columns)}")

    print("\nCanonical order payments:")
    print(f"  Rows: {len(canonical_payments):,}")
    print(f"  Columns: {len(canonical_payments.columns)}")

    print("\nCanonical columns:")
    for column in canonical_payments.columns:
        print(f"  - {column}")

    print("\nPayment ID uniqueness:")
    print(
        "  payment_id unique: "
        f"{canonical_payments['payment_id'].is_unique}"
    )

    print("\nMissing values:")
    print(canonical_payments.isna().sum())

    print("\nDtypes:")
    print(canonical_payments.dtypes)

    print("\nMoney totals:")
    print(
        "  payment_value_minor total: "
        f"{canonical_payments['payment_value_minor'].sum():,}"
    )

    print("\nPayment types:")
    print(canonical_payments["payment_type"].value_counts())

    print("\nZero-installment records:")
    print(
        "  Count: "
        f"{(canonical_payments['payment_installments'] == 0).sum()}"
    )

    print("\nSample:")
    print(canonical_payments.head())


if __name__ == "__main__":
    main()