"""Tests for production ML error handling."""

from pathlib import Path

import pandas as pd
import pytest
from sklearn.linear_model import Ridge

from bizintel.ml.artifacts import (
    load_model_artifact,
    save_model_artifact,
)
from bizintel.ml.forecast import generate_next_month_ridge_forecast
from bizintel.ml.metadata import (
    ModelMetadata,
    create_model_metadata,
    load_model_metadata,
    save_model_metadata,
)
from bizintel.ml.training import train_forecasting_model


def make_valid_monthly_dataset() -> pd.DataFrame:
    """Create a valid monthly dataset for error-handling tests."""
    return pd.DataFrame(
        {
            "month": pd.period_range(
                start="2023-01",
                periods=18,
                freq="M",
            ),
            "revenue": [
                1000,
                1100,
                1200,
                1300,
                1400,
                1500,
                1600,
                1700,
                1800,
                1900,
                2000,
                2100,
                2200,
                2300,
                2400,
                2500,
                2600,
                2700,
            ],
        }
    )


def make_valid_metadata() -> ModelMetadata:
    """Create valid model metadata."""
    return create_model_metadata(
        model_name="forecasting_ridge",
        model_version="1.0.0",
        model_type="Ridge",
        target="monthly_merchandise_revenue",
        feature_columns=[
            "revenue_lag_1",
            "revenue_lag_2",
        ],
        training_start="2016-10",
        training_end="2018-08",
        hyperparameters={"alpha": 1.0},
    )


def test_training_rejects_invalid_min_training_rows() -> None:
    """Training must reject a non-positive minimum row requirement."""
    dataset = make_valid_monthly_dataset()

    with pytest.raises(
        ValueError,
        match="min_training_rows must be greater than 0",
    ):
        train_forecasting_model(
            dataset,
            min_training_rows=0,
        )


def test_training_rejects_insufficient_training_rows() -> None:
    """Training must reject insufficient complete feature rows."""
    dataset = make_valid_monthly_dataset()

    with pytest.raises(
        ValueError,
        match="Insufficient complete rows available for model training",
    ):
        train_forecasting_model(
            dataset,
            min_training_rows=100,
        )


def test_save_artifact_rejects_non_pipeline_model(
    tmp_path: Path,
) -> None:
    """Artifact saving must reject non-Pipeline models."""
    model = Ridge(alpha=1.0)

    with pytest.raises(
        TypeError,
        match="model must be a scikit-learn Pipeline",
    ):
        save_model_artifact(
            model,
            tmp_path / "model.joblib",
        )


def test_save_artifact_rejects_wrong_extension(
    tmp_path: Path,
) -> None:
    """Artifact saving must require the joblib extension."""
    dataset = make_valid_monthly_dataset()
    model = train_forecasting_model(dataset)

    with pytest.raises(
        ValueError,
        match="artifact_path must use the .joblib extension",
    ):
        save_model_artifact(
            model,
            tmp_path / "model.pkl",
        )


def test_load_artifact_rejects_missing_file(
    tmp_path: Path,
) -> None:
    """Artifact loading must fail clearly for a missing file."""
    with pytest.raises(
        FileNotFoundError,
        match="Model artifact not found",
    ):
        load_model_artifact(
            tmp_path / "missing.joblib",
        )


def test_load_artifact_rejects_wrong_extension(
    tmp_path: Path,
) -> None:
    """Artifact loading must require the joblib extension."""
    with pytest.raises(
        ValueError,
        match="artifact_path must use the .joblib extension",
    ):
        load_model_artifact(
            tmp_path / "model.pkl",
        )


def test_create_metadata_rejects_empty_model_name() -> None:
    """Metadata creation must require a model name."""
    with pytest.raises(
        ValueError,
        match="model_name must not be empty",
    ):
        create_model_metadata(
            model_name="",
            model_version="1.0.0",
            model_type="Ridge",
            target="revenue",
            feature_columns=["revenue_lag_1"],
            training_start="2016-10",
            training_end="2018-08",
            hyperparameters={"alpha": 1.0},
        )


def test_create_metadata_rejects_empty_feature_columns() -> None:
    """Metadata creation must require feature columns."""
    with pytest.raises(
        ValueError,
        match="feature_columns must not be empty",
    ):
        create_model_metadata(
            model_name="forecasting_ridge",
            model_version="1.0.0",
            model_type="Ridge",
            target="revenue",
            feature_columns=[],
            training_start="2016-10",
            training_end="2018-08",
            hyperparameters={"alpha": 1.0},
        )


def test_save_metadata_rejects_invalid_metadata_type(
    tmp_path: Path,
) -> None:
    """Metadata saving must reject unrelated objects."""
    with pytest.raises(
        TypeError,
        match="metadata must be a ModelMetadata instance",
    ):
        save_model_metadata(
            {"model_name": "invalid"},
            tmp_path / "metadata.json",
        )


def test_save_metadata_rejects_wrong_extension(
    tmp_path: Path,
) -> None:
    """Metadata saving must require the JSON extension."""
    metadata = make_valid_metadata()

    with pytest.raises(
        ValueError,
        match="metadata_path must use the .json extension",
    ):
        save_model_metadata(
            metadata,
            tmp_path / "metadata.txt",
        )


def test_load_metadata_rejects_missing_file(
    tmp_path: Path,
) -> None:
    """Metadata loading must fail clearly for a missing file."""
    with pytest.raises(
        FileNotFoundError,
        match="Model metadata not found",
    ):
        load_model_metadata(
            tmp_path / "missing.json",
        )


def test_load_metadata_rejects_wrong_extension(
    tmp_path: Path,
) -> None:
    """Metadata loading must require the JSON extension."""
    with pytest.raises(
        ValueError,
        match="metadata_path must use the .json extension",
    ):
        load_model_metadata(
            tmp_path / "metadata.txt",
        )


def test_forecast_rejects_empty_dataset() -> None:
    """Forecast generation must reject an empty dataset."""
    dataset = pd.DataFrame(
        {
            "month": pd.PeriodIndex([], freq="M"),
            "revenue": pd.Series(dtype="int64"),
        }
    )

    with pytest.raises(
        ValueError,
        match="forecasting_dataset must not be empty",
    ):
        generate_next_month_ridge_forecast(dataset)


def test_forecast_rejects_duplicate_months() -> None:
    """Forecast generation must reject duplicate months."""
    dataset = make_valid_monthly_dataset()

    duplicate_row = dataset.iloc[[0]].copy()
    dataset = pd.concat(
        [dataset, duplicate_row],
        ignore_index=True,
    )

    with pytest.raises(
        ValueError,
        match="month values must be unique",
    ):
        generate_next_month_ridge_forecast(dataset)