"""Tests for the forecasting API endpoint."""

from fastapi.testclient import TestClient

from bizintel.main import app


def test_forecasting_endpoint_returns_success() -> None:
    """Forecasting endpoint should return a valid forecast."""
    client = TestClient(app)

    response = client.get("/analytics/forecast")

    assert response.status_code == 200

    data = response.json()

    assert "forecast_month" in data
    assert "forecast_revenue" in data

    assert isinstance(data["forecast_month"], str)
    assert isinstance(data["forecast_revenue"], float)