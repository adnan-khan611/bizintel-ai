import pandas as pd
import pytest

from bizintel.analytics.growth import (
    calculate_monthly_orders,
    calculate_monthly_revenue,
    calculate_monthly_unique_customers,
    calculate_order_growth,
    calculate_revenue_growth,
)


def test_calculate_monthly_revenue() -> None:
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "order_date": pd.to_datetime(
                ["2024-01-10", "2024-01-20", "2024-03-05"]
            ),
        }
    )

    order_items = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "price_minor": [1000, 2000, 3000],
        }
    )

    result = calculate_monthly_revenue(orders, order_items)

    expected = pd.Series(
        [3000, 0, 3000],
        index=pd.PeriodIndex(
            ["2024-01", "2024-02", "2024-03"],
            freq="M",
            name="month",
        ),
        name="price_minor",
    )

    pd.testing.assert_series_equal(result, expected)


def test_calculate_monthly_orders() -> None:
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "order_date": pd.to_datetime(
                ["2024-01-10", "2024-01-20", "2024-03-05"]
            ),
        }
    )

    result = calculate_monthly_orders(orders)

    expected = pd.Series(
        [2, 0, 1],
        index=pd.PeriodIndex(
            ["2024-01", "2024-02", "2024-03"],
            freq="M",
            name="month",
        ),
        name="order_id",
    )

    pd.testing.assert_series_equal(result, expected)


def test_calculate_monthly_unique_customers() -> None:
    orders = pd.DataFrame(
        {
            "customer_id": ["c1", "c1", "c2"],
            "order_date": pd.to_datetime(
                ["2024-01-10", "2024-01-20", "2024-03-05"]
            ),
        }
    )

    result = calculate_monthly_unique_customers(orders)

    expected = pd.Series(
        [1, 0, 1],
        index=pd.PeriodIndex(
            ["2024-01", "2024-02", "2024-03"],
            freq="M",
            name="month",
        ),
        name="customer_id",
    )

    pd.testing.assert_series_equal(result, expected)


def test_monthly_revenue_preserves_complete_calendar_months() -> None:
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2"],
            "order_date": pd.to_datetime(
                ["2024-01-10", "2024-04-05"]
            ),
        }
    )

    order_items = pd.DataFrame(
        {
            "order_id": ["o1", "o2"],
            "price_minor": [1000, 4000],
        }
    )

    result = calculate_monthly_revenue(orders, order_items)

    expected_index = pd.period_range(
        "2024-01",
        "2024-04",
        freq="M",
        name="month",
    )

    assert result.index.equals(expected_index)
    assert result.tolist() == [1000, 0, 0, 4000]


def test_monthly_orders_preserves_complete_calendar_months() -> None:
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2"],
            "order_date": pd.to_datetime(
                ["2024-01-10", "2024-04-05"]
            ),
        }
    )

    result = calculate_monthly_orders(orders)

    expected_index = pd.period_range(
        "2024-01",
        "2024-04",
        freq="M",
        name="month",
    )

    assert result.index.equals(expected_index)
    assert result.tolist() == [1, 0, 0, 1]


def test_calculate_revenue_growth() -> None:
    monthly_revenue = pd.Series(
        [1000, 1200, 900],
        index=pd.PeriodIndex(
            ["2024-01", "2024-02", "2024-03"],
            freq="M",
        ),
    )

    result = calculate_revenue_growth(monthly_revenue)

    expected = pd.Series(
        [None, 20.0, -25.0],
        index=monthly_revenue.index,
        dtype="float64",
    )

    pd.testing.assert_series_equal(result, expected)


def test_calculate_order_growth() -> None:
    monthly_orders = pd.Series(
        [100, 120, 90],
        index=pd.PeriodIndex(
            ["2024-01", "2024-02", "2024-03"],
            freq="M",
        ),
    )

    result = calculate_order_growth(monthly_orders)

    expected = pd.Series(
        [None, 20.0, -25.0],
        index=monthly_orders.index,
        dtype="float64",
    )

    pd.testing.assert_series_equal(result, expected)


def test_revenue_growth_handles_zero_previous_month() -> None:
    monthly_revenue = pd.Series(
        [0, 100],
        index=pd.PeriodIndex(
            ["2024-01", "2024-02"],
            freq="M",
        ),
    )

    result = calculate_revenue_growth(monthly_revenue)

    assert pd.isna(result.iloc[0])
    assert pd.isna(result.iloc[1])


def test_order_growth_handles_zero_previous_month() -> None:
    monthly_orders = pd.Series(
        [0, 100],
        index=pd.PeriodIndex(
            ["2024-01", "2024-02"],
            freq="M",
        ),
    )

    result = calculate_order_growth(monthly_orders)

    assert pd.isna(result.iloc[0])
    assert pd.isna(result.iloc[1])


def test_monthly_revenue_requires_order_columns() -> None:
    orders = pd.DataFrame({"order_id": ["o1"]})

    order_items = pd.DataFrame(
        {
            "order_id": ["o1"],
            "price_minor": [1000],
        }
    )

    with pytest.raises(ValueError, match="order_date"):
        calculate_monthly_revenue(orders, order_items)


def test_monthly_orders_requires_order_columns() -> None:
    orders = pd.DataFrame({"order_id": ["o1"]})

    with pytest.raises(ValueError, match="order_date"):
        calculate_monthly_orders(orders)


def test_monthly_customers_requires_customer_columns() -> None:
    orders = pd.DataFrame(
        {
            "order_id": ["o1"],
            "order_date": pd.to_datetime(["2024-01-10"]),
        }
    )

    with pytest.raises(ValueError, match="customer_id"):
        calculate_monthly_unique_customers(orders)