"""Tests for the growth analytics API endpoint."""

from fastapi.testclient import TestClient

from bizintel.main import app


def test_growth_endpoint_returns_expected_contract(
    monkeypatch,
) -> None:
    """Growth endpoint should return the expected response."""
    import bizintel.main as main

    monkeypatch.setattr(
        main,
        "get_growth_analytics",
        lambda processed_data_dir: {
            "monthly_revenue": {
                "2017-01": 1000,
                "2017-02": 1200,
            },
            "monthly_orders": {
                "2017-01": 100,
                "2017-02": 120,
            },
            "monthly_unique_customers": {
                "2017-01": 90,
                "2017-02": 105,
            },
            "revenue_growth": {
                "2017-02": 0.20,
            },
            "order_growth": {
                "2017-02": 0.20,
            },
        },
    )

    client = TestClient(app)

    response = client.get("/analytics/growth")

    assert response.status_code == 200

    body = response.json()

    assert set(body) == {
        "monthly_revenue",
        "monthly_orders",
        "monthly_unique_customers",
        "revenue_growth",
        "order_growth",
    }

    assert body["monthly_revenue"] == {
        "2017-01": 1000,
        "2017-02": 1200,
    }
    assert body["monthly_orders"] == {
        "2017-01": 100,
        "2017-02": 120,
    }
    assert body["monthly_unique_customers"] == {
        "2017-01": 90,
        "2017-02": 105,
    }
    assert body["revenue_growth"] == {
        "2017-02": 0.20,
    }
    assert body["order_growth"] == {
        "2017-02": 0.20,
    }


def test_growth_endpoint_exposes_openapi_schema() -> None:
    """Growth endpoint should expose its response model in OpenAPI."""
    client = TestClient(app)

    response = client.get("/openapi.json")

    assert response.status_code == 200

    openapi = response.json()

    growth_operation = openapi["paths"]["/analytics/growth"]["get"]

    assert growth_operation["responses"]["200"]["content"][
        "application/json"
    ]["schema"]["$ref"] == (
        "#/components/schemas/GrowthResponse"
    )

    assert "GrowthResponse" in openapi["components"]["schemas"]