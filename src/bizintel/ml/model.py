"""Machine learning forecasting models for BizIntel AI."""

import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from bizintel.ml.contracts import (
    get_feature_matrix,
    validate_inference_features,
)
from bizintel.ml.features import FEATURE_COLUMNS


def train_ridge_model(
    forecasting_dataset: pd.DataFrame,
    alpha: float = 1.0,
) -> Pipeline:
    """Train a scaled Ridge regression model on forecasting features."""
    required_columns = {"revenue", *FEATURE_COLUMNS}
    missing_columns = required_columns - set(forecasting_dataset.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    if alpha <= 0:
        raise ValueError("alpha must be greater than 0")

    data = forecasting_dataset.dropna(
        subset=FEATURE_COLUMNS + ["revenue"]
    ).copy()

    if data.empty:
        raise ValueError("No complete rows available for model training")

    X = get_feature_matrix(data)
    y = data["revenue"]

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("ridge", Ridge(alpha=alpha)),
        ]
    )

    model.fit(X, y)

    return model


def predict_ridge_model(
    model: Pipeline,
    forecasting_dataset: pd.DataFrame,
) -> pd.Series:
    """Generate revenue predictions using a trained Ridge model."""
    validate_inference_features(forecasting_dataset)

    X = get_feature_matrix(forecasting_dataset)
    predictions = model.predict(X)

    return pd.Series(
        predictions,
        index=forecasting_dataset.index,
        name="forecast",
    )