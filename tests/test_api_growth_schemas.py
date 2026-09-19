"""Tests for growth API response schemas."""

from bizintel.api.growth_schemas import GrowthResponse


def test_growth_response_accepts_valid_values() -> None:
    """GrowthResponse should accept valid growth analytics."""
    response = GrowthResponse(
        monthly_revenue={
            "2017-01": 1000,
            "2017-02": 1200,
        },
        monthly_orders={
            "2017-01": 100,
            "2017-02": 120,
        },
        monthly_unique_customers={
            "2017-01": 90,
            "2017-02": 105,
        },
        revenue_growth={
            "2017-02": 0.20,
        },
        order_growth={
            "2017-02": 0.20,
        },
    )

    assert response.monthly_revenue == {
        "2017-01": 1000,
        "2017-02": 1200,
    }
    assert response.monthly_orders == {
        "2017-01": 100,
        "2017-02": 120,
    }
    assert response.monthly_unique_customers == {
        "2017-01": 90,
        "2017-02": 105,
    }
    assert response.revenue_growth == {
        "2017-02": 0.20,
    }
    assert response.order_growth == {
        "2017-02": 0.20,
    }


def test_growth_response_serializes_to_dict() -> None:
    """GrowthResponse should serialize to a dictionary."""
    response = GrowthResponse(
        monthly_revenue={
            "2017-01": 1000,
            "2017-02": 1200,
        },
        monthly_orders={
            "2017-01": 100,
            "2017-02": 120,
        },
        monthly_unique_customers={
            "2017-01": 90,
            "2017-02": 105,
        },
        revenue_growth={
            "2017-02": 0.20,
        },
        order_growth={
            "2017-02": 0.20,
        },
    )

    assert response.model_dump() == {
        "monthly_revenue": {
            "2017-01": 1000,
            "2017-02": 1200,
        },
        "monthly_orders": {
            "2017-01": 100,
            "2017-02": 120,
        },
        "monthly_unique_customers": {
            "2017-01": 90,
            "2017-02": 105,
        },
        "revenue_growth": {
            "2017-02": 0.20,
        },
        "order_growth": {
            "2017-02": 0.20,
        },
    }