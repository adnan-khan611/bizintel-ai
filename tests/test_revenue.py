import pandas as pd

from bizintel.analytics.revenue import (
    calculate_freight_value,
    calculate_merchandise_revenue,
    calculate_payment_value,
)


def test_calculate_merchandise_revenue():
    order_items = pd.DataFrame(
        {
            "price_minor": [1000, 2500, 1500],
        }
    )

    result = calculate_merchandise_revenue(order_items)

    assert result == 5000


def test_calculate_merchandise_revenue_with_zero_values():
    order_items = pd.DataFrame(
        {
            "price_minor": [1000, 0, 2500],
        }
    )

    result = calculate_merchandise_revenue(order_items)

    assert result == 3500


def test_calculate_freight_value():
    order_items = pd.DataFrame(
        {
            "freight_value_minor": [100, 250, 150],
        }
    )

    result = calculate_freight_value(order_items)

    assert result == 500


def test_calculate_payment_value():
    order_payments = pd.DataFrame(
        {
            "payment_value_minor": [1000, 2500, 1500],
        }
    )

    result = calculate_payment_value(order_payments)

    assert result == 5000


def test_missing_price_column():
    order_items = pd.DataFrame(
        {
            "freight_value_minor": [100, 200],
        }
    )

    try:
        calculate_merchandise_revenue(order_items)
        assert False
    except ValueError as error:
        assert "price_minor" in str(error)


def test_missing_freight_column():
    order_items = pd.DataFrame(
        {
            "price_minor": [1000, 2000],
        }
    )

    try:
        calculate_freight_value(order_items)
        assert False
    except ValueError as error:
        assert "freight_value_minor" in str(error)


def test_missing_payment_column():
    order_payments = pd.DataFrame(
        {
            "payment_type": ["credit_card", "boleto"],
        }
    )

    try:
        calculate_payment_value(order_payments)
        assert False
    except ValueError as error:
        assert "payment_value_minor" in str(error)