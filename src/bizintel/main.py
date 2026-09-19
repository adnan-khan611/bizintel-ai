"""FastAPI application entry point."""

from fastapi import FastAPI

from bizintel.api.analytics_schemas import AnalyticsSummaryResponse
from bizintel.api.analytics_service import get_analytics_summary
from bizintel.api.customers_schemas import CustomersResponse
from bizintel.api.customers_service import get_customers_analytics
from bizintel.api.growth_schemas import GrowthResponse
from bizintel.api.growth_service import get_growth_analytics
from bizintel.api.orders_schemas import OrdersResponse
from bizintel.api.orders_service import get_orders_analytics
from bizintel.api.products_schemas import ProductsResponse
from bizintel.api.products_service import get_products_analytics
from bizintel.api.revenue_schemas import RevenueResponse
from bizintel.api.revenue_service import get_revenue_analytics
from bizintel.api.schemas import HealthResponse
from bizintel.config import settings


def create_app() -> FastAPI:
    """Create and configure the BizIntel AI API application."""
    app = FastAPI(title=settings.app_name)

    @app.get(
        "/health",
        response_model=HealthResponse,
    )
    def health_check() -> HealthResponse:
        """Return the service health status."""
        return HealthResponse(status="ok")

    @app.get(
        "/analytics/summary",
        response_model=AnalyticsSummaryResponse,
    )
    def analytics_summary() -> AnalyticsSummaryResponse:
        """Return the combined business analytics summary."""
        summary = get_analytics_summary(
            settings.processed_data_dir
        )

        return AnalyticsSummaryResponse(
            **summary
        )

    @app.get(
        "/analytics/revenue",
        response_model=RevenueResponse,
    )
    def analytics_revenue() -> RevenueResponse:
        """Return revenue analytics."""
        return get_revenue_analytics(
            settings.processed_data_dir
        )

    @app.get(
        "/analytics/orders",
        response_model=OrdersResponse,
    )
    def analytics_orders() -> OrdersResponse:
        """Return order analytics."""
        return get_orders_analytics(
            settings.processed_data_dir
        )

    @app.get(
        "/analytics/customers",
        response_model=CustomersResponse,
    )
    def analytics_customers() -> CustomersResponse:
        """Return customer analytics."""
        return get_customers_analytics(
            settings.processed_data_dir
        )

    @app.get(
        "/analytics/products",
        response_model=ProductsResponse,
    )
    def analytics_products() -> ProductsResponse:
        """Return product analytics."""
        return get_products_analytics(
            settings.processed_data_dir
        )

    @app.get(
        "/analytics/growth",
        response_model=GrowthResponse,
    )
    def analytics_growth() -> GrowthResponse:
        """Return growth analytics."""
        return get_growth_analytics(
            settings.processed_data_dir
        )

    return app


app = create_app()