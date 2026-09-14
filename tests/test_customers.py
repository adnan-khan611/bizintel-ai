"""Tests for customer analytics."""

import pandas as pd
import pytest

from bizintel.analytics.customers import (
    calculate_customer_order_counts,
    calculate_customer_order_distribution,
    calculate_orders_per_customer,
    calculate_top_customers_by_orders,
    calculate_unique_customers,
)


def test_calculate_unique_customers() -> None:
    """Test distinct customer calculation."""
    customers = pd.DataFrame(
        {
            "customer_id": ["c1", "c2", "c3"],
        }
    )

    assert calculate_unique_customers(customers) == 3


def test_calculate_unique_customers_counts_distinct_ids() -> None:
    """Test that duplicate customer IDs are counted once."""
    customers = pd.DataFrame(
        {
            "customer_id": ["c1", "c1", "c2"],
        }
    )

    assert calculate_unique_customers(customers) == 2


def test_calculate_orders_per_customer() -> None:
    """Test average orders per customer."""
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3", "o4"],
            "customer_id": ["c1", "c1", "c2", "c3"],
        }
    )
    customers = pd.DataFrame(
        {
            "customer_id": ["c1", "c2", "c3"],
        }
    )

    result = calculate_orders_per_customer(orders, customers)

    assert result == pytest.approx(4 / 3)


def test_calculate_orders_per_customer_with_no_customers() -> None:
    """Test zero division handling when there are no customers."""
    orders = pd.DataFrame(
        {
            "order_id": ["o1"],
            "customer_id": ["c1"],
        }
    )
    customers = pd.DataFrame(
        {
            "customer_id": [],
        }
    )

    assert calculate_orders_per_customer(orders, customers) == 0.0


def test_calculate_customer_order_counts() -> None:
    """Test order count per customer."""
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3", "o4"],
            "customer_id": ["c1", "c1", "c2", "c3"],
        }
    )

    result = calculate_customer_order_counts(orders)

    assert result["c1"] == 2
    assert result["c2"] == 1
    assert result["c3"] == 1


def test_customer_order_counts_use_distinct_orders() -> None:
    """Test that duplicate order IDs are counted once per customer."""
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o1", "o2"],
            "customer_id": ["c1", "c1", "c1"],
        }
    )

    result = calculate_customer_order_counts(orders)

    assert result["c1"] == 2


def test_calculate_customer_order_distribution() -> None:
    """Test customer order frequency distribution."""
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3", "o4", "o5"],
            "customer_id": ["c1", "c1", "c2", "c3", "c3"],
        }
    )

    result = calculate_customer_order_distribution(orders)

    assert result[1] == 1
    assert result[2] == 2


def test_calculate_top_customers_by_orders() -> None:
    """Test top customers by distinct order count."""
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3", "o4"],
            "customer_id": ["c1", "c1", "c2", "c3"],
        }
    )

    result = calculate_top_customers_by_orders(orders, limit=2)

    assert len(result) == 2
    assert result.index[0] == "c1"
    assert result.iloc[0] == 2


def test_top_customers_rejects_invalid_limit() -> None:
    """Test validation of the top-customer limit."""
    orders = pd.DataFrame(
        {
            "order_id": ["o1"],
            "customer_id": ["c1"],
        }
    )

    with pytest.raises(ValueError, match="limit"):
        calculate_top_customers_by_orders(orders, limit=0)


def test_missing_customer_id_raises_error() -> None:
    """Test validation for missing customer_id."""
    customers = pd.DataFrame(
        {
            "name": ["Alice"],
        }
    )

    with pytest.raises(ValueError, match="customer_id"):
        calculate_unique_customers(customers)