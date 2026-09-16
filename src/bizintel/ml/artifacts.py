"""Model artifact persistence utilities for BizIntel AI forecasting."""

from pathlib import Path

from joblib import dump, load
from sklearn.pipeline import Pipeline


def save_model_artifact(
    model: Pipeline,
    artifact_path: str | Path,
) -> Path:
    """Save a trained forecasting model to a local artifact file."""
    if not isinstance(model, Pipeline):
        raise TypeError("model must be a scikit-learn Pipeline")

    path = Path(artifact_path)

    if path.suffix.lower() != ".joblib":
        raise ValueError("artifact_path must use the .joblib extension")

    path.parent.mkdir(parents=True, exist_ok=True)

    dump(model, path)

    return path


def load_model_artifact(
    artifact_path: str | Path,
) -> Pipeline:
    """Load a trained forecasting model from a joblib artifact."""
    path = Path(artifact_path)

    if path.suffix.lower() != ".joblib":
        raise ValueError("artifact_path must use the .joblib extension")

    if not path.exists():
        raise FileNotFoundError(
            f"Model artifact not found: {path}"
        )

    model = load(path)

    if not isinstance(model, Pipeline):
        raise TypeError(
            "Loaded model artifact must contain a scikit-learn Pipeline"
        )

    return model