"""Verify analytics summary against the processed Olist datasets."""

from pathlib import Path

import pandas as pd

from bizintel.analytics.summary import build_analytics_summary

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CUSTOMERS_FILE = PROJECT_ROOT / "data" / "processed" / "customers.parquet"
ORDERS_FILE = PROJECT_ROOT / "data" / "processed" / "orders.parquet"
PRODUCTS_FILE = PROJECT_ROOT / "data" / "processed" / "products.parquet"
ORDER_ITEMS_FILE = (
    PROJECT_ROOT / "data" / "processed" / "order_items.parquet"
)
ORDER_PAYMENTS_FILE = (
    PROJECT_ROOT / "data" / "processed" / "order_payments.parquet"
)


def main() -> None:
    """Run the complete analytics summary against canonical datasets."""

    customers = pd.read_parquet(CUSTOMERS_FILE)
    orders = pd.read_parquet(ORDERS_FILE)
    products = pd.read_parquet(PRODUCTS_FILE)
    order_items = pd.read_parquet(ORDER_ITEMS_FILE)
    order_payments = pd.read_parquet(ORDER_PAYMENTS_FILE)

    summary = build_analytics_summary(
        customers=customers,
        orders=orders,
        products=products,
        order_items=order_items,
        order_payments=order_payments,
    )

    revenue = summary["revenue"]
    order_metrics = summary["orders"]
    customer_metrics = summary["customers"]
    product_metrics = summary["products"]
    growth = summary["growth"]

    print("Analytics Summary Verification")
    print("=" * 50)

    print("\nRevenue:")
    print(
        "  Merchandise Revenue: "
        f"R$ {revenue['merchandise_revenue_minor'] / 100:,.2f}"
    )
    print(
        "  Freight Value: "
        f"R$ {revenue['freight_value_minor'] / 100:,.2f}"
    )
    print(
        "  Payment Value: "
        f"R$ {revenue['payment_value_minor'] / 100:,.2f}"
    )

    print("\nOrders:")
    print(f"  Total Orders: {order_metrics['total_orders']:,}")
    print(f"  Delivered Orders: {order_metrics['delivered_orders']:,}")
    print(f"  Canceled Orders: {order_metrics['canceled_orders']:,}")
    print(
        f"  Unavailable Orders: "
        f"{order_metrics['unavailable_orders']:,}"
    )

    print("\nCustomers:")
    print(
        f"  Unique Customers: "
        f"{customer_metrics['unique_customers']:,}"
    )
    print(
        f"  Orders per Customer: "
        f"{customer_metrics['orders_per_customer']:.4f}"
    )

    print("\nProducts:")
    print(
        f"  Total Products: "
        f"{product_metrics['total_products']:,}"
    )

    print("\nTop 10 Product Categories:")
    for category, count in (
        product_metrics["products_by_category"].head(10).items()
    ):
        print(f"  {category}: {count:,}")

    print("\nTop 10 Products by Revenue:")
    for product_id, revenue_minor in (
        product_metrics["product_revenue"].head(10).items()
    ):
        print(
            f"  {product_id}: "
            f"R$ {revenue_minor / 100:,.2f}"
        )

    print("\nTop 10 Products by Order-Item Count:")
    for product_id, count in (
        product_metrics["product_order_items"].head(10).items()
    ):
        print(f"  {product_id}: {count:,}")

    print("\nGrowth:")
    print(
        f"  Revenue Months: "
        f"{len(growth['monthly_revenue']):,}"
    )
    print(
        f"  Order Months: "
        f"{len(growth['monthly_orders']):,}"
    )
    print(
        f"  Customer Months: "
        f"{len(growth['monthly_unique_customers']):,}"
    )

    print("\nLatest Monthly Revenue:")
    for month, revenue_minor in growth["monthly_revenue"].tail(5).items():
        print(
            f"  {month}: "
            f"R$ {revenue_minor / 100:,.2f}"
        )

    print("\nLatest Monthly Orders:")
    for month, count in growth["monthly_orders"].tail(5).items():
        print(f"  {month}: {count:,}")

    print("\nLatest Revenue Growth:")
    for month, growth_value in growth["revenue_growth"].tail(5).items():
        if pd.isna(growth_value):
            print(f"  {month}: N/A")
        else:
            print(f"  {month}: {growth_value:.2f}%")

    print("\nLatest Order Growth:")
    for month, growth_value in growth["order_growth"].tail(5).items():
        if pd.isna(growth_value):
            print(f"  {month}: N/A")
        else:
            print(f"  {month}: {growth_value:.2f}%")

    print("\nSummary Structure:")
    for section, values in summary.items():
        print(
            f"  {section}: "
            f"{len(values)} metrics"
        )


if __name__ == "__main__":
    main()