"""Orders service layer for BizIntel AI."""

from pathlib import Path
from typing import Any

import pandas as pd

from bizintel.analytics.orders import (
    calculate_canceled_orders,
    calculate_delivered_orders,
    calculate_orders_by_status,
    calculate_total_orders,
    calculate_unavailable_orders,
)
from bizintel.api.analytics_data import load_analytics_datasets
from bizintel.api.orders_schemas import OrdersResponse


def _series_to_dict(series: pd.Series) -> dict[str, Any]:
    """Convert a pandas Series into a JSON-compatible dictionary."""
    return {
        str(key): value.item()
        if hasattr(value, "item")
        else value
        for key, value in series.items()
    }


def get_orders_analytics(
    processed_data_dir: Path,
) -> OrdersResponse:
    """Load order data and build the orders response."""
    datasets = load_analytics_datasets(
        processed_data_dir
    )

    orders = datasets["orders"]

    total_orders = calculate_total_orders(orders)
    delivered_orders = calculate_delivered_orders(orders)
    canceled_orders = calculate_canceled_orders(orders)
    unavailable_orders = calculate_unavailable_orders(orders)
    orders_by_status = calculate_orders_by_status(orders)

    return OrdersResponse(
        total_orders=total_orders,
        delivered_orders=delivered_orders,
        canceled_orders=canceled_orders,
        unavailable_orders=unavailable_orders,
        orders_by_status=_series_to_dict(
            orders_by_status
        ),
    )