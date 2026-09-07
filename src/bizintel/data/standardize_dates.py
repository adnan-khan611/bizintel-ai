from dataclasses import dataclass

import pandas as pd

from bizintel.data.datetime_utils import parse_datetime_column


@dataclass(frozen=True)
class DateStandardizationResult:
    """Represent the result of standardizing a date column."""

    dataframe: pd.DataFrame
    invalid_count: int


def standardize_datetime_column(
    dataframe: pd.DataFrame,
    column: str,
) -> DateStandardizationResult:
    """Convert one DataFrame column to datetime and report invalid values."""
    if column not in dataframe.columns:
        raise ValueError(f"Column not found: {column}")

    original_values = dataframe[column]
    standardized_values = parse_datetime_column(original_values)

    invalid_count = int(
        standardized_values.isna().sum()
        - original_values.isna().sum()
    )

    result_dataframe = dataframe.copy()
    result_dataframe[column] = standardized_values

    return DateStandardizationResult(
        dataframe=result_dataframe,
        invalid_count=max(invalid_count, 0),
    )