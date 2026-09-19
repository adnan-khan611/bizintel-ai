"""Tests for the customers analytics API endpoint."""

from fastapi.testclient import TestClient

from bizintel.main import app


def test_customers_endpoint_returns_expected_contract(
    monkeypatch,
) -> None:
    """Customers endpoint should return the expected response."""
    import bizintel.main as main

    monkeypatch.setattr(
        main,
        "get_customers_analytics",
        lambda processed_data_dir: {
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
        },
    )

    client = TestClient(app)

    response = client.get("/analytics/customers")

    assert response.status_code == 200

    body = response.json()

    assert set(body) == {
        "unique_customers",
        "orders_per_customer",
        "customer_order_counts",
        "customer_order_distribution",
    }

    assert body["unique_customers"] == 100
    assert body["orders_per_customer"] == 1.25
    assert body["customer_order_counts"] == {
        "C001": 2,
        "C002": 1,
    }
    assert body["customer_order_distribution"] == {
        "1": 80,
        "2": 20,
    }


def test_customers_endpoint_exposes_openapi_schema() -> None:
    """Customers endpoint should expose its response model in OpenAPI."""
    client = TestClient(app)

    response = client.get("/openapi.json")

    assert response.status_code == 200

    openapi = response.json()

    customers_operation = openapi["paths"]["/analytics/customers"]["get"]

    assert customers_operation["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["$ref"] == (
        "#/components/schemas/CustomersResponse"
    )

    assert "CustomersResponse" in openapi["components"]["schemas"]