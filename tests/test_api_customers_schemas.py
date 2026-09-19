"""Tests for customers API response schemas."""

from bizintel.api.customers_schemas import CustomersResponse


def test_customers_response_accepts_valid_values() -> None:
    """CustomersResponse should accept valid customer analytics."""
    response = CustomersResponse(
        unique_customers=100,
        orders_per_customer=1.25,
        customer_order_counts={
            "C001": 2,
            "C002": 1,
        },
        customer_order_distribution={
            "1": 80,
            "2": 20,
        },
    )

    assert response.unique_customers == 100
    assert response.orders_per_customer == 1.25
    assert response.customer_order_counts == {
        "C001": 2,
        "C002": 1,
    }
    assert response.customer_order_distribution == {
        "1": 80,
        "2": 20,
    }


def test_customers_response_serializes_to_dict() -> None:
    """CustomersResponse should serialize to a dictionary."""
    response = CustomersResponse(
        unique_customers=100,
        orders_per_customer=1.25,
        customer_order_counts={
            "C001": 2,
            "C002": 1,
        },
        customer_order_distribution={
            "1": 80,
            "2": 20,
        },
    )

    result = response.model_dump()

    assert result == {
        "unique_customers": 100,
        "orders_per_customer": 1.25,
        "customer_order_counts": {
            "C001": 2,
            "C002": 1,
        },
        "customer_order_distribution": {
            "1": 80,
            "2": 20,
        },
    }