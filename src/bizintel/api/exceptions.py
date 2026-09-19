"""Application exceptions for BizIntel AI API."""


class APIError(Exception):
    """Base exception for expected API errors."""

    def __init__(self, detail: str) -> None:
        super().__init__(detail)
        self.detail = detail