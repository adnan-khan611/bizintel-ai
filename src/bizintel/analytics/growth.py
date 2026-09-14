"""Growth analytics for BizIntel AI."""

import pandas as pd


def _create_month_index(
    order_dates: pd.Series,
) -> pd.PeriodIndex:
    """Create a complete calendar-month index from the available dates."""
    if order_dates.empty:
        return pd.PeriodIndex([], freq="M", name="month")

    start_month = order_dates.min().to_period("M")
    end_month = order_dates.max().to_period("M")

    return pd.period_range(
        start=start_month,
        end=end_month,
        freq="M",
        name="month",
    )


def calculate_monthly_revenue(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
) -> pd.Series:
    """Calculate monthly merchandise revenue in minor currency units."""
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

    data = orders[["order_id", "order_date"]].copy()

    data["month"] = data["order_date"].dt.to_period("M")

    merged = data.merge(
        order_items[["order_id", "price_minor"]],
        on="order_id",
        how="inner",
    )

    monthly_revenue = merged.groupby("month")["price_minor"].sum()

    month_index = _create_month_index(data["order_date"])

    return monthly_revenue.reindex(month_index, fill_value=0).astype("int64")


def calculate_monthly_orders(orders: pd.DataFrame) -> pd.Series:
    """Calculate the number of distinct orders for each month."""
    required_columns = {"order_id", "order_date"}
    missing_columns = required_columns - set(orders.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    data = orders[["order_id", "order_date"]].copy()
    data["month"] = data["order_date"].dt.to_period("M")

    monthly_orders = data.groupby("month")["order_id"].nunique()

    month_index = _create_month_index(data["order_date"])

    return monthly_orders.reindex(month_index, fill_value=0).astype("int64")


def calculate_monthly_unique_customers(orders: pd.DataFrame) -> pd.Series:
    """Calculate the number of unique customers for each month."""
    required_columns = {"customer_id", "order_date"}
    missing_columns = required_columns - set(orders.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    data = orders[["customer_id", "order_date"]].copy()
    data["month"] = data["order_date"].dt.to_period("M")

    monthly_customers = data.groupby("month")["customer_id"].nunique()

    month_index = _create_month_index(data["order_date"])

    return monthly_customers.reindex(month_index, fill_value=0).astype("int64")


def calculate_revenue_growth(monthly_revenue: pd.Series) -> pd.Series:
    """Calculate month-over-month revenue growth percentage."""
    previous_month = monthly_revenue.shift(1)

    growth = (monthly_revenue - previous_month) / previous_month * 100

    return growth.where(previous_month != 0)


def calculate_order_growth(monthly_orders: pd.Series) -> pd.Series:
    """Calculate month-over-month order growth percentage."""
    previous_month = monthly_orders.shift(1)

    growth = (monthly_orders - previous_month) / previous_month * 100

    return growth.where(previous_month != 0)