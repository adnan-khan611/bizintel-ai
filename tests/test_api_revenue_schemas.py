"""Tests for revenue API response schemas."""

from bizintel.api.revenue_schemas import RevenueResponse


def test_revenue_response_accepts_valid_values() -> None:
    """RevenueResponse should accept valid revenue values."""
    response = RevenueResponse(
        merchandise_revenue_minor=1000,
        freight_value_minor=200,
        payment_value_minor=1200,
    )

    assert response.merchandise_revenue_minor == 1000
    assert response.freight_value_minor == 200
    assert response.payment_value_minor == 1200


def test_revenue_response_serializes_to_dict() -> None:
    """RevenueResponse should serialize to a dictionary."""
    response = RevenueResponse(
        merchandise_revenue_minor=1000,
        freight_value_minor=200,
        payment_value_minor=1200,
    )

    result = response.model_dump()

    assert result == {
        "merchandise_revenue_minor": 1000,
        "freight_value_minor": 200,
        "payment_value_minor": 1200,
    }