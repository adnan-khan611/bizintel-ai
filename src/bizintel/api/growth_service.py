"""Growth service layer for BizIntel AI."""

from pathlib import Path
from typing import Any

import pandas as pd

from bizintel.analytics.growth import (
    calculate_monthly_orders,
    calculate_monthly_revenue,
    calculate_monthly_unique_customers,
    calculate_order_growth,
    calculate_revenue_growth,
)
from bizintel.api.analytics_data import load_analytics_datasets
from bizintel.api.growth_schemas import GrowthResponse


def _series_to_dict(series: pd.Series) -> dict[str, Any]:
    """Convert a pandas Series into a JSON-compatible dictionary."""
    return {
        str(key): value.item()
        if hasattr(value, "item")
        else value
        for key, value in series.items()
    }


def get_growth_analytics(
    processed_data_dir: Path,
) -> GrowthResponse:
    """Load datasets and build the growth response."""
    datasets = load_analytics_datasets(
        processed_data_dir
    )

    orders = datasets["orders"]
    order_items = datasets["order_items"]

    monthly_revenue = calculate_monthly_revenue(
        orders,
        order_items,
    )
    monthly_orders = calculate_monthly_orders(
        orders
    )
    monthly_unique_customers = (
        calculate_monthly_unique_customers(orders)
    )
    revenue_growth = calculate_revenue_growth(
        monthly_revenue
    )
    order_growth = calculate_order_growth(
        monthly_orders
    )

    return GrowthResponse(
        monthly_revenue=_series_to_dict(
            monthly_revenue
        ),
        monthly_orders=_series_to_dict(
            monthly_orders
        ),
        monthly_unique_customers=_series_to_dict(
            monthly_unique_customers
        ),
        revenue_growth=_series_to_dict(
            revenue_growth
        ),
        order_growth=_series_to_dict(
            order_growth
        ),
    )