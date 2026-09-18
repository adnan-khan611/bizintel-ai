"""Analytics API response schemas for BizIntel AI."""

from typing import Any

from pydantic import BaseModel


class AnalyticsSummaryResponse(BaseModel):
    """Response schema for the combined analytics summary."""

    revenue: dict[str, Any]
    orders: dict[str, Any]
    customers: dict[str, Any]
    products: dict[str, Any]
    growth: dict[str, Any]