"""Tests for forecasting machine learning models."""

import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from bizintel.ml.features import FEATURE_COLUMNS
from bizintel.ml.model import predict_ridge_model, train_ridge_model


def make_forecasting_dataset() -> pd.DataFrame:
    """Create a small dataset containing all forecasting features."""
    months = pd.period_range(
        start="2017-01",
        periods=15,
        freq="M",
    )

    rows = []

    for index, month in enumerate(months):
        row = {
            "month": month,
            "revenue": float((index + 1) * 1000),
        }

        for feature_index, feature in enumerate(FEATURE_COLUMNS):
            row[feature] = float(index + feature_index + 1)

        rows.append(row)

    return pd.DataFrame(rows)


def test_train_ridge_model_returns_fitted_pipeline() -> None:
    """Ridge training should return a fitted scaling pipeline."""
    dataset = make_forecasting_dataset()

    model = train_ridge_model(dataset)

    assert isinstance(model, Pipeline)
    assert "scaler" in model.named_steps
    assert "ridge" in model.named_steps

    scaler = model.named_steps["scaler"]
    ridge = model.named_steps["ridge"]

    assert hasattr(scaler, "scale_")
    assert hasattr(ridge, "coef_")
    assert len(ridge.coef_) == len(FEATURE_COLUMNS)


def test_train_ridge_model_accepts_custom_alpha() -> None:
    """Ridge training should accept a positive regularization value."""
    dataset = make_forecasting_dataset()

    model = train_ridge_model(dataset, alpha=10.0)

    ridge = model.named_steps["ridge"]

    assert ridge.alpha == 10.0


def test_train_ridge_model_rejects_invalid_alpha() -> None:
    """Ridge training should reject non-positive alpha."""
    dataset = make_forecasting_dataset()

    with pytest.raises(ValueError, match="alpha must be greater than 0"):
        train_ridge_model(dataset, alpha=0)


def test_train_ridge_model_rejects_missing_columns() -> None:
    """Training should fail when required features are missing."""
    dataset = make_forecasting_dataset().drop(columns=["revenue_lag_1"])

    with pytest.raises(ValueError, match="Missing required columns"):
        train_ridge_model(dataset)


def test_train_ridge_model_rejects_empty_training_data() -> None:
    """Training should fail when no complete rows are available."""
    dataset = make_forecasting_dataset()

    dataset[FEATURE_COLUMNS] = float("nan")

    with pytest.raises(
        ValueError,
        match="No complete rows available for model training",
    ):
        train_ridge_model(dataset)


def test_predict_ridge_model_returns_forecast_series() -> None:
    """Prediction should return a forecast Series."""
    dataset = make_forecasting_dataset()

    model = train_ridge_model(dataset)
    forecast = predict_ridge_model(model, dataset)

    assert isinstance(forecast, pd.Series)
    assert forecast.name == "forecast"
    assert len(forecast) == len(dataset)
    assert forecast.index.equals(dataset.index)


def test_predict_ridge_model_rejects_missing_features() -> None:
    """Prediction should fail when a required feature is missing."""
    dataset = make_forecasting_dataset()

    model = train_ridge_model(dataset)

    prediction_data = dataset.drop(columns=["revenue_lag_1"])

    with pytest.raises(ValueError, match="Missing required columns"):
        predict_ridge_model(model, prediction_data)


def test_predict_ridge_model_produces_numeric_predictions() -> None:
    """Predictions should contain numeric values."""
    dataset = make_forecasting_dataset()

    model = train_ridge_model(dataset)
    forecast = predict_ridge_model(model, dataset)

    assert pd.api.types.is_numeric_dtype(forecast)
    assert forecast.notna().all()