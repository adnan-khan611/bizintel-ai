"""Tests for analytics data access utilities."""

import pandas as pd
import pytest

from bizintel.api.analytics_data import load_analytics_datasets


def test_load_analytics_datasets_reads_all_datasets(tmp_path):
    dataset_names = (
        "customers",
        "products",
        "orders",
        "order_items",
        "order_payments",
    )

    for dataset_name in dataset_names:
        dataframe = pd.DataFrame(
            {
                "id": [1, 2],
                "value": ["A", "B"],
            }
        )

        dataframe.to_parquet(
            tmp_path / f"{dataset_name}.parquet",
            engine="pyarrow",
            index=False,
        )

    datasets = load_analytics_datasets(tmp_path)

    assert set(datasets) == set(dataset_names)

    for dataset_name in dataset_names:
        pd.testing.assert_frame_equal(
            datasets[dataset_name],
            pd.DataFrame(
                {
                    "id": [1, 2],
                    "value": ["A", "B"],
                }
            ),
        )


def test_load_analytics_datasets_raises_for_missing_dataset(
    tmp_path,
):
    customers = pd.DataFrame(
        {
            "customer_id": ["C001"],
        }
    )

    customers.to_parquet(
        tmp_path / "customers.parquet",
        engine="pyarrow",
        index=False,
    )

    with pytest.raises(
        FileNotFoundError,
        match="Parquet file not found",
    ):
        load_analytics_datasets(tmp_path)