"""Model versioning and metadata utilities for BizIntel AI."""

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModelMetadata:
    """Metadata describing a trained forecasting model."""

    model_name: str
    model_version: str
    model_type: str
    target: str
    feature_columns: list[str]
    training_start: str
    training_end: str
    hyperparameters: dict[str, float]


def create_model_metadata(
    model_name: str,
    model_version: str,
    model_type: str,
    target: str,
    feature_columns: list[str],
    training_start: str,
    training_end: str,
    hyperparameters: dict[str, float],
) -> ModelMetadata:
    """Create metadata for a trained forecasting model."""
    if not model_name.strip():
        raise ValueError("model_name must not be empty")

    if not model_version.strip():
        raise ValueError("model_version must not be empty")

    if not model_type.strip():
        raise ValueError("model_type must not be empty")

    if not target.strip():
        raise ValueError("target must not be empty")

    if not feature_columns:
        raise ValueError("feature_columns must not be empty")

    if not training_start.strip():
        raise ValueError("training_start must not be empty")

    if not training_end.strip():
        raise ValueError("training_end must not be empty")

    return ModelMetadata(
        model_name=model_name,
        model_version=model_version,
        model_type=model_type,
        target=target,
        feature_columns=list(feature_columns),
        training_start=training_start,
        training_end=training_end,
        hyperparameters=dict(hyperparameters),
    )


def save_model_metadata(
    metadata: ModelMetadata,
    metadata_path: str | Path,
) -> Path:
    """Save model metadata to a JSON file."""
    if not isinstance(metadata, ModelMetadata):
        raise TypeError("metadata must be a ModelMetadata instance")

    path = Path(metadata_path)

    if path.suffix.lower() != ".json":
        raise ValueError("metadata_path must use the .json extension")

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            asdict(metadata),
            file,
            indent=2,
            sort_keys=True,
        )
        file.write("\n")

    return path


def load_model_metadata(
    metadata_path: str | Path,
) -> ModelMetadata:
    """Load model metadata from a JSON file."""
    path = Path(metadata_path)

    if path.suffix.lower() != ".json":
        raise ValueError("metadata_path must use the .json extension")

    if not path.exists():
        raise FileNotFoundError(
            f"Model metadata not found: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return ModelMetadata(**data)