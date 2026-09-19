"""Integration tests for the revenue analytics API."""

from fastapi.testclient import TestClient

from bizintel.main import app


def test_revenue_endpoint_with_real_processed_data() -> None:
    """Revenue endpoint should work with real canonical Parquet data."""
    client = TestClient(app)

    response = client.get("/analytics/revenue")

    assert response.status_code == 200

    body = response.json()

    assert set(body) == {
        "merchandise_revenue_minor",
        "freight_value_minor",
        "payment_value_minor",
    }

    assert body["merchandise_revenue_minor"] > 0
    assert body["freight_value_minor"] > 0
    assert body["payment_value_minor"] > 0