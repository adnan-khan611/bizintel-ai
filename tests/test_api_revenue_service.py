"""Tests for the revenue API service."""

import pandas as pd

from bizintel.api.revenue_schemas import RevenueResponse
from bizintel.api.revenue_service import get_revenue_analytics


def test_get_revenue_analytics_builds_response(
    tmp_path,
    monkeypatch,
) -> None:
    """Revenue service should build the expected response."""
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

    def fake_merchandise_revenue(order_items):
        assert order_items is datasets["order_items"]
        return 1000

    def fake_freight_value(order_items):
        assert order_items is datasets["order_items"]
        return 200

    def fake_payment_value(order_payments):
        assert order_payments is datasets["order_payments"]
        return 1200

    monkeypatch.setattr(
        "bizintel.api.revenue_service.load_analytics_datasets",
        fake_load_analytics_datasets,
    )
    monkeypatch.setattr(
        "bizintel.api.revenue_service.calculate_merchandise_revenue",
        fake_merchandise_revenue,
    )
    monkeypatch.setattr(
        "bizintel.api.revenue_service.calculate_freight_value",
        fake_freight_value,
    )
    monkeypatch.setattr(
        "bizintel.api.revenue_service.calculate_payment_value",
        fake_payment_value,
    )

    result = get_revenue_analytics(tmp_path)

    assert isinstance(result, RevenueResponse)
    assert result.model_dump() == {
        "merchandise_revenue_minor": 1000,
        "freight_value_minor": 200,
        "payment_value_minor": 1200,
    }