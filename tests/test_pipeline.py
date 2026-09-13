from pathlib import Path

import pandas as pd

from bizintel.data.pipeline import (
    build_canonical_datasets,
    write_canonical_datasets,
)


def create_raw_dataset_files(raw_data_dir: Path) -> None:
    """Create minimal raw Olist-style datasets for testing."""
    customers = pd.DataFrame(
        {
            "customer_id": ["c1"],
            "customer_unique_id": ["u1"],
            "customer_zip_code_prefix": [1000],
            "customer_city": ["City"],
            "customer_state": ["SP"],
        }
    )

    products = pd.DataFrame(
        {
            "product_id": ["p1"],
            "product_category_name": ["category"],
            "product_name_lenght": [10],
            "product_description_lenght": [20],
            "product_photos_qty": [1],
            "product_weight_g": [100.0],
            "product_length_cm": [10.0],
            "product_height_cm": [5.0],
            "product_width_cm": [5.0],
        }
    )

    orders = pd.DataFrame(
        {
            "order_id": ["o1"],
            "customer_id": ["c1"],
            "order_status": ["delivered"],
            "order_purchase_timestamp": [
                "2018-01-01 10:00:00"
            ],
            "order_approved_at": [
                "2018-01-01 10:10:00"
            ],
            "order_delivered_carrier_date": [
                "2018-01-02 10:00:00"
            ],
            "order_delivered_customer_date": [
                "2018-01-03 10:00:00"
            ],
            "order_estimated_delivery_date": [
                "2018-01-05 10:00:00"
            ],
        }
    )

    order_items = pd.DataFrame(
        {
            "order_id": ["o1"],
            "order_item_id": [1],
            "product_id": ["p1"],
            "seller_id": ["s1"],
            "shipping_limit_date": [
                "2018-01-02 10:00:00"
            ],
            "price": [100.50],
            "freight_value": [10.25],
        }
    )

    payments = pd.DataFrame(
        {
            "order_id": ["o1"],
            "payment_sequential": [1],
            "payment_type": ["credit_card"],
            "payment_installments": [2],
            "payment_value": [110.75],
        }
    )

    customers.to_csv(
        raw_data_dir / "olist_customers_dataset.csv",
        index=False,
    )
    products.to_csv(
        raw_data_dir / "olist_products_dataset.csv",
        index=False,
    )
    orders.to_csv(
        raw_data_dir / "olist_orders_dataset.csv",
        index=False,
    )
    order_items.to_csv(
        raw_data_dir / "olist_order_items_dataset.csv",
        index=False,
    )
    payments.to_csv(
        raw_data_dir / "olist_order_payments_dataset.csv",
        index=False,
    )


def test_build_canonical_datasets(tmp_path):
    raw_data_dir = tmp_path / "raw"
    raw_data_dir.mkdir()

    create_raw_dataset_files(raw_data_dir)

    datasets = build_canonical_datasets(
        raw_data_dir
    )

    assert set(datasets) == {
        "customers",
        "products",
        "orders",
        "order_items",
        "order_payments",
    }

    assert len(datasets["customers"]) == 1
    assert len(datasets["products"]) == 1
    assert len(datasets["orders"]) == 1
    assert len(datasets["order_items"]) == 1
    assert len(datasets["order_payments"]) == 1


def test_write_canonical_datasets(tmp_path):
    raw_data_dir = tmp_path / "raw"
    processed_data_dir = tmp_path / "processed"

    raw_data_dir.mkdir()

    create_raw_dataset_files(raw_data_dir)

    datasets = build_canonical_datasets(
        raw_data_dir
    )

    write_canonical_datasets(
        datasets,
        processed_data_dir,
    )

    expected_files = [
        "customers.parquet",
        "products.parquet",
        "orders.parquet",
        "order_items.parquet",
        "order_payments.parquet",
    ]

    for filename in expected_files:
        assert (
            processed_data_dir / filename
        ).exists()


def test_written_canonical_data_can_be_read_back(
    tmp_path,
):
    raw_data_dir = tmp_path / "raw"
    processed_data_dir = tmp_path / "processed"

    raw_data_dir.mkdir()

    create_raw_dataset_files(raw_data_dir)

    datasets = build_canonical_datasets(
        raw_data_dir
    )

    write_canonical_datasets(
        datasets,
        processed_data_dir,
    )

    orders = pd.read_parquet(
        processed_data_dir / "orders.parquet",
        engine="pyarrow",
    )

    assert len(orders) == 1
    assert orders.loc[0, "order_id"] == "o1"
    assert orders.loc[0, "customer_id"] == "u1"