from pathlib import Path

import pandas as pd
from scripts.inspect_data import inspect_csv


def test_inspect_csv_reads_csv(capsys, tmp_path):
    """Test that inspect_csv reads a CSV and prints basic information."""
    csv_file = tmp_path / "sample.csv"

    dataframe = pd.DataFrame(
        {
            "customer_id": ["C001", "C002"],
            "amount": [100.0, 200.0],
        }
    )
    dataframe.to_csv(csv_file, index=False)

    inspect_csv(Path(csv_file))

    captured = capsys.readouterr()

    assert "FILE: sample.csv" in captured.out
    assert "Rows: 2" in captured.out
    assert "Columns: 2" in captured.out