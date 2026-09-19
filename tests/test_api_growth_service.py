"""Tests for growth analytics service."""

from pathlib import Path

from bizintel.api.growth_service import (
    get_growth_analytics,
)


def test_get_growth_analytics_returns_response(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Growth service should return the expected response."""
    import bizintel.api.growth_service as growth_service

    expected = {
        "monthly_revenue": {
            "2017-01": 1000,
            "2017-02": 1200,
        },
        "monthly_orders": {
            "2017-01": 100,
            "2017-02": 120,
        },
        "monthly_unique_customers": {
            "2017-01": 90,
            "2017-02": 105,
        },
        "revenue_growth": {
            "2017-02": 0.20,
        },
        "order_growth": {
            "2017-02": 0.20,
        },
    }

    class FakeSeries:
        def __init__(self, values):
            self._values = values

        def items(self):
            return self._values

    monkeypatch.setattr(
        growth_service,
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
        growth_service,
        "calculate_monthly_revenue",
        lambda orders, order_items: FakeSeries(
            [
                ("2017-01", 1000),
                ("2017-02", 1200),
            ]
        ),
    )

    monkeypatch.setattr(
        growth_service,
        "calculate_monthly_orders",
        lambda orders: FakeSeries(
            [
                ("2017-01", 100),
                ("2017-02", 120),
            ]
        ),
    )

    monkeypatch.setattr(
        growth_service,
        "calculate_monthly_unique_customers",
        lambda orders: FakeSeries(
            [
                ("2017-01", 90),
                ("2017-02", 105),
            ]
        ),
    )

    monkeypatch.setattr(
        growth_service,
        "calculate_revenue_growth",
        lambda monthly_revenue: FakeSeries(
            [
                ("2017-02", 0.20),
            ]
        ),
    )

    monkeypatch.setattr(
        growth_service,
        "calculate_order_growth",
        lambda monthly_orders: FakeSeries(
            [
                ("2017-02", 0.20),
            ]
        ),
    )

    response = get_growth_analytics(tmp_path)

    assert response.model_dump() == expected