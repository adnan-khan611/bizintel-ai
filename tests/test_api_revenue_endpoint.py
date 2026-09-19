"""Tests for the revenue analytics API endpoint."""

from fastapi.testclient import TestClient

from bizintel.api.revenue_schemas import RevenueResponse
from bizintel.config import settings
from bizintel.main import app


def test_revenue_endpoint_returns_expected_contract(
    monkeypatch,
) -> None:
    """Revenue endpoint should return the expected response contract."""
    expected_response = RevenueResponse(
        merchandise_revenue_minor=1000,
        freight_value_minor=200,
        payment_value_minor=1200,
    )

    def fake_get_revenue_analytics(processed_data_dir):
        assert processed_data_dir == settings.processed_data_dir
        return expected_response

    monkeypatch.setattr(
        "bizintel.main.get_revenue_analytics",
        fake_get_revenue_analytics,
    )

    client = TestClient(app)

    response = client.get("/analytics/revenue")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "application/json"
    )

    body = response.json()

    assert set(body) == {
        "merchandise_revenue_minor",
        "freight_value_minor",
        "payment_value_minor",
    }

    assert body["merchandise_revenue_minor"] == 1000
    assert body["freight_value_minor"] == 200
    assert body["payment_value_minor"] == 1200


def test_revenue_endpoint_exposes_openapi_schema() -> None:
    """Revenue endpoint should expose its response model in OpenAPI."""
    client = TestClient(app)

    response = client.get("/openapi.json")

    assert response.status_code == 200

    openapi = response.json()

    revenue_operation = openapi["paths"]["/analytics/revenue"]["get"]

    assert revenue_operation["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["$ref"] == "#/components/schemas/RevenueResponse"

    assert "RevenueResponse" in openapi["components"]["schemas"]