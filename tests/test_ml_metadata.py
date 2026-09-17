"""Tests for model versioning and metadata utilities."""

from pathlib import Path

import pytest

from bizintel.ml.metadata import (
    ModelMetadata,
    create_model_metadata,
    load_model_metadata,
    save_model_metadata,
)


def make_metadata() -> ModelMetadata:
    """Create sample model metadata for tests."""
    return create_model_metadata(
        model_name="revenue_forecasting",
        model_version="1.0.0",
        model_type="ridge",
        target="monthly_merchandise_revenue",
        feature_columns=[
            "revenue_lag_1",
            "revenue_lag_2",
            "month_number",
        ],
        training_start="2016-10",
        training_end="2018-08",
        hyperparameters={
            "alpha": 1.0,
        },
    )


def test_create_model_metadata() -> None:
    """Test metadata creation."""
    metadata = make_metadata()

    assert metadata.model_name == "revenue_forecasting"
    assert metadata.model_version == "1.0.0"
    assert metadata.model_type == "ridge"
    assert metadata.target == "monthly_merchandise_revenue"
    assert metadata.feature_columns == [
        "revenue_lag_1",
        "revenue_lag_2",
        "month_number",
    ]
    assert metadata.training_start == "2016-10"
    assert metadata.training_end == "2018-08"
    assert metadata.hyperparameters == {"alpha": 1.0}


def test_create_model_metadata_copies_mutable_inputs() -> None:
    """Test that mutable input values are copied."""
    feature_columns = ["revenue_lag_1"]
    hyperparameters = {"alpha": 1.0}

    metadata = create_model_metadata(
        model_name="revenue_forecasting",
        model_version="1.0.0",
        model_type="ridge",
        target="monthly_merchandise_revenue",
        feature_columns=feature_columns,
        training_start="2016-10",
        training_end="2018-08",
        hyperparameters=hyperparameters,
    )

    feature_columns.append("month_number")
    hyperparameters["alpha"] = 2.0

    assert metadata.feature_columns == ["revenue_lag_1"]
    assert metadata.hyperparameters == {"alpha": 1.0}


def test_save_model_metadata_creates_json_file(
    tmp_path: Path,
) -> None:
    """Test that metadata is saved as JSON."""
    metadata = make_metadata()
    metadata_path = tmp_path / "forecasting_ridge.json"

    returned_path = save_model_metadata(
        metadata,
        metadata_path,
    )

    assert returned_path == metadata_path
    assert metadata_path.exists()
    assert metadata_path.is_file()


def test_load_model_metadata_returns_model_metadata(
    tmp_path: Path,
) -> None:
    """Test that saved metadata can be loaded."""
    metadata = make_metadata()
    metadata_path = tmp_path / "forecasting_ridge.json"

    save_model_metadata(metadata, metadata_path)

    loaded_metadata = load_model_metadata(metadata_path)

    assert isinstance(loaded_metadata, ModelMetadata)
    assert loaded_metadata == metadata


def test_save_and_load_preserves_all_metadata(
    tmp_path: Path,
) -> None:
    """Test that all metadata fields survive a save/load cycle."""
    metadata = make_metadata()
    metadata_path = tmp_path / "forecasting_ridge.json"

    save_model_metadata(metadata, metadata_path)
    loaded_metadata = load_model_metadata(metadata_path)

    assert loaded_metadata.model_name == metadata.model_name
    assert loaded_metadata.model_version == metadata.model_version
    assert loaded_metadata.model_type == metadata.model_type
    assert loaded_metadata.target == metadata.target
    assert loaded_metadata.feature_columns == metadata.feature_columns
    assert loaded_metadata.training_start == metadata.training_start
    assert loaded_metadata.training_end == metadata.training_end
    assert loaded_metadata.hyperparameters == metadata.hyperparameters


def test_create_model_metadata_rejects_empty_required_fields() -> None:
    """Test that required string fields cannot be empty."""
    with pytest.raises(ValueError, match="model_name must not be empty"):
        create_model_metadata(
            model_name="",
            model_version="1.0.0",
            model_type="ridge",
            target="revenue",
            feature_columns=["feature"],
            training_start="2016-10",
            training_end="2018-08",
            hyperparameters={"alpha": 1.0},
        )

    with pytest.raises(ValueError, match="model_version must not be empty"):
        create_model_metadata(
            model_name="revenue_forecasting",
            model_version="",
            model_type="ridge",
            target="revenue",
            feature_columns=["feature"],
            training_start="2016-10",
            training_end="2018-08",
            hyperparameters={"alpha": 1.0},
        )


def test_create_model_metadata_rejects_empty_feature_columns() -> None:
    """Test that feature columns cannot be empty."""
    with pytest.raises(
        ValueError,
        match="feature_columns must not be empty",
    ):
        create_model_metadata(
            model_name="revenue_forecasting",
            model_version="1.0.0",
            model_type="ridge",
            target="revenue",
            feature_columns=[],
            training_start="2016-10",
            training_end="2018-08",
            hyperparameters={"alpha": 1.0},
        )


def test_save_model_metadata_rejects_invalid_extension(
    tmp_path: Path,
) -> None:
    """Test that metadata must use the JSON extension."""
    metadata = make_metadata()
    metadata_path = tmp_path / "forecasting_ridge.joblib"

    with pytest.raises(
        ValueError,
        match="metadata_path must use the .json extension",
    ):
        save_model_metadata(metadata, metadata_path)


def test_load_model_metadata_raises_for_missing_file(
    tmp_path: Path,
) -> None:
    """Test that a missing metadata file raises FileNotFoundError."""
    metadata_path = tmp_path / "missing_metadata.json"

    with pytest.raises(
        FileNotFoundError,
        match="Model metadata not found",
    ):
        load_model_metadata(metadata_path)