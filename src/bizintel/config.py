"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class Settings:
    """Runtime settings for the API and ML services."""

    app_name: str = ""
    environment: str = ""

    forecasting_model_version: str = ""
    forecasting_ridge_alpha: float = 0.0
    forecasting_min_training_rows: int = 0

    def __post_init__(self) -> None:
        """Load and validate environment-based settings."""
        object.__setattr__(
            self,
            "app_name",
            getenv("APP_NAME", "BizIntel AI"),
        )
        object.__setattr__(
            self,
            "environment",
            getenv("APP_ENV", "development"),
        )
        object.__setattr__(
            self,
            "forecasting_model_version",
            getenv("FORECASTING_MODEL_VERSION", "1.0.0"),
        )
        object.__setattr__(
            self,
            "forecasting_ridge_alpha",
            float(getenv("FORECASTING_RIDGE_ALPHA", "1.0")),
        )
        object.__setattr__(
            self,
            "forecasting_min_training_rows",
            int(getenv("FORECASTING_MIN_TRAINING_ROWS", "10")),
        )

        if self.forecasting_ridge_alpha <= 0:
            raise ValueError(
                "FORECASTING_RIDGE_ALPHA must be greater than 0"
            )

        if self.forecasting_min_training_rows < 1:
            raise ValueError(
                "FORECASTING_MIN_TRAINING_ROWS must be greater than 0"
            )


settings = Settings()