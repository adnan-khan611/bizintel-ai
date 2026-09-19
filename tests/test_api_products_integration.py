"""Integration tests for the products analytics API."""

from fastapi.testclient import TestClient

from bizintel.main import app


def test_products_endpoint_works_with_real_processed_data() -> None:
    """Products endpoint should work with actual processed datasets."""
    client = TestClient(app)

    response = client.get("/analytics/products")

    assert response.status_code == 200

    body = response.json()

    assert body["total_products"] > 0

    assert isinstance(
        body["products_by_category"],
        dict,
    )

    assert isinstance(
        body["product_revenue"],
        dict,
    )

    assert isinstance(
        body["product_order_items"],
        dict,
    )