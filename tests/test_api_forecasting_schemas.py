"""Tests for forecasting API response schemas."""

from bizintel.api.forecasting_schemas import ForecastResponse


def test_forecast_response_accepts_valid_values() -> None:
    """ForecastResponse should accept valid forecast values."""
    response = ForecastResponse(
        forecast_month="2018-09",
        forecast_revenue=85662.75,
    )

    assert response.forecast_month == "2018-09"
    assert response.forecast_revenue == 85662.75


def test_forecast_response_serializes_to_dict() -> None:
    """ForecastResponse should serialize to a dictionary."""
    response = ForecastResponse(
        forecast_month="2018-09",
        forecast_revenue=85662.75,
    )

    assert response.model_dump() == {
        "forecast_month": "2018-09",
        "forecast_revenue": 85662.75,
    }