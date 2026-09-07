import pandas as pd


def parse_datetime_column(
    series: pd.Series,
) -> pd.Series:
    """Convert a Series to pandas datetime values."""
    return pd.to_datetime(
        series,
        errors="coerce",
    )