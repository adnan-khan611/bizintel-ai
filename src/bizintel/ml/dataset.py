"""Dataset builders for BizIntel AI forecasting."""

import pandas as pd


def build_monthly_revenue_dataset(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    include_partial_months: bool = False,
) -> pd.DataFrame:
    """Build a monthly merchandise revenue dataset for forecasting.

    Revenue is calculated from canonical order items and grouped by the
    calendar month of the corresponding order date.

    By default, incomplete boundary months are excluded because they do not
    represent a complete month's business activity.
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

    data = orders[["order_id", "order_date"]].copy()

    data["month"] = data["order_date"].dt.to_period("M")

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

    if monthly_revenue.empty:
        return pd.DataFrame(
            {
                "month": pd.PeriodIndex([], freq="M"),
                "revenue": pd.Series(dtype="int64"),
            }
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
        first_order_date = data["order_date"].min()
        last_order_date = data["order_date"].max()

        first_month = first_order_date.to_period("M")
        last_month = last_order_date.to_period("M")

        if first_order_date.day != 1:
            monthly_revenue = monthly_revenue[
                monthly_revenue["month"] != first_month
            ]

        last_day_of_month = last_order_date.days_in_month

        if last_order_date.day != last_day_of_month:
            monthly_revenue = monthly_revenue[
                monthly_revenue["month"] != last_month
            ]

        monthly_revenue = monthly_revenue.reset_index(drop=True)

    return monthly_revenue