"""Product analytics for BizIntel AI."""

import pandas as pd


def calculate_total_products(products: pd.DataFrame) -> int:
    """Calculate the number of distinct products."""
    if "product_id" not in products.columns:
        raise ValueError("Missing required column: product_id")

    return int(products["product_id"].nunique())


def calculate_products_by_category(
    products: pd.DataFrame,
) -> pd.Series:
    """Calculate the number of products in each category."""
    required_columns = {"product_id", "product_category_name"}

    missing_columns = required_columns - set(products.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    categories = products["product_category_name"].fillna("unknown")

    return (
        products.assign(product_category_name=categories)
        .groupby("product_category_name")["product_id"]
        .nunique()
        .sort_values(ascending=False)
    )


def calculate_product_revenue(
    order_items: pd.DataFrame,
) -> pd.Series:
    """Calculate merchandise revenue for each product."""
    required_columns = {"product_id", "price_minor"}

    missing_columns = required_columns - set(order_items.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    return (
        order_items.groupby("product_id")["price_minor"]
        .sum()
        .sort_values(ascending=False)
    )


def calculate_product_order_item_counts(
    order_items: pd.DataFrame,
) -> pd.Series:
    """Calculate order-item count for each product."""
    required_columns = {"product_id", "order_id", "order_item_id"}

    missing_columns = required_columns - set(order_items.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    return (
        order_items.groupby("product_id")
        .size()
        .sort_values(ascending=False)
    )


def calculate_top_products_by_revenue(
    order_items: pd.DataFrame,
    limit: int = 10,
) -> pd.Series:
    """Return products with the highest merchandise revenue."""
    if limit < 1:
        raise ValueError("limit must be at least 1")

    product_revenue = calculate_product_revenue(order_items)

    return product_revenue.head(limit)


def calculate_top_products_by_order_items(
    order_items: pd.DataFrame,
    limit: int = 10,
) -> pd.Series:
    """Return products with the highest order-item counts."""
    if limit < 1:
        raise ValueError("limit must be at least 1")

    order_item_counts = calculate_product_order_item_counts(order_items)

    return order_item_counts.head(limit)