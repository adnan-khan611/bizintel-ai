from pathlib import Path

import pandas as pd
import pytest

from bizintel.data.readers import read_csv_file


def test_read_csv_file_returns_dataframe(tmp_path):
    """Test that a valid CSV is loaded as a DataFrame."""
    csv_file = tmp_path / "sample.csv"

    dataframe = pd.DataFrame(
        {
            "customer_id": ["C001", "C002"],
            "amount": [100.0, 200.0],
        }
    )
    dataframe.to_csv(csv_file, index=False)

    result = read_csv_file(Path(csv_file))

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert list(result.columns) == ["customer_id", "amount"]


def test_read_csv_file_raises_for_missing_file(tmp_path):
    """Test that a missing CSV raises FileNotFoundError."""
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        read_csv_file(missing_file)


def test_read_csv_file_raises_for_non_csv_file(tmp_path):
    """Test that a non-CSV file raises ValueError."""
    text_file = tmp_path / "sample.txt"
    text_file.write_text("not a csv")

    with pytest.raises(ValueError):
        read_csv_file(text_file)