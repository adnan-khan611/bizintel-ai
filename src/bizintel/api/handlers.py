"""API exception handlers for BizIntel AI."""

from fastapi import Request
from fastapi.responses import JSONResponse

from bizintel.api.exceptions import APIError


def api_error_handler(
    request: Request,
    exc: APIError,
) -> JSONResponse:
    """Convert an APIError into a standard JSON response."""
    return JSONResponse(
        status_code=400,
        content={
            "detail": exc.detail,
        },
    )