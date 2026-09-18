"""Integration tests for the analytics summary API."""

from fastapi.testclient import TestClient

from bizintel.main import app


def test_analytics_summary_endpoint_with_real_processed_data() -> None:
    """Analytics endpoint should work with real canonical Parquet data."""
    client = TestClient(app)

    response = client.get("/analytics/summary")

    assert response.status_code == 200

    body = response.json()

    assert set(body) == {
        "revenue",
        "orders",
        "customers",
        "products",
        "growth",
    }

    assert body["revenue"]["merchandise_revenue_minor"] > 0
    assert body["revenue"]["freight_value_minor"] > 0
    assert body["revenue"]["payment_value_minor"] > 0

    assert body["orders"]["total_orders"] > 0
    assert body["orders"]["delivered_orders"] > 0
    assert body["orders"]["canceled_orders"] >= 0
    assert body["orders"]["unavailable_orders"] >= 0

    assert body["customers"]["unique_customers"] > 0
    assert body["customers"]["orders_per_customer"] > 0

    assert body["products"]["total_products"] > 0

    assert body["growth"]["monthly_revenue"]
    assert body["growth"]["monthly_orders"]
    assert body["growth"]["monthly_unique_customers"]