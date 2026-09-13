"""Tests for canonical dataset transformations."""
import pandas as pd
import pytest

from bizintel.data.canonical import (
    build_canonical_customers,
    build_canonical_order_items,
    build_canonical_order_payments,
    build_canonical_orders,
    build_canonical_products,
)


def test_build_canonical_customers_maps_columns_correctly():
    """Test customer columns map correctly."""
    raw = pd.DataFrame(
        {
            "customer_id": ["source-1", "source-2"],
            "customer_unique_id": ["customer-1", "customer-2"],
            "customer_zip_code_prefix": [12345, 67890],
            "customer_city": ["sao paulo", "rio de janeiro"],
            "customer_state": ["SP", "RJ"],
        }
    )

    result = build_canonical_customers(raw)

    assert list(result.columns) == [
        "customer_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
    ]

    assert result["customer_id"].tolist() == [
        "customer-1",
        "customer-2",
    ]


def test_build_canonical_customers_deduplicates_customer_identity():
    """Test duplicate customer identities are deduplicated."""
    raw = pd.DataFrame(
        {
            "customer_id": [
                "source-1",
                "source-2",
                "source-3",
            ],
            "customer_unique_id": [
                "customer-1",
                "customer-1",
                "customer-2",
            ],
            "customer_zip_code_prefix": [
                12345,
                12345,
                67890,
            ],
            "customer_city": [
                "sao paulo",
                "sao paulo",
                "rio de janeiro",
            ],
            "customer_state": [
                "SP",
                "SP",
                "RJ",
            ],
        }
    )

    result = build_canonical_customers(raw)

    assert len(result) == 2
    assert result["customer_id"].is_unique
    assert result["customer_id"].tolist() == [
        "customer-1",
        "customer-2",
    ]

    assert "source_customer_id" not in result.columns


def test_build_canonical_customers_keeps_first_record_deterministically():
    """Test first duplicate customer record is retained."""
    raw = pd.DataFrame(
        {
            "customer_id": ["source-1", "source-2"],
            "customer_unique_id": ["customer-1", "customer-1"],
            "customer_zip_code_prefix": [12345, 54321],
            "customer_city": ["sao paulo", "campinas"],
            "customer_state": ["SP", "SP"],
        }
    )

    result = build_canonical_customers(raw)

    assert len(result) == 1
    assert result.iloc[0]["customer_id"] == "customer-1"
    assert result.iloc[0]["customer_zip_code_prefix"] == 12345
    assert result.iloc[0]["customer_city"] == "sao paulo"
    assert result.iloc[0]["customer_state"] == "SP"


def test_build_canonical_customers_does_not_modify_input():
    """Test customer input is not modified."""
    raw = pd.DataFrame(
        {
            "customer_id": ["source-1"],
            "customer_unique_id": ["customer-1"],
            "customer_zip_code_prefix": [12345],
            "customer_city": ["sao paulo"],
            "customer_state": ["SP"],
        }
    )

    original = raw.copy(deep=True)

    build_canonical_customers(raw)

    pd.testing.assert_frame_equal(raw, original)


