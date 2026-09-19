"""Forecasting API response schemas for BizIntel AI."""

from pydantic import BaseModel


class ForecastResponse(BaseModel):
    """Response schema for a revenue forecast."""

    forecast_month: str
    forecast_revenue: float