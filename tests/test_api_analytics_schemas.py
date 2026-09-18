"""Tests for analytics API response schemas."""

from bizintel.api.analytics_schemas import AnalyticsSummaryResponse


def test_analytics_summary_response_accepts_summary_sections() -> None:
    """Analytics summary should accept all required sections."""
    response = AnalyticsSummaryResponse(
        revenue={
            "merchandise_revenue_minor": 1000,
            "freight_value_minor": 200,
            "payment_value_minor": 1200,
        },
        orders={
            "total_orders": 10,
            "delivered_orders": 8,
            "canceled_orders": 1,
            "unavailable_orders": 1,
        },
        customers={
            "unique_customers": 9,
            "orders_per_customer": 1.11,
        },
        products={
            "total_products": 5,
            "products_by_category": {},
            "product_revenue": {},
            "product_order_items": {},
        },
        growth={
            "monthly_revenue": {},
            "monthly_orders": {},
            "monthly_unique_customers": {},
            "revenue_growth": {},
            "order_growth": {},
        },
    )

    assert response.revenue["merchandise_revenue_minor"] == 1000
    assert response.orders["total_orders"] == 10
    assert response.customers["unique_customers"] == 9
    assert response.products["total_products"] == 5


def test_analytics_summary_response_serializes_to_dict() -> None:
    """Analytics summary should serialize using the expected sections."""
    response = AnalyticsSummaryResponse(
        revenue={},
        orders={},
        customers={},
        products={},
        growth={},
    )

    result = response.model_dump()

    assert set(result) == {
        "revenue",
        "orders",
        "customers",
        "products",
        "growth",
    }