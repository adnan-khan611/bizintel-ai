"""Verify the forecasting feature contract on the Olist dataset."""

from pathlib import Path

import pandas as pd

from bizintel.ml.contracts import (
    get_feature_matrix,
    validate_feature_columns,
    validate_inference_features,
)
from bizintel.ml.dataset import build_monthly_revenue_dataset
from bizintel.ml.features import (
    FEATURE_COLUMNS,
    build_forecasting_features,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ORDERS_PATH = PROJECT_ROOT / "data" / "raw" / "olist_orders_dataset.csv"
ORDER_ITEMS_PATH = (
    PROJECT_ROOT / "data" / "raw" / "olist_order_items_dataset.csv"
)


def main() -> None:
    """Verify the feature contract using the real Olist dataset."""
    print("Loading Olist data...")

    orders = pd.read_csv(
        ORDERS_PATH,
        parse_dates=["order_purchase_timestamp"],
    )

    order_items = pd.read_csv(ORDER_ITEMS_PATH)

    order_items["price_minor"] = (
        order_items["price"].mul(100).round().astype("int64")
    )

    orders = orders.rename(
        columns={"order_purchase_timestamp": "order_date"}
    )

    monthly_dataset = build_monthly_revenue_dataset(
        orders,
        order_items,
        include_partial_months=True,
        start_month="2016-10",
        end_month="2018-08",
    )

    print(f"Monthly observations: {len(monthly_dataset)}")
    print(f"Training window: {monthly_dataset['month'].min()}")
    print(f"Training window: {monthly_dataset['month'].max()}")

    forecasting_dataset = build_forecasting_features(
        monthly_dataset
    )

    complete_dataset = forecasting_dataset.dropna(
        subset=FEATURE_COLUMNS + ["revenue"]
    ).reset_index(drop=True)

    print(f"Complete feature rows: {len(complete_dataset)}")

    print("Validating feature columns...")
    validate_feature_columns(complete_dataset)

    feature_matrix = get_feature_matrix(complete_dataset)

    if list(feature_matrix.columns) != FEATURE_COLUMNS:
        raise AssertionError(
            "Feature matrix does not follow the canonical feature order"
        )

    print("Feature order matches the canonical contract.")

    non_numeric_columns = [
        column
        for column in FEATURE_COLUMNS
        if not pd.api.types.is_numeric_dtype(feature_matrix[column])
    ]

    if non_numeric_columns:
        raise AssertionError(
            "Non-numeric features found: "
            + ", ".join(non_numeric_columns)
        )

    print("All forecasting features are numeric.")

    print("Validating inference features...")
    validate_inference_features(complete_dataset)

    print("Inference feature validation PASSED.")

    print("Testing missing-feature rejection...")

    missing_feature_dataset = complete_dataset.drop(
        columns=["revenue_lag_1"]
    )

    try:
        validate_feature_columns(missing_feature_dataset)
    except ValueError as error:
        if "Missing required columns" not in str(error):
            raise AssertionError(
                "Missing-feature validation returned an unexpected error"
            ) from error
    else:
        raise AssertionError(
            "Missing feature was not rejected"
        )

    print("Missing-feature rejection PASSED.")

    print("Testing missing-value rejection...")

    missing_value_dataset = complete_dataset.copy()
    missing_value_dataset.loc[
        missing_value_dataset.index[0],
        "revenue_lag_1",
    ] = float("nan")

    try:
        validate_inference_features(missing_value_dataset)
    except ValueError as error:
        if "Forecasting features contain missing values" not in str(error):
            raise AssertionError(
                "Missing-value validation returned an unexpected error"
            ) from error
    else:
        raise AssertionError(
            "Missing inference value was not rejected"
        )

    print("Missing-value rejection PASSED.")

    print("Feature contract verification PASSED.")


if __name__ == "__main__":
    main()