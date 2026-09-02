"""Tests for service health endpoints."""

from fastapi.testclient import TestClient

from bizintel.main import app


def test_health_endpoint_returns_ok() -> None:
    """The health endpoint confirms the service is available."""
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
