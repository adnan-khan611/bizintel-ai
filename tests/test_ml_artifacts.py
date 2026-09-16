"""Tests for forecasting model artifact persistence."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from bizintel.ml.artifacts import (
    load_model_artifact,
    save_model_artifact,
)
from bizintel.ml.features import build_forecasting_features
from bizintel.ml.model import train_ridge_model


def make_forecasting_dataset() -> pd.DataFrame:
    """Create a small forecasting dataset for artifact tests."""
    months = pd.period_range("2017-01", periods=18, freq="M")
    revenue = pd.Series(
        [1000 + index * 100 for index in range(18)],
        dtype="int64",
    )

    monthly_dataset = pd.DataFrame(
        {
            "month": months,
            "revenue": revenue,
        }
    )

    return build_forecasting_features(monthly_dataset)


def train_test_model() -> tuple[Pipeline, pd.DataFrame]:
    """Build a trained Ridge model and complete test dataset."""
    forecasting_dataset = make_forecasting_dataset()

    model = train_ridge_model(forecasting_dataset)

    complete_dataset = forecasting_dataset.dropna(
        subset=["revenue"]
        + [
            "revenue_lag_1",
            "revenue_lag_2",
            "revenue_lag_3",
            "revenue_lag_6",
            "revenue_lag_12",
            "revenue_rolling_mean_3",
            "revenue_rolling_mean_6",
            "revenue_rolling_std_3",
            "revenue_rolling_std_6",
            "month_number",
            "quarter",
            "year",
        ]
    ).reset_index(drop=True)

    return model, complete_dataset


def test_save_model_artifact_creates_joblib_file(tmp_path: Path) -> None:
    """Test that a trained model is saved to a joblib file."""
    model, _ = train_test_model()
    artifact_path = tmp_path / "model.joblib"

    returned_path = save_model_artifact(model, artifact_path)

    assert returned_path == artifact_path
    assert artifact_path.exists()
    assert artifact_path.is_file()


def test_load_model_artifact_returns_pipeline(tmp_path: Path) -> None:
    """Test that a saved model can be loaded as a Pipeline."""
    model, _ = train_test_model()
    artifact_path = tmp_path / "model.joblib"

    save_model_artifact(model, artifact_path)
    loaded_model = load_model_artifact(artifact_path)

    assert isinstance(loaded_model, Pipeline)


def test_loaded_model_predictions_match_original(
    tmp_path: Path,
) -> None:
    """Test that loading preserves model predictions."""
    model, forecasting_dataset = train_test_model()
    artifact_path = tmp_path / "model.joblib"

    save_model_artifact(model, artifact_path)
    loaded_model = load_model_artifact(artifact_path)

    feature_columns = [
        "revenue_lag_1",
        "revenue_lag_2",
        "revenue_lag_3",
        "revenue_lag_6",
        "revenue_lag_12",
        "revenue_rolling_mean_3",
        "revenue_rolling_mean_6",
        "revenue_rolling_std_3",
        "revenue_rolling_std_6",
        "month_number",
        "quarter",
        "year",
    ]

    X = forecasting_dataset[feature_columns]

    original_predictions = model.predict(X)
    loaded_predictions = loaded_model.predict(X)

    np.testing.assert_allclose(
        original_predictions,
        loaded_predictions,
    )


def test_save_model_artifact_rejects_non_pipeline(
    tmp_path: Path,
) -> None:
    """Test that saving a non-Pipeline object raises TypeError."""
    artifact_path = tmp_path / "model.joblib"

    with pytest.raises(TypeError, match="model must be a scikit-learn Pipeline"):
        save_model_artifact("not a model", artifact_path)


def test_save_model_artifact_rejects_invalid_extension(
    tmp_path: Path,
) -> None:
    """Test that saving with a non-joblib extension raises ValueError."""
    model, _ = train_test_model()
    artifact_path = tmp_path / "model.pkl"

    with pytest.raises(
        ValueError,
        match="artifact_path must use the .joblib extension",
    ):
        save_model_artifact(model, artifact_path)


def test_load_model_artifact_rejects_invalid_extension(
    tmp_path: Path,
) -> None:
    """Test that loading with a non-joblib extension raises ValueError."""
    artifact_path = tmp_path / "model.pkl"

    with pytest.raises(
        ValueError,
        match="artifact_path must use the .joblib extension",
    ):
        load_model_artifact(artifact_path)


def test_load_model_artifact_raises_for_missing_file(
    tmp_path: Path,
) -> None:
    """Test that a missing artifact raises FileNotFoundError."""
    artifact_path = tmp_path / "missing_model.joblib"

    with pytest.raises(
        FileNotFoundError,
        match="Model artifact not found",
    ):
        load_model_artifact(artifact_path)