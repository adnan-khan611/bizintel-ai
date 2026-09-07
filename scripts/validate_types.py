from pathlib import Path

from bizintel.data.readers import read_csv_file
from bizintel.data.type_validation import validate_column_types

RAW_DATA_DIR = Path("data/raw")


DATASET_FILES = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
}


EXPECTED_TYPES = {
    "customers": {
        "customer_id": "string",
        "customer_unique_id": "string",
        "customer_zip_code_prefix": "integer",
        "customer_city": "string",
        "customer_state": "string",
    },
    "orders": {
        "order_id": "string",
        "customer_id": "string",
        "order_status": "string",
        "order_purchase_timestamp": "datetime",
        "order_approved_at": "datetime",
        "order_delivered_carrier_date": "datetime",
        "order_delivered_customer_date": "datetime",
        "order_estimated_delivery_date": "datetime",
    },
    "order_items": {
        "order_id": "string",
        "order_item_id": "integer",
        "product_id": "string",
        "seller_id": "string",
        "shipping_limit_date": "datetime",
        "price": "float",
        "freight_value": "float",
    },
    "order_payments": {
        "order_id": "string",
        "payment_sequential": "integer",
        "payment_type": "string",
        "payment_installments": "integer",
        "payment_value": "float",
    },
}


def main() -> None:
    """Validate types in the core Olist datasets."""
    overall_valid = True

    for dataset_name, filename in DATASET_FILES.items():
        file_path = RAW_DATA_DIR / filename
        dataframe = read_csv_file(file_path)

        result = validate_column_types(
            dataframe,
            EXPECTED_TYPES[dataset_name],
        )

        print("\n" + "=" * 60)
        print(f"DATASET: {dataset_name}")
        print("=" * 60)
        print(
            f"Status: {'VALID' if result.is_valid else 'INVALID'}"
        )

        if result.errors:
            print("\nType errors:")

            for error in result.errors:
                print(f"- {error}")
        else:
            print("No type errors found.")

        if not result.is_valid:
            overall_valid = False

    print("\n" + "=" * 60)
    print(
        "OVERALL STATUS: "
        + ("VALID" if overall_valid else "INVALID")
    )
    print("=" * 60)


if __name__ == "__main__":
    main()