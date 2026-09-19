"""Tests for API exception handlers."""

from fastapi import Request

from bizintel.api.exceptions import APIError
from bizintel.api.handlers import api_error_handler


def test_api_error_handler_returns_bad_request() -> None:
    """API error handler should return HTTP 400."""
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/test",
            "headers": [],
            "query_string": b"",
            "server": ("testserver", 80),
            "scheme": "http",
            "client": ("testclient", 50000),
        }
    )

    response = api_error_handler(
        request,
        APIError("Invalid request"),
    )

    assert response.status_code == 400