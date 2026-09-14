import pandas as pd
import pytest

from bizintel.analytics.summary import build_analytics_summary


def create_test_data() -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    customers = pd.DataFrame(
        {
            "customer_id": ["c1", "c2"],
            "customer_zip_code_prefix": [1000, 2000],
            "customer_city": ["City A", "City B"],
            "customer_state": ["SP", "RJ"],
        }
    )

    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "customer_id": ["c1", "c1", "c2"],
            "order_status": ["delivered", "canceled", "delivered"],
            "order_date": pd.to_datetime(
                [
                    "2024-01-10",
                    "2024-01-20",
                    "2024-03-05",
                ]
            ),
        }
    )

    products = pd.DataFrame(
        {
            "product_id": ["p1", "p2"],
            "product_category_name": [
                "electronics",
                "furniture",
            ],
        }
    )

    order_items = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "order_item_id": [1, 1, 1],
            "product_id": ["p1", "p1", "p2"],
            "seller_id": ["s1", "s1", "s2"],
            "shipping_limit_at": pd.to_datetime(
                [
                    "2024-01-15",
                    "2024-01-25",
                    "2024-03-10",
                ]
            ),
            "price_minor": [1000, 2000, 3000],
            "freight_value_minor": [100, 200, 300],
        }
    )

    order_payments = pd.DataFrame(
        {
            "payment_id": ["o1_1", "o2_1", "o3_1"],
            "order_id": ["o1", "o2", "o3"],
            "payment_sequential": [1, 1, 1],
            "payment_type": [
                "credit_card",
                "boleto",
                "credit_card",
            ],
            "payment_installments": [2, 1, 3],
            "payment_value_minor": [1100, 2200, 3300],
        }
    )

    return (
        customers,
        orders,
        products,
        order_items,
        order_payments,
    )


def test_build_analytics_summary_contains_expected_sections() -> None:
    data = create_test_data()

    summary = build_analytics_summary(*data)

    assert set(summary) == {
        "revenue",
        "orders",
        "customers",
        "products",
        "growth",
    }


def test_summary_revenue_metrics() -> None:
    data = create_test_data()

    summary = build_analytics_summary(*data)

    assert summary["revenue"]["merchandise_revenue_minor"] == 6000
    assert summary["revenue"]["freight_value_minor"] == 600
    assert summary["revenue"]["payment_value_minor"] == 6600


def test_summary_order_metrics() -> None:
    data = create_test_data()

    summary = build_analytics_summary(*data)

    assert summary["orders"]["total_orders"] == 3
    assert summary["orders"]["delivered_orders"] == 2
    assert summary["orders"]["canceled_orders"] == 1
    assert summary["orders"]["unavailable_orders"] == 0


def test_summary_customer_metrics() -> None:
    data = create_test_data()

    summary = build_analytics_summary(*data)

    assert summary["customers"]["unique_customers"] == 2
    assert summary["customers"]["orders_per_customer"] == 1.5


def test_summary_product_metrics() -> None:
    data = create_test_data()

    summary = build_analytics_summary(*data)

    assert summary["products"]["total_products"] == 2

    expected_categories = pd.Series(
        [1, 1],
        index=pd.Index(
            ["electronics", "furniture"],
            name="product_category_name",
        ),
        name="product_id",
    )

    pd.testing.assert_series_equal(
        summary["products"]["products_by_category"],
        expected_categories,
    )

    expected_revenue = pd.Series(
        [3000, 3000],
        index=pd.Index(
            ["p1", "p2"],
            name="product_id",
        ),
        name="price_minor",
    )

    pd.testing.assert_series_equal(
        summary["products"]["product_revenue"],
        expected_revenue,
    )


def test_summary_growth_metrics() -> None:
    data = create_test_data()

    summary = build_analytics_summary(*data)

    expected_months = pd.PeriodIndex(
        ["2024-01", "2024-02", "2024-03"],
        freq="M",
        name="month",
    )

    assert summary["growth"]["monthly_revenue"].index.equals(
        expected_months
    )
    assert summary["growth"]["monthly_orders"].index.equals(
        expected_months
    )
    assert summary["growth"]["monthly_unique_customers"].index.equals(
        expected_months
    )

    assert summary["growth"]["monthly_revenue"].tolist() == [
        3000,
        0,
        3000,
    ]

    assert summary["growth"]["monthly_orders"].tolist() == [
        2,
        0,
        1,
    ]

    assert summary["growth"]["monthly_unique_customers"].tolist() == [
        1,
        0,
        1,
    ]


def test_summary_growth_calculations() -> None:
    data = create_test_data()

    summary = build_analytics_summary(*data)

    revenue_growth = summary["growth"]["revenue_growth"]
    order_growth = summary["growth"]["order_growth"]

    # First month has no previous month.
    assert pd.isna(revenue_growth.iloc[0])
    assert pd.isna(order_growth.iloc[0])

    # February has a previous month with revenue/orders.
    assert revenue_growth.iloc[1] == -100.0
    assert order_growth.iloc[1] == -100.0

    # March follows a zero-activity month, so growth is undefined.
    assert pd.isna(revenue_growth.iloc[2])
    assert pd.isna(order_growth.iloc[2])


def test_summary_requires_product_id() -> None:
    customers, orders, products, order_items, order_payments = (
        create_test_data()
    )

    products = products.drop(columns=["product_id"])

    with pytest.raises(ValueError, match="product_id"):
        build_analytics_summary(
            customers,
            orders,
            products,
            order_items,
            order_payments,
        )


def test_summary_requires_payment_value() -> None:
    customers, orders, products, order_items, order_payments = (
        create_test_data()
    )

    order_payments = order_payments.drop(
        columns=["payment_value_minor"]
    )

    with pytest.raises(ValueError, match="payment_value_minor"):
        build_analytics_summary(
            customers,
            orders,
            products,
            order_items,
            order_payments,
        )


def test_summary_requires_order_date() -> None:
    customers, orders, products, order_items, order_payments = (
        create_test_data()
    )

    orders = orders.drop(columns=["order_date"])

    with pytest.raises(ValueError, match="order_date"):
        build_analytics_summary(
            customers,
            orders,
            products,
            order_items,
            order_payments,
        )