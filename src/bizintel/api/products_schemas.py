"""Products API response schemas for BizIntel AI."""

from typing import Any

from pydantic import BaseModel


class ProductsResponse(BaseModel):
    """Response schema for product analytics."""

    total_products: int
    products_by_category: dict[str, Any]
    product_revenue: dict[str, Any]
    product_order_items: dict[str, Any]