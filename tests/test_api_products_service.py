"""Tests for products analytics service."""

from pathlib import Path

from bizintel.api.products_service import (
    get_products_analytics,
)


def test_get_products_analytics_returns_response(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Products service should return the expected response."""
    import bizintel.api.products_service as products_service

    expected = {
        "total_products": 100,
        "products_by_category": {
            "electronics": 40,
            "furniture": 60,
        },
        "product_revenue": {
            "P001": 1500,
            "P002": 900,
        },
        "product_order_items": {
            "P001": 10,
            "P002": 5,
        },
    }

    class FakeSeries:
        def __init__(self, values):
            self._values = values

        def items(self):
            return self._values

    monkeypatch.setattr(
        products_service,
        "load_analytics_datasets",
        lambda processed_data_dir: {
            "customers": object(),
            "products": object(),
            "orders": object(),
            "order_items": object(),
            "order_payments": object(),
        },
    )

    monkeypatch.setattr(
        products_service,
        "calculate_total_products",
        lambda products: 100,
    )

    monkeypatch.setattr(
        products_service,
        "calculate_products_by_category",
        lambda products: FakeSeries(
            [
                ("electronics", 40),
                ("furniture", 60),
            ]
        ),
    )

    monkeypatch.setattr(
        products_service,
        "calculate_product_revenue",
        lambda order_items: FakeSeries(
            [
                ("P001", 1500),
                ("P002", 900),
            ]
        ),
    )

    monkeypatch.setattr(
        products_service,
        "calculate_product_order_item_counts",
        lambda order_items: FakeSeries(
            [
                ("P001", 10),
                ("P002", 5),
            ]
        ),
    )

    response = get_products_analytics(tmp_path)

    assert response.model_dump() == expected