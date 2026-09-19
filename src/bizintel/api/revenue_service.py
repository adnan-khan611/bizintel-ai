"""Revenue service layer for BizIntel AI."""

from pathlib import Path

from bizintel.analytics.revenue import (
    calculate_freight_value,
    calculate_merchandise_revenue,
    calculate_payment_value,
)
from bizintel.api.analytics_data import load_analytics_datasets
from bizintel.api.revenue_schemas import RevenueResponse


def get_revenue_analytics(
    processed_data_dir: Path,
) -> RevenueResponse:
    """Load revenue datasets and build the revenue response."""
    datasets = load_analytics_datasets(
        processed_data_dir
    )

    merchandise_revenue = calculate_merchandise_revenue(
        datasets["order_items"]
    )
    freight_value = calculate_freight_value(
        datasets["order_items"]
    )
    payment_value = calculate_payment_value(
        datasets["order_payments"]
    )

    return RevenueResponse(
        merchandise_revenue_minor=merchandise_revenue,
        freight_value_minor=freight_value,
        payment_value_minor=payment_value,
    )