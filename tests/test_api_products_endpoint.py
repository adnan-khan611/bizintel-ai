"""Tests for the products analytics API endpoint."""

from fastapi.testclient import TestClient

from bizintel.main import app


def test_products_endpoint_returns_expected_contract(
    monkeypatch,
) -> None:
    """Products endpoint should return the expected response."""
    import bizintel.main as main

    monkeypatch.setattr(
        main,
        "get_products_analytics",
        lambda processed_data_dir: {
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
        },
    )

    client = TestClient(app)

    response = client.get("/analytics/products")

    assert response.status_code == 200

    body = response.json()

    assert set(body) == {
        "total_products",
        "products_by_category",
        "product_revenue",
        "product_order_items",
    }

    assert body["total_products"] == 100
    assert body["products_by_category"] == {
        "electronics": 40,
        "furniture": 60,
    }
    assert body["product_revenue"] == {
        "P001": 1500,
        "P002": 900,
    }
    assert body["product_order_items"] == {
        "P001": 10,
        "P002": 5,
    }


def test_products_endpoint_exposes_openapi_schema() -> None:
    """Products endpoint should expose its response model in OpenAPI."""
    client = TestClient(app)

    response = client.get("/openapi.json")

    assert response.status_code == 200

    openapi = response.json()

    products_operation = openapi["paths"]["/analytics/products"]["get"]

    assert products_operation["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["$ref"] == (
        "#/components/schemas/ProductsResponse"
    )

    assert "ProductsResponse" in openapi["components"]["schemas"]