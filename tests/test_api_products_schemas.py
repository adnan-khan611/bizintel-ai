"""Tests for products API response schemas."""

from bizintel.api.products_schemas import ProductsResponse


def test_products_response_accepts_valid_values() -> None:
    """ProductsResponse should accept valid product analytics."""
    response = ProductsResponse(
        total_products=100,
        products_by_category={
            "electronics": 40,
            "furniture": 60,
        },
        product_revenue={
            "P001": 1500,
            "P002": 900,
        },
        product_order_items={
            "P001": 10,
            "P002": 5,
        },
    )

    assert response.total_products == 100
    assert response.products_by_category == {
        "electronics": 40,
        "furniture": 60,
    }
    assert response.product_revenue == {
        "P001": 1500,
        "P002": 900,
    }
    assert response.product_order_items == {
        "P001": 10,
        "P002": 5,
    }


def test_products_response_serializes_to_dict() -> None:
    """ProductsResponse should serialize to a dictionary."""
    response = ProductsResponse(
        total_products=100,
        products_by_category={
            "electronics": 40,
            "furniture": 60,
        },
        product_revenue={
            "P001": 1500,
            "P002": 900,
        },
        product_order_items={
            "P001": 10,
            "P002": 5,
        },
    )

    assert response.model_dump() == {
        "total_products": 100,
        "products_by_category": {
            "electronics": 40,
            "furniture": 60,
        },
        "product_revenue": {
            "P001": 1500,
            "P002": 900,
        },
        "product_order_items": {
            "P001": 10,
            "P002": 5,
        },
    }