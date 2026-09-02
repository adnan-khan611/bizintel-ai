"""FastAPI application entry point."""

from fastapi import FastAPI

from bizintel.config import settings


def create_app() -> FastAPI:
    """Create and configure the BizIntel AI API application."""
    app = FastAPI(title=settings.app_name)

    @app.get("/health")
    def health_check() -> dict[str, str]:
        """Return the service health status."""
        return {"status": "ok"}

    return app


app = create_app()
