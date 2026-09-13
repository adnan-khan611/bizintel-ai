from pathlib import Path

import pandas as pd

from bizintel.data.canonical import (
    build_canonical_customers,
    build_canonical_order_items,
    build_canonical_order_payments,
    build_canonical_orders,
    build_canonical_products,
)
from bizintel.data.parquet import write_parquet_file
from bizintel.data.readers import read_csv_file

DATASET_FILES = {
    "customers": "olist_customers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
}


def build_canonical_datasets(
    raw_data_dir: Path,
) -> dict[str, pd.DataFrame]:
    """Build all MVP canonical datasets from raw Olist CSV files."""
    customers = read_csv_file(
        raw_data_dir / DATASET_FILES["customers"]
    )
    products = read_csv_file(
        raw_data_dir / DATASET_FILES["products"]
    )
    orders = read_csv_file(
        raw_data_dir / DATASET_FILES["orders"]
    )
    order_items = read_csv_file(
        raw_data_dir / DATASET_FILES["order_items"]
    )
    payments = read_csv_file(
        raw_data_dir / DATASET_FILES["order_payments"]
    )

    canonical_customers = build_canonical_customers(
        customers
    )
    canonical_products = build_canonical_products(
        products
    )
    canonical_orders = build_canonical_orders(
        orders,
        customers,
    )
    canonical_order_items = build_canonical_order_items(
        order_items
    )
    canonical_payments = build_canonical_order_payments(
        payments
    )

    return {
        "customers": canonical_customers,
        "products": canonical_products,
        "orders": canonical_orders,
        "order_items": canonical_order_items,
        "order_payments": canonical_payments,
    }


def write_canonical_datasets(
    datasets: dict[str, pd.DataFrame],
    processed_data_dir: Path,
) -> None:
    """Write canonical datasets to Parquet files."""
    processed_data_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    for dataset_name, dataframe in datasets.items():
        output_path = (
            processed_data_dir
            / f"{dataset_name}.parquet"
        )

        write_parquet_file(
            dataframe,
            output_path,
        )


def build_and_write_canonical_datasets(
    raw_data_dir: Path,
    processed_data_dir: Path,
) -> dict[str, pd.DataFrame]:
    """Build canonical datasets and write them to Parquet."""
    datasets = build_canonical_datasets(
        raw_data_dir
    )

    write_canonical_datasets(
        datasets,
        processed_data_dir,
    )

    return datasets