"""Tests for the analytics service layer."""

import pandas as pd

from bizintel.api.analytics_service import get_analytics_summary


def test_get_analytics_summary_loads_datasets_and_builds_summary(
    tmp_path,
    monkeypatch,
):
    datasets = {
        "customers": pd.DataFrame(
            {
                "customer_id": ["C001"],
            }
        ),
        "products": pd.DataFrame(
            {
                "product_id": ["P001"],
            }
        ),
        "orders": pd.DataFrame(
            {
                "order_id": ["O001"],
            }
        ),
        "order_items": pd.DataFrame(
            {
                "order_id": ["O001"],
                "price_minor": [1000],
            }
        ),
        "order_payments": pd.DataFrame(
            {
                "order_id": ["O001"],
                "payment_value_minor": [1000],
            }
        ),
    }

    expected_summary = {
        "revenue": {
            "merchandise_revenue_minor": 1000,
        },
    }

    def fake_load_analytics_datasets(processed_data_dir):
        assert processed_data_dir == tmp_path
        return datasets

    def fake_build_analytics_summary(
        customers,
        orders,
        products,
        order_items,
        order_payments,
    ):
        assert customers is datasets["customers"]
        assert orders is datasets["orders"]
        assert products is datasets["products"]
        assert order_items is datasets["order_items"]
        assert order_payments is datasets["order_payments"]

        return expected_summary

    monkeypatch.setattr(
        "bizintel.api.analytics_service.load_analytics_datasets",
        fake_load_analytics_datasets,
    )
    monkeypatch.setattr(
        "bizintel.api.analytics_service.build_analytics_summary",
        fake_build_analytics_summary,
    )

    result = get_analytics_summary(tmp_path)

    assert result == expected_summary