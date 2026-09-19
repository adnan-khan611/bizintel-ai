"""Tests for the orders analytics API endpoint."""

from fastapi.testclient import TestClient

from bizintel.api.orders_schemas import OrdersResponse
from bizintel.config import settings
from bizintel.main import app


def test_orders_endpoint_returns_expected_contract(
    monkeypatch,
) -> None:
    """Orders endpoint should return the expected response contract."""
    expected_response = OrdersResponse(
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

    def fake_get_orders_analytics(processed_data_dir):
        assert processed_data_dir == settings.processed_data_dir
        return expected_response

    monkeypatch.setattr(
        "bizintel.main.get_orders_analytics",
        fake_get_orders_analytics,
    )

    client = TestClient(app)

    response = client.get("/analytics/orders")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "application/json"
    )

    body = response.json()

    assert set(body) == {
        "total_orders",
        "delivered_orders",
        "canceled_orders",
        "unavailable_orders",
        "orders_by_status",
    }

    assert body["total_orders"] == 100
    assert body["delivered_orders"] == 90
    assert body["canceled_orders"] == 5
    assert body["unavailable_orders"] == 5
    assert body["orders_by_status"] == {
        "delivered": 90,
        "canceled": 5,
        "unavailable": 5,
    }


def test_orders_endpoint_exposes_openapi_schema() -> None:
    """Orders endpoint should expose its response model in OpenAPI."""
    client = TestClient(app)

    response = client.get("/openapi.json")

    assert response.status_code == 200

    openapi = response.json()

    orders_operation = openapi["paths"]["/analytics/orders"]["get"]

    assert orders_operation["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["$ref"] == "#/components/schemas/OrdersResponse"

    assert "OrdersResponse" in openapi["components"]["schemas"]