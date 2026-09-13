import pandas as pd
import pytest

from bizintel.data.parquet import write_parquet_file


def test_write_parquet_file_creates_file(tmp_path):
    dataframe = pd.DataFrame(
        {
            "customer_id": ["C001", "C002"],
            "customer_state": ["SP", "RJ"],
        }
    )

    output_path = tmp_path / "customers.parquet"

    write_parquet_file(dataframe, output_path)

    assert output_path.exists()


def test_write_parquet_file_preserves_data(tmp_path):
    dataframe = pd.DataFrame(
        {
            "customer_id": ["C001", "C002"],
            "customer_state": ["SP", "RJ"],
        }
    )

    output_path = tmp_path / "customers.parquet"

    write_parquet_file(dataframe, output_path)

    loaded_dataframe = pd.read_parquet(
        output_path,
        engine="pyarrow",
    )

    pd.testing.assert_frame_equal(
        dataframe,
        loaded_dataframe,
    )


def test_write_parquet_file_creates_parent_directory(tmp_path):
    dataframe = pd.DataFrame(
        {
            "value": [10, 20],
        }
    )

    output_path = (
        tmp_path
        / "processed"
        / "nested"
        / "data.parquet"
    )

    write_parquet_file(dataframe, output_path)

    assert output_path.exists()


def test_write_parquet_file_rejects_non_parquet_path(tmp_path):
    dataframe = pd.DataFrame(
        {
            "value": [10],
        }
    )

    output_path = tmp_path / "data.csv"

    with pytest.raises(ValueError, match="Expected a Parquet file"):
        write_parquet_file(dataframe, output_path)