def test_build_canonical_customers_missing_column_raises_error():
    """Test missing customer columns raise an error."""
    raw = pd.DataFrame(
        {
            "customer_id": ["source-1"],
            "customer_zip_code_prefix": [12345],
            "customer_city": ["sao paulo"],
            "customer_state": ["SP"],
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required customer columns",
    ):
        build_canonical_customers(raw)


def test_build_canonical_customers_missing_customer_id_raises_error():
    """Test missing canonical customer ID raises an error."""
    raw = pd.DataFrame(
        {
            "customer_id": ["source-1"],
            "customer_unique_id": [None],
            "customer_zip_code_prefix": [12345],
            "customer_city": ["sao paulo"],
            "customer_state": ["SP"],
        }
    )

    with pytest.raises(
        ValueError,
        match="Canonical customer_id cannot contain missing values",
    ):
        build_canonical_customers(raw)


def test_build_canonical_products_maps_columns_correctly():
    """Test product columns map correctly."""
    raw = pd.DataFrame(
        {
            "product_id": ["product-1", "product-2"],
            "product_category_name": ["beleza", "informatica"],
            "product_name_lenght": [40.0, 50.0],
            "product_description_lenght": [100.0, 200.0],
            "product_photos_qty": [3.0, 5.0],
            "product_weight_g": [500.0, 1000.0],
            "product_length_cm": [20.0, 30.0],
            "product_height_cm": [10.0, 15.0],
            "product_width_cm": [5.0, 10.0],
        }
    )

    result = build_canonical_products(raw)

    assert list(result.columns) == [
        "product_id",
        "product_category_name",
        "product_name_length",
        "product_description_length",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]

    assert result["product_id"].tolist() == [
        "product-1",
        "product-2",
    ]


def test_build_canonical_products_converts_nullable_integer_columns():
    """Test nullable product integer columns use Int64."""
    raw = pd.DataFrame(
        {
            "product_id": ["product-1"],
            "product_category_name": ["beleza"],
            "product_name_lenght": [40.0],
            "product_description_lenght": [100.0],
            "product_photos_qty": [3.0],
            "product_weight_g": [500.0],
            "product_length_cm": [20.0],
            "product_height_cm": [10.0],
            "product_width_cm": [5.0],
        }
    )

    result = build_canonical_products(raw)

    assert str(result["product_name_length"].dtype) == "Int64"
    assert str(result["product_description_length"].dtype) == "Int64"
    assert str(result["product_photos_qty"].dtype) == "Int64"


def test_build_canonical_products_preserves_missing_values():
    """Test missing product values remain missing."""
    raw = pd.DataFrame(
        {
            "product_id": ["product-1"],
            "product_category_name": [None],
            "product_name_lenght": [None],
            "product_description_lenght": [None],
            "product_photos_qty": [None],
            "product_weight_g": [None],
            "product_length_cm": [None],
            "product_height_cm": [None],
            "product_width_cm": [None],
        }
    )

    result = build_canonical_products(raw)

    assert result["product_category_name"].isna().all()
    assert result["product_name_length"].isna().all()
    assert result["product_description_length"].isna().all()
    assert result["product_photos_qty"].isna().all()
    assert result["product_weight_g"].isna().all()
    assert result["product_length_cm"].isna().all()
    assert result["product_height_cm"].isna().all()
    assert result["product_width_cm"].isna().all()


def test_build_canonical_products_rejects_duplicate_product_id():
    """Test duplicate product IDs are rejected."""
    raw = pd.DataFrame(
        {
            "product_id": ["product-1", "product-1"],
            "product_category_name": ["beleza", "informatica"],
            "product_name_lenght": [40.0, 50.0],
            "product_description_lenght": [100.0, 200.0],
            "product_photos_qty": [3.0, 5.0],
            "product_weight_g": [500.0, 1000.0],
            "product_length_cm": [20.0, 30.0],
            "product_height_cm": [10.0, 15.0],
            "product_width_cm": [5.0, 10.0],
        }
    )

    with pytest.raises(
        ValueError,
        match="Canonical product_id must be unique",
    ):
        build_canonical_products(raw)


def test_build_canonical_orders_maps_columns():
    """Test canonical order columns and basic field mapping."""
    orders = pd.DataFrame(
        {
            "order_id": ["order_1"],
            "customer_id": ["raw_customer_1"],
            "order_status": ["delivered"],
            "order_purchase_timestamp": ["2018-01-01 10:00:00"],
            "order_approved_at": ["2018-01-01 10:05:00"],
            "order_delivered_carrier_date": ["2018-01-02 09:00:00"],
            "order_delivered_customer_date": ["2018-01-05 12:00:00"],
            "order_estimated_delivery_date": ["2018-01-10"],
        }
    )

    customers = pd.DataFrame(
        {
            "customer_id": ["raw_customer_1"],
            "customer_unique_id": ["unique_customer_1"],
        }
    )

    result = build_canonical_orders(orders, customers)

    assert list(result.columns) == [
        "order_id",
        "customer_id",
        "order_status",
        "order_date",
        "order_approved_at",
        "order_delivered_carrier_at",
        "order_delivered_customer_at",
        "order_estimated_delivery_at",
    ]

    assert result.loc[0, "order_id"] == "order_1"
    assert result.loc[0, "customer_id"] == "unique_customer_1"
    assert result.loc[0, "order_status"] == "delivered"


def test_build_canonical_orders_maps_customer_unique_id():
    """Test raw customer IDs map to canonical customer IDs."""
    orders = pd.DataFrame(
        {
            "order_id": ["order_1"],
            "customer_id": ["raw_customer_1"],
            "order_status": ["shipped"],
            "order_purchase_timestamp": ["2018-01-01 10:00:00"],
            "order_approved_at": ["2018-01-01 10:05:00"],
            "order_delivered_carrier_date": [None],
            "order_delivered_customer_date": [None],
            "order_estimated_delivery_date": ["2018-01-10"],
        }
    )

    customers = pd.DataFrame(
        {
            "customer_id": ["raw_customer_1"],
            "customer_unique_id": ["unique_customer_abc"],
        }
    )

    result = build_canonical_orders(orders, customers)

    assert result.loc[0, "customer_id"] == "unique_customer_abc"


def test_build_canonical_orders_converts_dates():
    """Test order date columns are converted to datetime."""
    orders = pd.DataFrame(
        {
            "order_id": ["order_1"],
            "customer_id": ["raw_customer_1"],
            "order_status": ["delivered"],
            "order_purchase_timestamp": ["2018-01-01 10:00:00"],
            "order_approved_at": ["2018-01-01 10:05:00"],
            "order_delivered_carrier_date": ["2018-01-02 09:00:00"],
            "order_delivered_customer_date": ["2018-01-05 12:00:00"],
            "order_estimated_delivery_date": ["2018-01-10"],
        }
    )

    customers = pd.DataFrame(
        {
            "customer_id": ["raw_customer_1"],
            "customer_unique_id": ["unique_customer_1"],
        }
    )

    result = build_canonical_orders(orders, customers)

    date_columns = [
        "order_date",
        "order_approved_at",
        "order_delivered_carrier_at",
        "order_delivered_customer_at",
        "order_estimated_delivery_at",
    ]

    for column in date_columns:
        assert pd.api.types.is_datetime64_any_dtype(result[column])


def test_build_canonical_orders_preserves_missing_dates():
    """Test missing lifecycle dates remain missing."""
    orders = pd.DataFrame(
        {
            "order_id": ["order_1"],
            "customer_id": ["raw_customer_1"],
            "order_status": ["processing"],
            "order_purchase_timestamp": ["2018-01-01 10:00:00"],
            "order_approved_at": [None],
            "order_delivered_carrier_date": [None],
            "order_delivered_customer_date": [None],
            "order_estimated_delivery_date": ["2018-01-10"],
        }
    )

    customers = pd.DataFrame(
        {
            "customer_id": ["raw_customer_1"],
            "customer_unique_id": ["unique_customer_1"],
        }
    )

    result = build_canonical_orders(orders, customers)

    assert pd.isna(result.loc[0, "order_approved_at"])
    assert pd.isna(result.loc[0, "order_delivered_carrier_at"])
    assert pd.isna(result.loc[0, "order_delivered_customer_at"])


def test_build_canonical_orders_rejects_duplicate_order_id():
    """Test duplicate order IDs are rejected."""
    orders = pd.DataFrame(
        {
            "order_id": ["order_1", "order_1"],
            "customer_id": ["raw_customer_1", "raw_customer_1"],
            "order_status": ["delivered", "delivered"],
            "order_purchase_timestamp": [
                "2018-01-01 10:00:00",
                "2018-01-01 11:00:00",
            ],
            "order_approved_at": [None, None],
            "order_delivered_carrier_date": [None, None],
            "order_delivered_customer_date": [None, None],
            "order_estimated_delivery_date": [
                "2018-01-10",
                "2018-01-10",
            ],
        }
    )

    customers = pd.DataFrame(
        {
            "customer_id": ["raw_customer_1"],
            "customer_unique_id": ["unique_customer_1"],
        }
    )

    with pytest.raises(
        ValueError,
        match="Duplicate order_id",
    ):
        build_canonical_orders(orders, customers)


def test_build_canonical_orders_rejects_unmapped_customer():
    """Test unknown customer IDs are rejected."""
    orders = pd.DataFrame(
        {
            "order_id": ["order_1"],
            "customer_id": ["unknown_customer"],
            "order_status": ["delivered"],
            "order_purchase_timestamp": ["2018-01-01 10:00:00"],
            "order_approved_at": [None],
            "order_delivered_carrier_date": [None],
            "order_delivered_customer_date": [None],
            "order_estimated_delivery_date": [
                "2018-01-10",
            ],
        }
    )

    customers = pd.DataFrame(
        {
            "customer_id": ["raw_customer_1"],
            "customer_unique_id": ["unique_customer_1"],
        }
    )

    with pytest.raises(
        ValueError,
        match="unmapped customer_id",
    ):
        build_canonical_orders(orders, customers)


def test_build_canonical_orders_rejects_missing_order_columns():
    """Test missing required order columns are rejected."""
    orders = pd.DataFrame(
        {
            "order_id": ["order_1"],
            "customer_id": ["raw_customer_1"],
        }
    )

    customers = pd.DataFrame(
        {
            "customer_id": ["raw_customer_1"],
            "customer_unique_id": ["unique_customer_1"],
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required order columns",
    ):
        build_canonical_orders(orders, customers)


def test_build_canonical_orders_does_not_modify_input():
    """Test source DataFrames remain unchanged."""
    orders = pd.DataFrame(
        {
            "order_id": ["order_1"],
            "customer_id": ["raw_customer_1"],
            "order_status": ["delivered"],
            "order_purchase_timestamp": ["2018-01-01 10:00:00"],
            "order_approved_at": [None],
            "order_delivered_carrier_date": [None],
            "order_delivered_customer_date": [None],
            "order_estimated_delivery_date": [
                "2018-01-10",
            ],
        }
    )

    customers = pd.DataFrame(
        {
            "customer_id": ["raw_customer_1"],
            "customer_unique_id": ["unique_customer_1"],
        }
    )

    orders_before = orders.copy(deep=True)
    customers_before = customers.copy(deep=True)

    build_canonical_orders(orders, customers)

    pd.testing.assert_frame_equal(orders, orders_before)
    pd.testing.assert_frame_equal(customers, customers_before)
    
def test_build_canonical_order_items_maps_columns() -> None:
    """Test canonical order item columns."""
    dataframe = pd.DataFrame(
        {
            "order_id": ["order-1"],
            "order_item_id": [1],
            "product_id": ["product-1"],
            "seller_id": ["seller-1"],
            "shipping_limit_date": ["2018-01-02 10:30:00"],
            "price": [58.90],
            "freight_value": [13.29],
        }
    )

    result = build_canonical_order_items(dataframe)

    assert list(result.columns) == [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_at",
        "price_minor",
        "freight_value_minor",
    ]


def test_build_canonical_order_items_converts_dates() -> None:
    """Test shipping limit date conversion."""
    dataframe = pd.DataFrame(
        {
            "order_id": ["order-1"],
            "order_item_id": [1],
            "product_id": ["product-1"],
            "seller_id": ["seller-1"],
            "shipping_limit_date": ["2018-01-02 10:30:00"],
            "price": [58.90],
            "freight_value": [13.29],
        }
    )

    result = build_canonical_order_items(dataframe)

    assert pd.api.types.is_datetime64_any_dtype(
        result["shipping_limit_at"]
    )


def test_build_canonical_order_items_converts_money_to_minor_units() -> None:
    """Test monetary values are converted to minor units."""
    dataframe = pd.DataFrame(
        {
            "order_id": ["order-1"],
            "order_item_id": [1],
            "product_id": ["product-1"],
            "seller_id": ["seller-1"],
            "shipping_limit_date": ["2018-01-02 10:30:00"],
            "price": [58.90],
            "freight_value": [13.29],
        }
    )

    result = build_canonical_order_items(dataframe)

    assert result["price_minor"].iloc[0] == 5890
    assert result["freight_value_minor"].iloc[0] == 1329


def test_build_canonical_order_items_rejects_duplicate_key() -> None:
    """Test duplicate order item keys are rejected."""
    dataframe = pd.DataFrame(
        {
            "order_id": ["order-1", "order-1"],
            "order_item_id": [1, 1],
            "product_id": ["product-1", "product-1"],
            "seller_id": ["seller-1", "seller-1"],
            "shipping_limit_date": [
                "2018-01-02 10:30:00",
                "2018-01-02 10:30:00",
            ],
            "price": [58.90, 58.90],
            "freight_value": [13.29, 13.29],
        }
    )

    with pytest.raises(
        ValueError,
        match="Duplicate order_id \\+ order_item_id combinations found",
    ):
        build_canonical_order_items(dataframe)


def test_build_canonical_order_items_missing_column_raises_error() -> None:
    """Test missing required column."""
    dataframe = pd.DataFrame(
        {
            "order_id": ["order-1"],
            "order_item_id": [1],
            "product_id": ["product-1"],
            "seller_id": ["seller-1"],
            "shipping_limit_date": ["2018-01-02 10:30:00"],
            "price": [58.90],
        }
    )

    with pytest.raises(
        ValueError,
        match="Missing required order item columns",
    ):
        build_canonical_order_items(dataframe)


def test_build_canonical_order_items_does_not_modify_input() -> None:
    """Test input DataFrame remains unchanged."""
    dataframe = pd.DataFrame(
        {
            "order_id": ["order-1"],
            "order_item_id": [1],
            "product_id": ["product-1"],
            "seller_id": ["seller-1"],
            "shipping_limit_date": ["2018-01-02 10:30:00"],
            "price": [58.90],
            "freight_value": [13.29],
        }
    )

    original = dataframe.copy(deep=True)

    build_canonical_order_items(dataframe)

    pd.testing.assert_frame_equal(dataframe, original)
    
def test_build_canonical_order_payments_maps_columns():
    payments = pd.DataFrame(
        {
            "order_id": ["order-1", "order-2"],
            "payment_sequential": [1, 1],
            "payment_type": ["credit_card", "boleto"],
            "payment_installments": [2, 1],
            "payment_value": [100.50, 250.75],
        }
    )

    result = build_canonical_order_payments(payments)

    assert list(result.columns) == [
        "payment_id",
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value_minor",
    ]

    assert result["payment_id"].tolist() == [
        "order-1_1",
        "order-2_1",
    ]


def test_build_canonical_order_payments_converts_money_to_minor_units():
    payments = pd.DataFrame(
        {
            "order_id": ["order-1", "order-2"],
            "payment_sequential": [1, 1],
            "payment_type": ["credit_card", "boleto"],
            "payment_installments": [2, 1],
            "payment_value": [100.50, 250.75],
        }
    )

    result = build_canonical_order_payments(payments)

    assert result["payment_value_minor"].tolist() == [
        10050,
        25075,
    ]


def test_build_canonical_order_payments_creates_unique_payment_id():
    payments = pd.DataFrame(
        {
            "order_id": ["order-1", "order-1"],
            "payment_sequential": [1, 2],
            "payment_type": ["credit_card", "voucher"],
            "payment_installments": [2, 1],
            "payment_value": [100.50, 50.25],
        }
    )

    result = build_canonical_order_payments(payments)

    assert result["payment_id"].is_unique
    assert result["payment_id"].tolist() == [
        "order-1_1",
        "order-1_2",
    ]


def test_build_canonical_order_payments_rejects_duplicate_key():
    payments = pd.DataFrame(
        {
            "order_id": ["order-1", "order-1"],
            "payment_sequential": [1, 1],
            "payment_type": ["credit_card", "credit_card"],
            "payment_installments": [2, 2],
            "payment_value": [100.50, 100.50],
        }
    )

    with pytest.raises(ValueError, match="Duplicate"):
        build_canonical_order_payments(payments)


def test_build_canonical_order_payments_missing_column_raises_error():
    payments = pd.DataFrame(
        {
            "order_id": ["order-1"],
            "payment_sequential": [1],
            "payment_type": ["credit_card"],
            "payment_installments": [2],
        }
    )

    with pytest.raises(ValueError, match="Missing required payment columns"):
        build_canonical_order_payments(payments)


def test_build_canonical_order_payments_does_not_modify_input():
    payments = pd.DataFrame(
        {
            "order_id": ["order-1"],
            "payment_sequential": [1],
            "payment_type": ["credit_card"],
            "payment_installments": [2],
            "payment_value": [100.50],
        }
    )

    original = payments.copy(deep=True)

    build_canonical_order_payments(payments)

    pd.testing.assert_frame_equal(payments, original)