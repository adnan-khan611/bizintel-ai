"""Customer analytics for BizIntel AI."""

import pandas as pd


def calculate_unique_customers(customers: pd.DataFrame) -> int:
    """Calculate the number of distinct customers."""
    if "customer_id" not in customers.columns:
        raise ValueError("Missing required column: customer_id")

    return int(customers["customer_id"].nunique())


def calculate_orders_per_customer(
    orders: pd.DataFrame,
    customers: pd.DataFrame,
) -> float:
    """Calculate the average number of orders per customer."""
    if "order_id" not in orders.columns:
        raise ValueError("Missing required column: order_id")

    if "customer_id" not in orders.columns:
        raise ValueError("Missing required column: customer_id")

    if "customer_id" not in customers.columns:
        raise ValueError("Missing required column: customer_id")

    total_orders = orders["order_id"].nunique()
    unique_customers = customers["customer_id"].nunique()

    if unique_customers == 0:
        return 0.0

    return total_orders / unique_customers


def calculate_customer_order_counts(
    orders: pd.DataFrame,
) -> pd.Series:
    """Calculate the number of distinct orders for each customer."""
    required_columns = {"order_id", "customer_id"}

    missing_columns = required_columns - set(orders.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    return (
        orders.groupby("customer_id")["order_id"]
        .nunique()
        .sort_values(ascending=False)
    )


def calculate_customer_order_distribution(
    orders: pd.DataFrame,
) -> pd.Series:
    """Calculate how many customers have each number of orders."""
    customer_order_counts = calculate_customer_order_counts(orders)

    return customer_order_counts.value_counts().sort_index()


def calculate_top_customers_by_orders(
    orders: pd.DataFrame,
    limit: int = 10,
) -> pd.Series:
    """Return customers with the highest number of distinct orders."""
    if limit < 1:
        raise ValueError("limit must be at least 1")

    customer_order_counts = calculate_customer_order_counts(orders)

    return customer_order_counts.head(limit)