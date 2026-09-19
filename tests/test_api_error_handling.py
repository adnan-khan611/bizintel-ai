"""Tests for centralized API error handling."""

from fastapi import Request
from fastapi.testclient import TestClient

from bizintel.api.exceptions import APIError
from bizintel.main import app


def test_api_error_handler_is_registered() -> None:
    """APIError should be registered with the FastAPI application."""
    assert APIError in app.exception_handlers


def test_api_error_returns_standard_response() -> None:
    """APIError should produce the standard error response."""
    async def raise_api_error(request: Request) -> None:
        raise APIError("Test API error")

    app.add_api_route(
        "/test-api-error",
        raise_api_error,
        methods=["GET"],
    )

    client = TestClient(app)

    response = client.get("/test-api-error")

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Test API error",
    }