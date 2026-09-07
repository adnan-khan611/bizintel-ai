from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class IntegrityResult:
    """Represent the result of a referential integrity check."""

    is_valid: bool
    missing_count: int
    message: str


def validate_foreign_key(
    child_dataframe: pd.DataFrame,
    child_column: str,
    parent_dataframe: pd.DataFrame,
    parent_column: str,
) -> IntegrityResult:
    """Validate that child values exist in the parent column."""
    if child_column not in child_dataframe.columns:
        raise ValueError(
            f"Child column not found: {child_column}"
        )

    if parent_column not in parent_dataframe.columns:
        raise ValueError(
            f"Parent column not found: {parent_column}"
        )

    parent_values = set(parent_dataframe[parent_column].dropna())

    child_values = child_dataframe[child_column].dropna()

    missing_count = int(
        (~child_values.isin(parent_values)).sum()
    )

    if missing_count == 0:
        return IntegrityResult(
            is_valid=True,
            missing_count=0,
            message="Referential integrity check passed.",
        )

    return IntegrityResult(
        is_valid=False,
        missing_count=missing_count,
        message=(
            f"Found {missing_count:,} child records with "
            "missing parent references."
        ),
    )