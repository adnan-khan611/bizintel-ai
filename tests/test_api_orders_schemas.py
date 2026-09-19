"""Tests for orders API response schemas."""

from bizintel.api.orders_schemas import OrdersResponse


def test_orders_response_accepts_valid_values() -> None:
    """OrdersResponse should accept valid order analytics."""
    response = OrdersResponse(
        total_orders=100,
        delivered_orders=90,
        canceled_orders=5,
        unavailable_orders=5,
        orders_by_status={
            "delivered": 90,
            "canceled": 5,
            "unavailable": 5,
        },
    )

    assert response.total_orders == 100
    assert response.delivered_orders == 90
    assert response.canceled_orders == 5
    assert response.unavailable_orders == 5
    assert response.orders_by_status == {
        "delivered": 90,
        "canceled": 5,
        "unavailable": 5,
    }


def test_orders_response_serializes_to_dict() -> None:
    """OrdersResponse should serialize to a dictionary."""
    response = OrdersResponse(
        total_orders=100,
        delivered_orders=90,
        canceled_orders=5,
        unavailable_orders=5,
        orders_by_status={
            "delivered": 90,
            "canceled": 5,
            "unavailable": 5,
        },
    )

    result = response.model_dump()

    assert result == {
        "total_orders": 100,
        "delivered_orders": 90,
        "canceled_orders": 5,
        "unavailable_orders": 5,
        "orders_by_status": {
            "delivered": 90,
            "canceled": 5,
            "unavailable": 5,
        },
    }