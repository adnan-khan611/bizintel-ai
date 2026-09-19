"""Tests for the orders API service."""

import pandas as pd

from bizintel.api.orders_schemas import OrdersResponse
from bizintel.api.orders_service import get_orders_analytics


def test_get_orders_analytics_builds_response(
    tmp_path,
    monkeypatch,
) -> None:
    """Orders service should build the expected response."""
    datasets = {
        "customers": pd.DataFrame(),
        "products": pd.DataFrame(),
        "orders": pd.DataFrame(),
        "order_items": pd.DataFrame(),
        "order_payments": pd.DataFrame(),
    }

    def fake_load_analytics_datasets(processed_data_dir):
        assert processed_data_dir == tmp_path
        return datasets

    def fake_total_orders(orders):
        assert orders is datasets["orders"]
        return 100

    def fake_delivered_orders(orders):
        assert orders is datasets["orders"]
        return 90

    def fake_canceled_orders(orders):
        assert orders is datasets["orders"]
        return 5

    def fake_unavailable_orders(orders):
        assert orders is datasets["orders"]
        return 5

    def fake_orders_by_status(orders):
        assert orders is datasets["orders"]
        return pd.Series(
            {
                "delivered": 90,
                "canceled": 5,
                "unavailable": 5,
            }
        )

    monkeypatch.setattr(
        "bizintel.api.orders_service.load_analytics_datasets",
        fake_load_analytics_datasets,
    )
    monkeypatch.setattr(
        "bizintel.api.orders_service.calculate_total_orders",
        fake_total_orders,
    )
    monkeypatch.setattr(
        "bizintel.api.orders_service.calculate_delivered_orders",
        fake_delivered_orders,
    )
    monkeypatch.setattr(
        "bizintel.api.orders_service.calculate_canceled_orders",
        fake_canceled_orders,
    )
    monkeypatch.setattr(
        "bizintel.api.orders_service.calculate_unavailable_orders",
        fake_unavailable_orders,
    )
    monkeypatch.setattr(
        "bizintel.api.orders_service.calculate_orders_by_status",
        fake_orders_by_status,
    )

    result = get_orders_analytics(tmp_path)

    assert isinstance(result, OrdersResponse)

    assert result.model_dump() == {
        "total_orders": 100,
        "delivered_orders": 90,
        "canceled_orders": 5,
        "unavailable_orders": 5,
        "orders_by_status": {
            "delivered": 90,
            "canceled": 5,
            "unavailable": 5,
        },
    }