"""API response schemas for BizIntel AI."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response schema for the health endpoint."""

    status: str