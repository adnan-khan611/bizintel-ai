"""Integration tests for the growth analytics API."""

from fastapi.testclient import TestClient

from bizintel.main import app


def test_growth_endpoint_works_with_real_processed_data() -> None:
    """Growth endpoint should work with actual processed datasets."""
    client = TestClient(app)

    response = client.get("/analytics/growth")

    assert response.status_code == 200

    body = response.json()

    assert isinstance(
        body["monthly_revenue"],
        dict,
    )

    assert isinstance(
        body["monthly_orders"],
        dict,
    )

    assert isinstance(
        body["monthly_unique_customers"],
        dict,
    )

    assert isinstance(
        body["revenue_growth"],
        dict,
    )

    assert isinstance(
        body["order_growth"],
        dict,
    )

    assert len(body["monthly_revenue"]) > 0
    assert len(body["monthly_orders"]) > 0
    assert len(body["monthly_unique_customers"]) > 0