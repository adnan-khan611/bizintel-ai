"""Products service layer for BizIntel AI."""

from pathlib import Path
from typing import Any

import pandas as pd

from bizintel.analytics.products import (
    calculate_product_order_item_counts,
    calculate_product_revenue,
    calculate_products_by_category,
    calculate_total_products,
)
from bizintel.api.analytics_data import load_analytics_datasets
from bizintel.api.products_schemas import ProductsResponse


def _series_to_dict(series: pd.Series) -> dict[str, Any]:
    """Convert a pandas Series into a JSON-compatible dictionary."""
    return {
        str(key): value.item()
        if hasattr(value, "item")
        else value
        for key, value in series.items()
    }


def get_products_analytics(
    processed_data_dir: Path,
) -> ProductsResponse:
    """Load product data and build the products response."""
    datasets = load_analytics_datasets(
        processed_data_dir
    )

    products = datasets["products"]
    order_items = datasets["order_items"]

    total_products = calculate_total_products(
        products
    )
    products_by_category = calculate_products_by_category(
        products
    )
    product_revenue = calculate_product_revenue(
        order_items
    )
    product_order_items = calculate_product_order_item_counts(
        order_items
    )

    return ProductsResponse(
        total_products=total_products,
        products_by_category=_series_to_dict(
            products_by_category
        ),
        product_revenue=_series_to_dict(
            product_revenue
        ),
        product_order_items=_series_to_dict(
            product_order_items
        ),
    )