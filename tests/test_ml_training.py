"""Tests for the forecasting training workflow."""

import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from bizintel.ml.features import FEATURE_COLUMNS
from bizintel.ml.training import train_forecasting_model


def make_monthly_dataset() -> pd.DataFrame:
    """Create enough monthly observations for complete features."""
    months = pd.period_range(
        start="2017-01",
        periods=15,
        freq="M",
    )

    return pd.DataFrame(
        {
            "month": months,
            "revenue": [
                float((index + 1) * 1000)
                for index in range(len(months))
            ],
        }
    )


def test_train_forecasting_model_returns_pipeline() -> None:
    """Training workflow should return a fitted pipeline."""
    dataset = make_monthly_dataset()

    model = train_forecasting_model(dataset)

    assert isinstance(model, Pipeline)
    assert "scaler" in model.named_steps
    assert "ridge" in model.named_steps


def test_train_forecasting_model_uses_forecasting_features() -> None:
    """Training workflow should train using the feature contract."""
    dataset = make_monthly_dataset()

    model = train_forecasting_model(dataset)

    ridge = model.named_steps["ridge"]

    assert len(ridge.coef_) == len(FEATURE_COLUMNS)


def test_train_forecasting_model_accepts_custom_alpha() -> None:
    """Training workflow should pass alpha to the Ridge model."""
    dataset = make_monthly_dataset()

    model = train_forecasting_model(
        dataset,
        alpha=10.0,
    )

    assert model.named_steps["ridge"].alpha == 10.0


def test_train_forecasting_model_rejects_invalid_minimum_rows() -> None:
    """Training workflow should reject invalid minimum row settings."""
    dataset = make_monthly_dataset()

    with pytest.raises(
        ValueError,
        match="min_training_rows must be greater than 0",
    ):
        train_forecasting_model(
            dataset,
            min_training_rows=0,
        )


def test_train_forecasting_model_rejects_insufficient_rows() -> None:
    """Training workflow should reject insufficient complete rows."""
    dataset = make_monthly_dataset()

    with pytest.raises(
        ValueError,
        match="Insufficient complete rows available for model training",
    ):
        train_forecasting_model(
            dataset,
            min_training_rows=4,
        )