"""Integration tests for the customers analytics API."""

from fastapi.testclient import TestClient

from bizintel.main import app


def test_customers_endpoint_works_with_real_processed_data() -> None:
    """Customers endpoint should work with actual processed datasets."""
    client = TestClient(app)

    response = client.get("/analytics/customers")

    assert response.status_code == 200

    body = response.json()

    assert body["unique_customers"] == 96096
    assert body["orders_per_customer"] > 0

    assert isinstance(
        body["customer_order_counts"],
        dict,
    )

    assert isinstance(
        body["customer_order_distribution"],
        dict,
    )