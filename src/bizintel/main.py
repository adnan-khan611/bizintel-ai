"""FastAPI application entry point."""

from fastapi import FastAPI

from bizintel.api.schemas import HealthResponse
from bizintel.config import settings


def create_app() -> FastAPI:
    """Create and configure the BizIntel AI API application."""
    app = FastAPI(title=settings.app_name)

    @app.get(
        "/health",
        response_model=HealthResponse,
    )
    def health_check() -> HealthResponse:
        """Return the service health status."""
        return HealthResponse(status="ok")

    return app


app = create_app()