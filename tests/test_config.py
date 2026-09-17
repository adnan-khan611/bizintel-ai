"""Tests for application configuration."""

import pytest

from bizintel.config import Settings


def test_settings_defaults() -> None:
    """Test default application and forecasting settings."""
    settings = Settings()

    assert settings.app_name == "BizIntel AI"
    assert settings.environment == "development"
    assert settings.forecasting_model_version == "1.0.0"
    assert settings.forecasting_ridge_alpha == 1.0
    assert settings.forecasting_min_training_rows == 10


def test_settings_environment_overrides(monkeypatch) -> None:
    """Test that environment variables override default settings."""
    monkeypatch.setenv("APP_NAME", "Test BizIntel")
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("FORECASTING_MODEL_VERSION", "2.0.0")
    monkeypatch.setenv("FORECASTING_RIDGE_ALPHA", "2.5")
    monkeypatch.setenv("FORECASTING_MIN_TRAINING_ROWS", "15")

    settings = Settings()

    assert settings.app_name == "Test BizIntel"
    assert settings.environment == "production"
    assert settings.forecasting_model_version == "2.0.0"
    assert settings.forecasting_ridge_alpha == 2.5
    assert settings.forecasting_min_training_rows == 15
    
def test_settings_rejects_invalid_ridge_alpha(monkeypatch) -> None:
    """Test that non-positive Ridge alpha is rejected."""
    monkeypatch.setenv("FORECASTING_RIDGE_ALPHA", "0")

    with pytest.raises(
        ValueError,
        match="FORECASTING_RIDGE_ALPHA must be greater than 0",
    ):
        Settings()


def test_settings_rejects_invalid_min_training_rows(
    monkeypatch,
) -> None:
    """Test that non-positive training rows are rejected."""
    monkeypatch.setenv("FORECASTING_MIN_TRAINING_ROWS", "0")

    with pytest.raises(
        ValueError,
        match="FORECASTING_MIN_TRAINING_ROWS must be greater than 0",
    ):
        Settings()