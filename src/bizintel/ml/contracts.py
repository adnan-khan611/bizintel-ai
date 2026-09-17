"""Feature contract utilities for BizIntel AI forecasting."""

import pandas as pd

from bizintel.ml.features import FEATURE_COLUMNS


def validate_feature_columns(
    forecasting_dataset: pd.DataFrame,
) -> None:
    """Validate that all required forecasting features are present."""
    missing_columns = set(FEATURE_COLUMNS) - set(
        forecasting_dataset.columns
    )

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")


def get_feature_matrix(
    forecasting_dataset: pd.DataFrame,
) -> pd.DataFrame:
    """Return forecasting features in the canonical contract order."""
    validate_feature_columns(forecasting_dataset)

    feature_matrix = forecasting_dataset[FEATURE_COLUMNS].copy()

    non_numeric_columns = [
        column
        for column in FEATURE_COLUMNS
        if not pd.api.types.is_numeric_dtype(feature_matrix[column])
    ]

    if non_numeric_columns:
        columns = ", ".join(sorted(non_numeric_columns))
        raise TypeError(
            f"Forecasting features must be numeric: {columns}"
        )

    return feature_matrix


def validate_inference_features(
    forecasting_dataset: pd.DataFrame,
) -> None:
    """Validate that inference features contain no missing values."""
    feature_matrix = get_feature_matrix(forecasting_dataset)

    if feature_matrix.isna().any().any():
        raise ValueError(
            "Forecasting features contain missing values"
        )