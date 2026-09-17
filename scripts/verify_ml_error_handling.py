"""Real-data verification for production ML error handling."""

import tempfile
from pathlib import Path

import pandas as pd

from bizintel.data.pipeline import build_canonical_datasets
from bizintel.ml.artifacts import (
    load_model_artifact,
    save_model_artifact,
)
from bizintel.ml.forecast import generate_next_month_ridge_forecast
from bizintel.ml.metadata import (
    create_model_metadata,
    load_model_metadata,
    save_model_metadata,
)
from bizintel.ml.training import train_forecasting_model


def main() -> None:
    """Run real-data ML error-handling verification."""
    raw_data_dir = Path("data/raw")

    print("Loading and building canonical Olist datasets...")

    datasets = build_canonical_datasets(
        raw_data_dir
    )

    order_items = datasets["order_items"]

    monthly_dataset = (
        order_items.assign(
            month=order_items["shipping_limit_at"].dt.to_period("M")
        )
        .groupby("month", as_index=False)["price_minor"]
        .sum()
        .rename(columns={"price_minor": "revenue"})
    )

    print(
        f"Loaded monthly dataset: {len(monthly_dataset)} months"
    )

    model = train_forecasting_model(
        monthly_dataset,
        min_training_rows=1,
    )

    print("PASS: Valid forecasting model training")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        artifact_path = temp_path / "forecasting_model.joblib"
        metadata_path = temp_path / "forecasting_model.json"

        save_model_artifact(
            model,
            artifact_path,
        )

        if not artifact_path.exists():
            raise AssertionError(
                "Model artifact was not created"
            )

        loaded_model = load_model_artifact(
            artifact_path
        )

        if type(loaded_model) is not type(model):
            raise AssertionError(
                "Loaded model type does not match trained model"
            )

        print("PASS: Model artifact save/load")

        metadata = create_model_metadata(
            model_name="forecasting_ridge",
            model_version="1.0.0",
            model_type="Ridge",
            target="monthly_merchandise_revenue",
            feature_columns=[
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
            ],
            training_start=str(
                monthly_dataset["month"].min()
            ),
            training_end=str(
                monthly_dataset["month"].max()
            ),
            hyperparameters={"alpha": 1.0},
        )

        save_model_metadata(
            metadata,
            metadata_path,
        )

        if not metadata_path.exists():
            raise AssertionError(
                "Model metadata was not created"
            )

        loaded_metadata = load_model_metadata(
            metadata_path
        )

        if loaded_metadata != metadata:
            raise AssertionError(
                "Loaded metadata does not match saved metadata"
            )

        print("PASS: Model metadata save/load")

    try:
        train_forecasting_model(
            monthly_dataset,
            min_training_rows=10_000,
        )
    except ValueError as exc:
        expected_message = (
            "Insufficient complete rows available for model training"
        )

        if expected_message not in str(exc):
            raise AssertionError(
                "Unexpected insufficient-training error message"
            ) from exc

        print("PASS: Insufficient training rows rejected")
    else:
        raise AssertionError(
            "Insufficient training rows were not rejected"
        )

    try:
        load_model_artifact(
            Path("artifacts") / "does_not_exist.joblib"
        )
    except FileNotFoundError as exc:
        if "Model artifact not found" not in str(exc):
            raise AssertionError(
                "Unexpected missing-artifact error message"
            ) from exc

        print("PASS: Missing model artifact rejected")
    else:
        raise AssertionError(
            "Missing model artifact was not rejected"
        )

    try:
        load_model_metadata(
            Path("artifacts") / "does_not_exist.json"
        )
    except FileNotFoundError as exc:
        if "Model metadata not found" not in str(exc):
            raise AssertionError(
                "Unexpected missing-metadata error message"
            ) from exc

        print("PASS: Missing model metadata rejected")
    else:
        raise AssertionError(
            "Missing model metadata was not rejected"
        )

    empty_dataset = pd.DataFrame(
        {
            "month": pd.PeriodIndex([], freq="M"),
            "revenue": pd.Series(dtype="int64"),
        }
    )

    try:
        generate_next_month_ridge_forecast(
            empty_dataset
        )
    except ValueError as exc:
        if "forecasting_dataset must not be empty" not in str(exc):
            raise AssertionError(
                "Unexpected empty-dataset error message"
            ) from exc

        print("PASS: Empty forecasting dataset rejected")
    else:
        raise AssertionError(
            "Empty forecasting dataset was not rejected"
        )

    duplicate_dataset = monthly_dataset.copy()

    duplicate_row = duplicate_dataset.iloc[[0]].copy()

    duplicate_dataset = pd.concat(
        [
            duplicate_dataset,
            duplicate_row,
        ],
        ignore_index=True,
    )

    try:
        generate_next_month_ridge_forecast(
            duplicate_dataset
        )
    except ValueError as exc:
        if "month values must be unique" not in str(exc):
            raise AssertionError(
                "Unexpected duplicate-month error message"
            ) from exc

        print("PASS: Duplicate month values rejected")
    else:
        raise AssertionError(
            "Duplicate month values were not rejected"
        )

    print()
    print("========================================")
    print("ML ERROR HANDLING VERIFICATION PASSED")
    print("========================================")


if __name__ == "__main__":
    main()