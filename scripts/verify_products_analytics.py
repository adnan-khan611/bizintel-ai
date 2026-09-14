"""Verify product analytics against the processed Olist datasets."""

from pathlib import Path

import pandas as pd

from bizintel.analytics.products import (
    calculate_product_order_item_counts,
    calculate_product_revenue,
    calculate_products_by_category,
    calculate_top_products_by_order_items,
    calculate_top_products_by_revenue,
    calculate_total_products,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_FILE = PROJECT_ROOT / "data" / "processed" / "products.parquet"
ORDER_ITEMS_FILE = (
    PROJECT_ROOT / "data" / "processed" / "order_items.parquet"
)


def main() -> None:
    """Run product analytics against the canonical datasets."""
    products = pd.read_parquet(PRODUCTS_FILE)
    order_items = pd.read_parquet(ORDER_ITEMS_FILE)

    total_products = calculate_total_products(products)
    products_by_category = calculate_products_by_category(products)
    product_revenue = calculate_product_revenue(order_items)
    product_order_items = calculate_product_order_item_counts(order_items)
    top_by_revenue = calculate_top_products_by_revenue(
        order_items,
        limit=10,
    )
    top_by_order_items = calculate_top_products_by_order_items(
        order_items,
        limit=10,
    )

    print("Products Analytics Verification")
    print("=" * 40)

    print(f"Total Products: {total_products:,}")

    print("\nTop 10 Categories by Product Count:")
    for category, count in products_by_category.head(10).items():
        print(f"  {category}: {count:,}")

    print("\nTop 10 Products by Revenue:")
    for product_id, revenue_minor in top_by_revenue.items():
        revenue = revenue_minor / 100
        print(f"  {product_id}: R$ {revenue:,.2f}")

    print("\nTop 10 Products by Order-Item Count:")
    for product_id, count in top_by_order_items.items():
        print(f"  {product_id}: {count:,}")

    print("\nProduct Analytics Summary:")
    print(f"  Products with revenue: {len(product_revenue):,}")
    print(f"  Products with order items: {len(product_order_items):,}")


if __name__ == "__main__":
    main()