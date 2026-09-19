"""Growth API response schemas for BizIntel AI."""

from typing import Any

from pydantic import BaseModel


class GrowthResponse(BaseModel):
    """Response schema for growth analytics."""

    monthly_revenue: dict[str, Any]
    monthly_orders: dict[str, Any]
    monthly_unique_customers: dict[str, Any]
    revenue_growth: dict[str, Any]
    order_growth: dict[str, Any]