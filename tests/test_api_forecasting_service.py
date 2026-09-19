"""Tests for the forecasting API service."""

from pathlib import Path

import pytest

from bizintel.api.forecasting_service import get_forecast


def test_get_forecast_returns_forecast_response(
    processed_data_dir: Path,
) -> None:
    """Forecast service should return a valid forecast response."""
    response = get_forecast(processed_data_dir)

    assert response.forecast_month
    assert isinstance(response.forecast_revenue, float)


@pytest.fixture
def processed_data_dir() -> Path:
    """Return the local processed data directory."""
    return Path("data/processed")