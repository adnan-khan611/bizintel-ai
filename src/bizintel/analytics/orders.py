"""Order analytics for BizIntel AI."""

import pandas as pd


def calculate_total_orders(orders: pd.DataFrame) -> int:
    """Calculate the total number of distinct orders."""
    if "order_id" not in orders.columns:
        raise ValueError("Missing required column: order_id")

    return int(orders["order_id"].nunique())


def calculate_orders_by_status(orders: pd.DataFrame) -> pd.Series:
    """Calculate the number of orders for each order status."""
    required_columns = {"order_id", "order_status"}

    missing_columns = required_columns - set(orders.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    return orders.groupby("order_status")["order_id"].nunique().sort_index()


def calculate_delivered_orders(orders: pd.DataFrame) -> int:
    """Calculate the number of delivered orders."""
    if "order_id" not in orders.columns:
        raise ValueError("Missing required column: order_id")

    if "order_status" not in orders.columns:
        raise ValueError("Missing required column: order_status")

    delivered = orders.loc[
        orders["order_status"] == "delivered",
        "order_id",
    ]

    return int(delivered.nunique())


def calculate_canceled_orders(orders: pd.DataFrame) -> int:
    """Calculate the number of canceled orders."""
    if "order_id" not in orders.columns:
        raise ValueError("Missing required column: order_id")

    if "order_status" not in orders.columns:
        raise ValueError("Missing required column: order_status")

    canceled = orders.loc[
        orders["order_status"] == "canceled",
        "order_id",
    ]

    return int(canceled.nunique())


def calculate_unavailable_orders(orders: pd.DataFrame) -> int:
    """Calculate the number of unavailable orders."""
    if "order_id" not in orders.columns:
        raise ValueError("Missing required column: order_id")

    if "order_status" not in orders.columns:
        raise ValueError("Missing required column: order_status")

    unavailable = orders.loc[
        orders["order_status"] == "unavailable",
        "order_id",
    ]

    return int(unavailable.nunique())