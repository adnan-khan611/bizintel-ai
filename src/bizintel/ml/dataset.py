"""Dataset builders for BizIntel AI forecasting."""

import pandas as pd


def build_monthly_revenue_dataset(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    include_partial_months: bool = False,
    start_month: str | None = None,
    end_month: str | None = None,
) -> pd.DataFrame:
    """Build a monthly merchandise revenue dataset for forecasting.

    Revenue is calculated from canonical order items and grouped by the
    calendar month of the corresponding order date.

    By default, the first and last observed calendar months are excluded
    because boundary months may contain partial source-data coverage.

    Optional start_month and end_month parameters allow callers to explicitly
    select a known complete forecasting window.
    """
    required_order_columns = {"order_id", "order_date"}
    missing_order_columns = required_order_columns - set(orders.columns)

    if missing_order_columns:
        missing = ", ".join(sorted(missing_order_columns))
        raise ValueError(f"Missing required columns: {missing}")

    required_item_columns = {"order_id", "price_minor"}
    missing_item_columns = required_item_columns - set(order_items.columns)

    if missing_item_columns:
        missing = ", ".join(sorted(missing_item_columns))
        raise ValueError(f"Missing required columns: {missing}")

    if not pd.api.types.is_datetime64_any_dtype(orders["order_date"]):
        raise TypeError("order_date must be a datetime column")

    if start_month is not None:
        start_period = pd.Period(start_month, freq="M")
    else:
        start_period = None

    if end_month is not None:
        end_period = pd.Period(end_month, freq="M")
    else:
        end_period = None

    if start_period is not None and end_period is not None:
        if start_period > end_period:
            raise ValueError("start_month must be before or equal to end_month")

    data = orders[["order_id", "order_date"]].copy()
    data["month"] = data["order_date"].dt.to_period("M")

    if start_period is not None:
        data = data[data["month"] >= start_period]

    if end_period is not None:
        data = data[data["month"] <= end_period]

    if data.empty:
        return pd.DataFrame(
            {
                "month": pd.PeriodIndex([], freq="M"),
                "revenue": pd.Series(dtype="int64"),
            }
        )

    merged = data.merge(
        order_items[["order_id", "price_minor"]],
        on="order_id",
        how="inner",
    )

    monthly_revenue = (
        merged.groupby("month", as_index=False)["price_minor"]
        .sum()
        .rename(columns={"price_minor": "revenue"})
    )

    complete_month_index = pd.period_range(
        start=data["month"].min(),
        end=data["month"].max(),
        freq="M",
    )

    monthly_revenue = (
        monthly_revenue.set_index("month")
        .reindex(complete_month_index, fill_value=0)
        .rename_axis("month")
        .reset_index()
    )

    monthly_revenue["revenue"] = monthly_revenue["revenue"].astype("int64")

    if not include_partial_months:
        first_month = data["month"].min()
        last_month = data["month"].max()

        monthly_revenue = monthly_revenue[
            ~monthly_revenue["month"].isin([first_month, last_month])
        ].reset_index(drop=True)

    return monthly_revenue