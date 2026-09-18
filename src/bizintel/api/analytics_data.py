"""Analytics data access utilities for BizIntel AI."""

from pathlib import Path

import pandas as pd

from bizintel.data.parquet import read_parquet_file

DATASET_NAMES = (
    "customers",
    "products",
    "orders",
    "order_items",
    "order_payments",
)


def load_analytics_datasets(
    processed_data_dir: Path,
) -> dict[str, pd.DataFrame]:
    """Load canonical analytics datasets from Parquet files."""
    datasets: dict[str, pd.DataFrame] = {}

    for dataset_name in DATASET_NAMES:
        file_path = (
            processed_data_dir
            / f"{dataset_name}.parquet"
        )

        datasets[dataset_name] = read_parquet_file(
            file_path
        )

    return datasets