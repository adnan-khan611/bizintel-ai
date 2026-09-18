"""Tests for the health API response contract."""

from fastapi.testclient import TestClient

from bizintel.main import app


def test_health_endpoint_returns_expected_contract() -> None:
    """Health endpoint should return the documented response contract."""
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith(
        "application/json"
    )

    body = response.json()

    assert set(body) == {"status"}
    assert isinstance(body["status"], str)
    assert body["status"] == "ok"


def test_health_endpoint_exposes_openapi_schema() -> None:
    """Health endpoint should expose its response model in OpenAPI."""
    client = TestClient(app)

    response = client.get("/openapi.json")

    assert response.status_code == 200

    openapi = response.json()

    health_operation = openapi["paths"]["/health"]["get"]

    assert health_operation["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["$ref"] == "#/components/schemas/HealthResponse"

    assert "HealthResponse" in openapi["components"]["schemas"]