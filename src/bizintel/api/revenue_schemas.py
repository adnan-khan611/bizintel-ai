"""Revenue API response schemas for BizIntel AI."""

from pydantic import BaseModel


class RevenueResponse(BaseModel):
    """Response schema for revenue analytics."""

    merchandise_revenue_minor: int
    freight_value_minor: int
    payment_value_minor: int