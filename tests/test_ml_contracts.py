"""Tests for forecasting feature contracts."""

import pandas as pd
import pytest

from bizintel.ml.contracts import (
    get_feature_matrix,
    validate_feature_columns,
    validate_inference_features,
)
from bizintel.ml.features import FEATURE_COLUMNS


def make_valid_features() -> pd.DataFrame:
    """Create a valid forecasting feature dataset."""
    return pd.DataFrame(
        {
            column: [float(index + 1), float(index + 2)]
            for index, column in enumerate(FEATURE_COLUMNS)
        }
    )


def test_validate_feature_columns_accepts_valid_features() -> None:
    """Test that all required features are accepted."""
    data = make_valid_features()

    validate_feature_columns(data)


def test_validate_feature_columns_rejects_missing_feature() -> None:
    """Test that missing required features are rejected."""
    data = make_valid_features()
    data = data.drop(columns=["revenue_lag_1"])

    with pytest.raises(
    ValueError,
    match="Missing required columns",
    ):
        validate_feature_columns(data)


def test_get_feature_matrix_preserves_feature_contract_order() -> None:
    """Test that feature columns are returned in canonical order."""
    data = make_valid_features()
    data = data[
        list(reversed(FEATURE_COLUMNS))
    ]

    feature_matrix = get_feature_matrix(data)

    assert list(feature_matrix.columns) == FEATURE_COLUMNS


def test_get_feature_matrix_rejects_non_numeric_feature() -> None:
    """Test that non-numeric feature values are rejected."""
    data = make_valid_features()
    data["revenue_lag_1"] = ["invalid", "value"]

    with pytest.raises(
        TypeError,
        match="Forecasting features must be numeric",
    ):
        get_feature_matrix(data)


def test_validate_inference_features_accepts_complete_features() -> None:
    """Test that complete inference features are accepted."""
    data = make_valid_features()

    validate_inference_features(data)


def test_validate_inference_features_rejects_missing_values() -> None:
    """Test that missing inference feature values are rejected."""
    data = make_valid_features()
    data.loc[0, "revenue_lag_1"] = float("nan")

    with pytest.raises(
        ValueError,
        match="Forecasting features contain missing values",
    ):
        validate_inference_features(data)