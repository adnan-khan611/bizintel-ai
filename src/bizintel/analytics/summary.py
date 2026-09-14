"""Business analytics summary for BizIntel AI."""

from typing import Any

import pandas as pd

from bizintel.analytics.customers import (
    calculate_orders_per_customer,
    calculate_unique_customers,
)
from bizintel.analytics.growth import (
    calculate_monthly_orders,
    calculate_monthly_revenue,
    calculate_monthly_unique_customers,
    calculate_order_growth,
    calculate_revenue_growth,
)
from bizintel.analytics.orders import (
    calculate_canceled_orders,
    calculate_delivered_orders,
    calculate_total_orders,
    calculate_unavailable_orders,
)
from bizintel.analytics.products import (
    calculate_product_order_item_counts,
    calculate_product_revenue,
    calculate_products_by_category,
)
from bizintel.analytics.revenue import (
    calculate_freight_value,
    calculate_merchandise_revenue,
    calculate_payment_value,
)


def build_analytics_summary(
    customers: pd.DataFrame,
    orders: pd.DataFrame,
    products: pd.DataFrame,
    order_items: pd.DataFrame,
    order_payments: pd.DataFrame,
) -> dict[str, Any]:
    """Build a combined business-facing analytics summary."""

    merchandise_revenue = calculate_merchandise_revenue(order_items)
    freight_value = calculate_freight_value(order_items)
    payment_value = calculate_payment_value(order_payments)

    total_orders = calculate_total_orders(orders)
    delivered_orders = calculate_delivered_orders(orders)
    canceled_orders = calculate_canceled_orders(orders)
    unavailable_orders = calculate_unavailable_orders(orders)

    unique_customers = calculate_unique_customers(customers)
    orders_per_customer = calculate_orders_per_customer(
        orders,
        customers,
    )

    products_by_category = calculate_products_by_category(products)
    product_revenue = calculate_product_revenue(order_items)
    product_order_items = calculate_product_order_item_counts(order_items)

    monthly_revenue = calculate_monthly_revenue(
        orders,
        order_items,
    )
    monthly_orders = calculate_monthly_orders(orders)
    monthly_customers = calculate_monthly_unique_customers(orders)

    revenue_growth = calculate_revenue_growth(monthly_revenue)
    order_growth = calculate_order_growth(monthly_orders)

    return {
        "revenue": {
            "merchandise_revenue_minor": merchandise_revenue,
            "freight_value_minor": freight_value,
            "payment_value_minor": payment_value,
        },
        "orders": {
            "total_orders": total_orders,
            "delivered_orders": delivered_orders,
            "canceled_orders": canceled_orders,
            "unavailable_orders": unavailable_orders,
        },
        "customers": {
            "unique_customers": unique_customers,
            "orders_per_customer": orders_per_customer,
        },
        "products": {
            "total_products": int(products["product_id"].nunique()),
            "products_by_category": products_by_category,
            "product_revenue": product_revenue,
            "product_order_items": product_order_items,
        },
        "growth": {
            "monthly_revenue": monthly_revenue,
            "monthly_orders": monthly_orders,
            "monthly_unique_customers": monthly_customers,
            "revenue_growth": revenue_growth,
            "order_growth": order_growth,
        },
    }