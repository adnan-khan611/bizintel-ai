"""FastAPI application entry point."""

from fastapi import FastAPI

from bizintel.api.analytics_schemas import AnalyticsSummaryResponse
from bizintel.api.analytics_service import get_analytics_summary
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

    @app.get(
        "/analytics/summary",
        response_model=AnalyticsSummaryResponse,
    )
    def analytics_summary() -> AnalyticsSummaryResponse:
        """Return the combined business analytics summary."""
        summary = get_analytics_summary(
            settings.processed_data_dir
        )

        return AnalyticsSummaryResponse(
            **summary
        )

    return app


app = create_app()