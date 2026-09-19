"""Orders API response schemas for BizIntel AI."""

from typing import Any

from pydantic import BaseModel


class OrdersResponse(BaseModel):
    """Response schema for order analytics."""

    total_orders: int
    delivered_orders: int
    canceled_orders: int
    unavailable_orders: int
    orders_by_status: dict[str, Any]