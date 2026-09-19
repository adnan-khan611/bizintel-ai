"""Tests for customers analytics service."""

from pathlib import Path

from bizintel.api.customers_service import (
    get_customers_analytics,
)


def test_get_customers_analytics_returns_response(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Customers service should return the expected response."""
    from bizintel.api import customers_service

    expected = {
        "unique_customers": 100,
        "orders_per_customer": 1.25,
        "customer_order_counts": {
            "C001": 2,
            "C002": 1,
        },
        "customer_order_distribution": {
            "1": 80,
            "2": 20,
        },
    }

    class FakeSeries:
        def items(self):
            return [
                ("C001", 2),
                ("C002", 1),
            ]

    class FakeDistribution:
        def items(self):
            return [
                (1, 80),
                (2, 20),
            ]

    monkeypatch.setattr(
        customers_service,
        "load_analytics_datasets",
        lambda processed_data_dir: {
            "customers": object(),
            "orders": object(),
            "products": object(),
            "order_items": object(),
            "order_payments": object(),
        },
    )

    monkeypatch.setattr(
        customers_service,
        "calculate_unique_customers",
        lambda customers: 100,
    )

    monkeypatch.setattr(
        customers_service,
        "calculate_orders_per_customer",
        lambda orders, customers: 1.25,
    )

    monkeypatch.setattr(
        customers_service,
        "calculate_customer_order_counts",
        lambda orders: FakeSeries(),
    )

    monkeypatch.setattr(
        customers_service,
        "calculate_customer_order_distribution",
        lambda orders: FakeDistribution(),
    )

    response = get_customers_analytics(tmp_path)

    assert response.model_dump() == expected