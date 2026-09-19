"""Tests for API application exceptions."""

from bizintel.api.exceptions import APIError


def test_api_error_stores_detail() -> None:
    """APIError should store the provided detail."""
    error = APIError("Dataset not found")

    assert error.detail == "Dataset not found"


def test_api_error_is_exception() -> None:
    """APIError should inherit from Exception."""
    error = APIError("Invalid dataset")

    assert isinstance(error, Exception)