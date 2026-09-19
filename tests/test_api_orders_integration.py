"""Integration tests for the orders analytics API."""

from fastapi.testclient import TestClient

from bizintel.main import app


def test_orders_endpoint_with_real_processed_data() -> None:
    """Orders endpoint should work with real canonical Parquet data."""
    client = TestClient(app)

    response = client.get("/analytics/orders")

    assert response.status_code == 200

    body = response.json()

    assert set(body) == {
        "total_orders",
        "delivered_orders",
        "canceled_orders",
        "unavailable_orders",
        "orders_by_status",
    }

    assert body["total_orders"] > 0
    assert body["delivered_orders"] > 0
    assert body["canceled_orders"] >= 0
    assert body["unavailable_orders"] >= 0

    assert body["orders_by_status"]
    assert isinstance(body["orders_by_status"], dict)