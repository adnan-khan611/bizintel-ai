"""Tests for API error response schemas."""

from bizintel.api.errors import ErrorResponse


def test_error_response_accepts_valid_detail() -> None:
    """ErrorResponse should accept a valid error detail."""
    response = ErrorResponse(
        detail="Dataset not found"
    )

    assert response.detail == "Dataset not found"


def test_error_response_serializes_to_dict() -> None:
    """ErrorResponse should serialize to a dictionary."""
    response = ErrorResponse(
        detail="Dataset not found"
    )

    assert response.model_dump() == {
        "detail": "Dataset not found"
    }