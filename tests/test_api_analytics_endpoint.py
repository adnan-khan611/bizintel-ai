"""Tests for the analytics summary API endpoint."""

from fastapi.testclient import TestClient

from bizintel.config import settings
from bizintel.main import app


def test_analytics_summary_endpoint_returns_expected_contract(
    monkeypatch,
) -> None:
    """Analytics summary endpoint should return the expected contract."""
    expected_summary = {
        "revenue": {
            "merchandise_revenue_minor": 1000,
            "freight_value_minor": 200,
            "payment_value_minor": 1200,
        },
        "orders": {
            "total_orders": 10,
            "delivered_orders": 8,
            "canceled_orders": 1,
            "unavailable_orders": 1,
        },
        "customers": {
            "unique_customers": 9,
            "orders_per_customer": 1.11,
        },
        "products": {
            "total_products": 5,
            "products_by_category": {},
            "product_revenue": {},
            "product_order_items": {},
        },
        "growth": {
            "monthly_revenue": {},
            "monthly_orders": {},
            "monthly_unique_customers": {},
            "revenue_growth": {},
            "order_growth": {},
        },
    }

    def fake_get_analytics_summary(processed_data_dir):
        assert processed_data_dir == settings.processed_data_dir
        return expected_summary

    monkeypatch.setattr(
        "bizintel.main.get_analytics_summary",
        fake_get_analytics_summary,
    )

    client = TestClient(app)

    response = client.get("/analytics/summary")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "application/json"
    )

    body = response.json()

    assert set(body) == {
        "revenue",
        "orders",
        "customers",
        "products",
        "growth",
    }

    assert body["revenue"]["merchandise_revenue_minor"] == 1000
    assert body["orders"]["total_orders"] == 10
    assert body["customers"]["unique_customers"] == 9
    assert body["products"]["total_products"] == 5