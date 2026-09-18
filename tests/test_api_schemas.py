"""Tests for API response schemas."""

from bizintel.api.schemas import HealthResponse


def test_health_response_accepts_valid_status() -> None:
    """HealthResponse should accept a valid status value."""
    response = HealthResponse(status="ok")

    assert response.status == "ok"


def test_health_response_serializes_to_dict() -> None:
    """HealthResponse should serialize to a dictionary."""
    response = HealthResponse(status="ok")

    assert response.model_dump() == {"status": "ok"}