"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class Settings:
    """Runtime settings for the API service."""

    app_name: str = getenv("APP_NAME", "BizIntel AI")
    environment: str = getenv("APP_ENV", "development")


settings = Settings()
