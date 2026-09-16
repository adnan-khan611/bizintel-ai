"""Training workflow utilities for BizIntel AI forecasting."""

import pandas as pd
from sklearn.pipeline import Pipeline

from bizintel.ml.features import FEATURE_COLUMNS, build_forecasting_features
from bizintel.ml.model import train_ridge_model


def train_forecasting_model(
    monthly_dataset: pd.DataFrame,
    alpha: float = 1.0,
    min_training_rows: int = 1,
) -> Pipeline:
    """Build forecasting features and train the Ridge forecasting model."""
    if min_training_rows < 1:
        raise ValueError("min_training_rows must be greater than 0")

    forecasting_dataset = build_forecasting_features(monthly_dataset)

    complete_dataset = forecasting_dataset.dropna(
        subset=FEATURE_COLUMNS + ["revenue"]
    ).reset_index(drop=True)

    if len(complete_dataset) < min_training_rows:
        raise ValueError(
            "Insufficient complete rows available for model training"
        )

    return train_ridge_model(
        complete_dataset,
        alpha=alpha,
    )