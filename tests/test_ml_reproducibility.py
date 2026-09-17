"""Tests for forecasting model reproducibility."""

import numpy as np
import pandas as pd

from bizintel.ml.features import FEATURE_COLUMNS
from bizintel.ml.training import train_forecasting_model


def make_monthly_dataset() -> pd.DataFrame:
    """Create a deterministic monthly dataset for reproducibility tests."""
    months = pd.period_range("2017-01", periods=18, freq="M")
    revenue = pd.Series(
        [1000 + index * 100 for index in range(18)],
        dtype="int64",
    )

    return pd.DataFrame(
        {
            "month": months,
            "revenue": revenue,
        }
    )


def test_training_is_reproducible() -> None:
    """Test that repeated training produces identical predictions."""
    monthly_dataset = make_monthly_dataset()

    model_one = train_forecasting_model(
        monthly_dataset,
        alpha=1.0,
        min_training_rows=1,
    )

    model_two = train_forecasting_model(
        monthly_dataset,
        alpha=1.0,
        min_training_rows=1,
    )

    forecasting_dataset = monthly_dataset.copy()
    forecasting_dataset["month"] = forecasting_dataset[
        "month"
    ].astype("period[M]")

    from bizintel.ml.features import build_forecasting_features

    features = build_forecasting_features(forecasting_dataset)

    complete_features = features.dropna(
        subset=FEATURE_COLUMNS
    ).reset_index(drop=True)

    X = complete_features[FEATURE_COLUMNS]

    predictions_one = model_one.predict(X)
    predictions_two = model_two.predict(X)

    np.testing.assert_array_equal(
        predictions_one,
        predictions_two,
    )


def test_training_produces_same_model_coefficients() -> None:
    """Test that repeated Ridge training produces identical coefficients."""
    monthly_dataset = make_monthly_dataset()

    model_one = train_forecasting_model(
        monthly_dataset,
        alpha=1.0,
    )

    model_two = train_forecasting_model(
        monthly_dataset,
        alpha=1.0,
    )

    ridge_one = model_one.named_steps["ridge"]
    ridge_two = model_two.named_steps["ridge"]

    np.testing.assert_array_equal(
        ridge_one.coef_,
        ridge_two.coef_,
    )

    assert ridge_one.intercept_ == ridge_two.intercept_