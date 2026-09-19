"""Customers API response schemas for BizIntel AI."""

from typing import Any

from pydantic import BaseModel


class CustomersResponse(BaseModel):
    """Response schema for customer analytics."""

    unique_customers: int
    orders_per_customer: float
    customer_order_counts: dict[str, Any]
    customer_order_distribution: dict[str, Any]