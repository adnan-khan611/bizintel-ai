"""Revenue analytics for BizIntel AI."""

import pandas as pd


def calculate_merchandise_revenue(
    order_items: pd.DataFrame,
) -> int:
    """Calculate total merchandise revenue in minor currency units."""
    if "price_minor" not in order_items.columns:
        raise ValueError(
            "Missing required column: price_minor"
        )

    return int(order_items["price_minor"].sum())


def calculate_freight_value(
    order_items: pd.DataFrame,
) -> int:
    """Calculate total freight value in minor currency units."""
    if "freight_value_minor" not in order_items.columns:
        raise ValueError(
            "Missing required column: freight_value_minor"
        )

    return int(order_items["freight_value_minor"].sum())


def calculate_payment_value(
    order_payments: pd.DataFrame,
) -> int:
    """Calculate total payment value in minor currency units."""
    if "payment_value_minor" not in order_payments.columns:
        raise ValueError(
            "Missing required column: payment_value_minor"
        )

    return int(order_payments["payment_value_minor"].sum())