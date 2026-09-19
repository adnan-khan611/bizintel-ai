"""Customers service layer for BizIntel AI."""

from pathlib import Path
from typing import Any

import pandas as pd

from bizintel.analytics.customers import (
    calculate_customer_order_counts,
    calculate_customer_order_distribution,
    calculate_orders_per_customer,
    calculate_unique_customers,
)
from bizintel.api.analytics_data import load_analytics_datasets
from bizintel.api.customers_schemas import CustomersResponse


def _series_to_dict(series: pd.Series) -> dict[str, Any]:
    """Convert a pandas Series into a JSON-compatible dictionary."""
    return {
        str(key): value.item()
        if hasattr(value, "item")
        else value
        for key, value in series.items()
    }


def get_customers_analytics(
    processed_data_dir: Path,
) -> CustomersResponse:
    """Load customer data and build the customers response."""
    datasets = load_analytics_datasets(
        processed_data_dir
    )

    customers = datasets["customers"]
    orders = datasets["orders"]

    unique_customers = calculate_unique_customers(
        customers
    )
    orders_per_customer = calculate_orders_per_customer(
        orders,
        customers,
    )
    customer_order_counts = calculate_customer_order_counts(
        orders
    )
    customer_order_distribution = (
        calculate_customer_order_distribution(orders)
    )

    return CustomersResponse(
        unique_customers=unique_customers,
        orders_per_customer=orders_per_customer,
        customer_order_counts=_series_to_dict(
            customer_order_counts
        ),
        customer_order_distribution=_series_to_dict(
            customer_order_distribution
        ),
    )