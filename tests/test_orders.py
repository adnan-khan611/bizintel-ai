"""Tests for order analytics."""

import pandas as pd
import pytest

from bizintel.analytics.orders import (
    calculate_canceled_orders,
    calculate_delivered_orders,
    calculate_orders_by_status,
    calculate_total_orders,
    calculate_unavailable_orders,
)


def test_calculate_total_orders() -> None:
    """Test total distinct order calculation."""
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "order_status": ["delivered", "shipped", "canceled"],
        }
    )

    assert calculate_total_orders(orders) == 3


def test_calculate_total_orders_counts_distinct_ids() -> None:
    """Test that duplicate order IDs are counted once."""
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o1", "o2"],
            "order_status": ["delivered", "delivered", "shipped"],
        }
    )

    assert calculate_total_orders(orders) == 2


def test_calculate_orders_by_status() -> None:
    """Test order counts grouped by status."""
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3", "o4"],
            "order_status": [
                "delivered",
                "delivered",
                "canceled",
                "shipped",
            ],
        }
    )

    result = calculate_orders_by_status(orders)

    assert result["delivered"] == 2
    assert result["canceled"] == 1
    assert result["shipped"] == 1


def test_calculate_delivered_orders() -> None:
    """Test delivered order count."""
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "order_status": ["delivered", "shipped", "delivered"],
        }
    )

    assert calculate_delivered_orders(orders) == 2


def test_calculate_canceled_orders() -> None:
    """Test canceled order count."""
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "order_status": ["delivered", "canceled", "canceled"],
        }
    )

    assert calculate_canceled_orders(orders) == 2


def test_calculate_unavailable_orders() -> None:
    """Test unavailable order count."""
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "order_status": ["delivered", "unavailable", "shipped"],
        }
    )

    assert calculate_unavailable_orders(orders) == 1


def test_missing_order_id_raises_error() -> None:
    """Test validation for missing order_id."""
    orders = pd.DataFrame(
        {
            "order_status": ["delivered"],
        }
    )

    with pytest.raises(ValueError, match="order_id"):
        calculate_total_orders(orders)


def test_missing_order_status_raises_error() -> None:
    """Test validation for missing order_status."""
    orders = pd.DataFrame(
        {
            "order_id": ["o1"],
        }
    )

    with pytest.raises(ValueError, match="order_status"):
        calculate_orders_by_status(orders)