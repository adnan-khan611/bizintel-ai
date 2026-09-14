"""Tests for forecasting dataset builders."""

import pandas as pd
import pytest

from bizintel.ml.dataset import build_monthly_revenue_dataset


def test_build_monthly_revenue_dataset():
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "order_date": pd.to_datetime(
                [
                    "2024-01-05",
                    "2024-01-15",
                    "2024-02-10",
                ]
            ),
        }
    )

    order_items = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "price_minor": [1000, 2500, 3000],
        }
    )

    result = build_monthly_revenue_dataset(
        orders,
        order_items,
        include_partial_months=True,
    )

    expected = pd.DataFrame(
        {
            "month": pd.PeriodIndex(
                ["2024-01", "2024-02"],
                freq="M",
            ),
            "revenue": [3500, 3000],
        }
    )

    pd.testing.assert_frame_equal(result, expected)


def test_multiple_order_items_are_summed():
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2"],
            "order_date": pd.to_datetime(
                ["2024-01-10", "2024-01-20"]
            ),
        }
    )

    order_items = pd.DataFrame(
        {
            "order_id": ["o1", "o1", "o2"],
            "price_minor": [1000, 2000, 5000],
        }
    )

    result = build_monthly_revenue_dataset(
        orders,
        order_items,
        include_partial_months=True,
    )

    assert result.loc[0, "revenue"] == 8000


def test_missing_month_is_filled_with_zero():
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2"],
            "order_date": pd.to_datetime(
                ["2024-01-10", "2024-03-10"]
            ),
        }
    )

    order_items = pd.DataFrame(
        {
            "order_id": ["o1", "o2"],
            "price_minor": [1000, 3000],
        }
    )

    result = build_monthly_revenue_dataset(
        orders,
        order_items,
        include_partial_months=True,
    )

    expected_revenue = [1000, 0, 3000]

    assert result["revenue"].tolist() == expected_revenue
    assert result["month"].tolist() == [
        pd.Period("2024-01", freq="M"),
        pd.Period("2024-02", freq="M"),
        pd.Period("2024-03", freq="M"),
    ]


def test_partial_boundary_months_are_excluded_by_default():
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "order_date": pd.to_datetime(
                [
                    "2024-01-05",
                    "2024-02-15",
                    "2024-03-20",
                ]
            ),
        }
    )

    order_items = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "price_minor": [1000, 2000, 3000],
        }
    )

    result = build_monthly_revenue_dataset(
        orders,
        order_items,
    )

    expected = pd.DataFrame(
        {
            "month": pd.PeriodIndex(["2024-02"], freq="M"),
            "revenue": [2000],
        }
    )

    pd.testing.assert_frame_equal(result, expected)


def test_partial_months_can_be_included():
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "order_date": pd.to_datetime(
                [
                    "2024-01-05",
                    "2024-02-15",
                    "2024-03-20",
                ]
            ),
        }
    )

    order_items = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "price_minor": [1000, 2000, 3000],
        }
    )

    result = build_monthly_revenue_dataset(
        orders,
        order_items,
        include_partial_months=True,
    )

    assert result["revenue"].tolist() == [1000, 2000, 3000]


def test_missing_order_column_raises_error():
    orders = pd.DataFrame(
        {
            "order_id": ["o1"],
        }
    )

    order_items = pd.DataFrame(
        {
            "order_id": ["o1"],
            "price_minor": [1000],
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required columns: order_date",
    ):
        build_monthly_revenue_dataset(orders, order_items)


def test_missing_order_item_column_raises_error():
    orders = pd.DataFrame(
        {
            "order_id": ["o1"],
            "order_date": pd.to_datetime(["2024-01-10"]),
        }
    )

    order_items = pd.DataFrame(
        {
            "order_id": ["o1"],
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required columns: price_minor",
    ):
        build_monthly_revenue_dataset(orders, order_items)


def test_non_datetime_order_date_raises_error():
    orders = pd.DataFrame(
        {
            "order_id": ["o1"],
            "order_date": ["2024-01-10"],
        }
    )

    order_items = pd.DataFrame(
        {
            "order_id": ["o1"],
            "price_minor": [1000],
        }
    )

    with pytest.raises(
        TypeError,
        match="order_date must be a datetime column",
    ):
        build_monthly_revenue_dataset(orders, order_items)


def test_empty_input_returns_empty_dataset():
    orders = pd.DataFrame(
        {
            "order_id": pd.Series(dtype="string"),
            "order_date": pd.Series(dtype="datetime64[ns]"),
        }
    )

    order_items = pd.DataFrame(
        {
            "order_id": pd.Series(dtype="string"),
            "price_minor": pd.Series(dtype="int64"),
        }
    )

    result = build_monthly_revenue_dataset(
        orders,
        order_items,
    )

    assert result.empty
    assert result.columns.tolist() == ["month", "revenue"]