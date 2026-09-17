"""Verify forecasting leakage protection on the Olist dataset."""

from pathlib import Path

import pandas as pd

from bizintel.ml.dataset import build_monthly_revenue_dataset
from bizintel.ml.features import build_forecasting_features

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ORDERS_PATH = PROJECT_ROOT / "data" / "raw" / "olist_orders_dataset.csv"
ORDER_ITEMS_PATH = (
    PROJECT_ROOT / "data" / "raw" / "olist_order_items_dataset.csv"
)


LAG_AND_ROLLING_FEATURES = [
    "revenue_lag_1",
    "revenue_lag_2",
    "revenue_lag_3",
    "revenue_lag_6",
    "revenue_lag_12",
    "revenue_rolling_mean_3",
    "revenue_rolling_mean_6",
    "revenue_rolling_std_3",
    "revenue_rolling_std_6",
]


def main() -> None:
    """Verify leakage protection using the real Olist dataset."""
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
        subset=LAG_AND_ROLLING_FEATURES
    ).reset_index(drop=True)

    print(f"Complete feature rows: {len(complete_dataset)}")

    if len(monthly_dataset) != 23:
        raise AssertionError(
            "Expected 23 complete monthly observations"
        )

    if str(monthly_dataset["month"].min()) != "2016-10":
        raise AssertionError(
            "Unexpected forecasting window start"
        )

    if str(monthly_dataset["month"].max()) != "2018-08":
        raise AssertionError(
            "Unexpected forecasting window end"
        )

    if len(complete_dataset) != 11:
        raise AssertionError(
            "Expected 11 complete feature rows"
        )

    print("Checking future-revenue isolation...")

    modified_dataset = monthly_dataset.copy()

    last_index = modified_dataset.index[-1]
    modified_dataset.loc[last_index, "revenue"] = 999999999

    modified_features = build_forecasting_features(
        modified_dataset
    )

    original_features = build_forecasting_features(
        monthly_dataset
    )

    comparison_end = len(monthly_dataset) - 2

    pd.testing.assert_frame_equal(
        original_features.loc[
            :comparison_end,
            LAG_AND_ROLLING_FEATURES,
        ].reset_index(drop=True),
        modified_features.loc[
            :comparison_end,
            LAG_AND_ROLLING_FEATURES,
        ].reset_index(drop=True),
    )

    print(
        "Changing the final month's revenue does not change "
        "earlier forecasting features."
    )

    print("Checking current-month leakage...")

    current_index = len(monthly_dataset) - 2

    current_features = original_features.loc[
        current_index,
        LAG_AND_ROLLING_FEATURES,
    ]

    future_revenue = monthly_dataset.loc[
        last_index,
        "revenue",
    ]

    if current_features.isna().any():
        raise AssertionError(
            "Current feature row unexpectedly contains missing values"
        )

    if (current_features == future_revenue).any():
        raise AssertionError(
            "A forecasting feature matches future revenue"
        )

    print("Current-month features do not use future revenue.")

    print("Checking lag-1 relationship...")

    for index in range(1, len(original_features)):
        expected_previous_revenue = monthly_dataset.loc[
            index - 1,
            "revenue",
        ]

        actual_lag_1 = original_features.loc[
            index,
            "revenue_lag_1",
        ]

        if actual_lag_1 != expected_previous_revenue:
            raise AssertionError(
                "revenue_lag_1 does not match the previous month's revenue"
            )

    print("Lag-1 feature uses only the previous month's revenue.")

    print("Checking rolling mean-3 relationship...")

    for index in range(3, len(original_features)):
        previous_values = monthly_dataset.loc[
            index - 3:index - 1,
            "revenue",
        ]

        expected_mean = previous_values.mean()

        actual_mean = original_features.loc[
            index,
            "revenue_rolling_mean_3",
        ]

        if actual_mean != expected_mean:
            raise AssertionError(
                "Three-month rolling mean includes unexpected data"
            )

    print("Rolling mean-3 uses only the previous three months.")

    print("Leakage protection verification PASSED.")


if __name__ == "__main__":
    main()