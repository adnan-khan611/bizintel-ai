"""Tests for product analytics."""

import pandas as pd
import pytest

from bizintel.analytics.products import (
    calculate_product_order_item_counts,
    calculate_product_revenue,
    calculate_products_by_category,
    calculate_top_products_by_order_items,
    calculate_top_products_by_revenue,
    calculate_total_products,
)


def test_calculate_total_products() -> None:
    """Test distinct product calculation."""
    products = pd.DataFrame(
        {
            "product_id": ["p1", "p2", "p3"],
        }
    )

    assert calculate_total_products(products) == 3


def test_calculate_total_products_counts_distinct_ids() -> None:
    """Test that duplicate product IDs are counted once."""
    products = pd.DataFrame(
        {
            "product_id": ["p1", "p1", "p2"],
        }
    )

    assert calculate_total_products(products) == 2


def test_calculate_products_by_category() -> None:
    """Test product counts by category."""
    products = pd.DataFrame(
        {
            "product_id": ["p1", "p2", "p3", "p4"],
            "product_category_name": [
                "electronics",
                "electronics",
                "furniture",
                "books",
            ],
        }
    )

    result = calculate_products_by_category(products)

    assert result["electronics"] == 2
    assert result["furniture"] == 1
    assert result["books"] == 1


def test_calculate_products_by_category_handles_missing_category() -> None:
    """Test that missing categories are grouped as unknown."""
    products = pd.DataFrame(
        {
            "product_id": ["p1", "p2", "p3"],
            "product_category_name": [
                "electronics",
                None,
                None,
            ],
        }
    )

    result = calculate_products_by_category(products)

    assert result["electronics"] == 1
    assert result["unknown"] == 2


def test_calculate_product_revenue() -> None:
    """Test product merchandise revenue."""
    order_items = pd.DataFrame(
        {
            "product_id": ["p1", "p1", "p2"],
            "price_minor": [1000, 2000, 5000],
        }
    )

    result = calculate_product_revenue(order_items)

    assert result["p1"] == 3000
    assert result["p2"] == 5000


def test_calculate_product_order_item_counts() -> None:
    """Test order-item count by product."""
    order_items = pd.DataFrame(
        {
            "product_id": ["p1", "p1", "p2"],
            "order_id": ["o1", "o2", "o3"],
            "order_item_id": [1, 1, 1],
        }
    )

    result = calculate_product_order_item_counts(order_items)

    assert result["p1"] == 2
    assert result["p2"] == 1


def test_calculate_top_products_by_revenue() -> None:
    """Test top products by merchandise revenue."""
    order_items = pd.DataFrame(
        {
            "product_id": ["p1", "p2", "p3"],
            "price_minor": [1000, 5000, 3000],
        }
    )

    result = calculate_top_products_by_revenue(
        order_items,
        limit=2,
    )

    assert len(result) == 2
    assert result.index[0] == "p2"
    assert result.iloc[0] == 5000


def test_calculate_top_products_by_order_items() -> None:
    """Test top products by order-item count."""
    order_items = pd.DataFrame(
        {
            "product_id": ["p1", "p1", "p1", "p2"],
            "order_id": ["o1", "o2", "o3", "o4"],
            "order_item_id": [1, 1, 1, 1],
        }
    )

    result = calculate_top_products_by_order_items(
        order_items,
        limit=1,
    )

    assert len(result) == 1
    assert result.index[0] == "p1"
    assert result.iloc[0] == 3


def test_top_products_rejects_invalid_revenue_limit() -> None:
    """Test validation of revenue ranking limit."""
    order_items = pd.DataFrame(
        {
            "product_id": ["p1"],
            "price_minor": [1000],
        }
    )

    with pytest.raises(ValueError, match="limit"):
        calculate_top_products_by_revenue(
            order_items,
            limit=0,
        )


def test_top_products_rejects_invalid_order_item_limit() -> None:
    """Test validation of order-item ranking limit."""
    order_items = pd.DataFrame(
        {
            "product_id": ["p1"],
            "order_id": ["o1"],
            "order_item_id": [1],
        }
    )

    with pytest.raises(ValueError, match="limit"):
        calculate_top_products_by_order_items(
            order_items,
            limit=0,
        )


def test_missing_product_id_raises_error() -> None:
    """Test validation for missing product_id."""
    products = pd.DataFrame(
        {
            "product_category_name": ["electronics"],
        }
    )

    with pytest.raises(ValueError, match="product_id"):
        calculate_total_products(products)