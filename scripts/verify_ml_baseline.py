"""Verify the naive forecasting baseline against the Olist dataset."""

from pathlib import Path

import pandas as pd

from bizintel.ml.baseline import naive_forecast
from bizintel.ml.dataset import build_monthly_revenue_dataset

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ORDERS_FILE = PROJECT_ROOT / "data" / "processed" / "orders.parquet"
ORDER_ITEMS_FILE = (
    PROJECT_ROOT / "data" / "processed" / "order_items.parquet"
)


def main() -> None:
    """Run naive baseline verification on canonical datasets."""

    orders = pd.read_parquet(ORDERS_FILE)
    order_items = pd.read_parquet(ORDER_ITEMS_FILE)

    monthly_dataset = build_monthly_revenue_dataset(
        orders=orders,
        order_items=order_items,
        start_month="2016-10",
        end_month="2018-08",
        include_partial_months=True,
    )

    forecast = naive_forecast(monthly_dataset)

    verification = monthly_dataset.copy()
    verification["forecast"] = forecast

    verification["error"] = (
        verification["revenue"] - verification["forecast"]
    )

    print("ML Baseline Verification")
    print("=" * 60)

    print("\nDataset:")
    print(f"  Months: {len(monthly_dataset):,}")
    print(f"  First Month: {monthly_dataset['month'].min()}")
    print(f"  Last Month: {monthly_dataset['month'].max()}")

    print("\nForecast Preview:")
    print(
        verification[
            ["month", "revenue", "forecast", "error"]
        ].to_string(index=False)
    )

    print("\nBaseline Checks:")

    first_forecast_missing = pd.isna(
        verification.loc[0, "forecast"]
    )

    print(
        f"  First Forecast Is Missing: "
        f"{first_forecast_missing}"
    )

    forecast_values = (
        verification["forecast"]
        .iloc[1:]
        .to_numpy()
    )

    previous_revenue_values = (
        verification["revenue"]
        .iloc[:-1]
        .to_numpy()
    )

    forecast_matches_previous = (
        forecast_values == previous_revenue_values
    ).all()

    print(
        f"  Forecast Equals Previous Month Revenue: "
        f"{forecast_matches_previous}"
    )

    print(
        f"  Forecast Rows: "
        f"{verification['forecast'].notna().sum():,}"
    )

    print(
        f"  Missing Forecast Rows: "
        f"{verification['forecast'].isna().sum():,}"
    )

    print("\nLatest Historical Forecast:")

    latest = verification.iloc[-1]

    print(f"  Forecast Month: {latest['month']}")
    print(
        f"  Actual Revenue: "
        f"R$ {latest['revenue'] / 100:,.2f}"
    )
    print(
        f"  Forecast Revenue: "
        f"R$ {latest['forecast'] / 100:,.2f}"
    )
    print(
        f"  Forecast Error: "
        f"R$ {latest['error'] / 100:,.2f}"
    )

    print("\nData Integrity:")

    print(
        f"  Duplicate Months: "
        f"{verification['month'].duplicated().sum()}"
    )

    print(
        f"  Chronologically Sorted: "
        f"{verification['month'].is_monotonic_increasing}"
    )

    print(
        f"  Missing Actual Revenue Rows: "
        f"{verification['revenue'].isna().sum()}"
    )

    print("\nNote:")
    print(
        "  The naive baseline forecasts each month using only "
        "the previous month's actual revenue."
    )
    print(
        "  The first month has no previous month, so its forecast "
        "is intentionally missing."
    )


if __name__ == "__main__":
    main()