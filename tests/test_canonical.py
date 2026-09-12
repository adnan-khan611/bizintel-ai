"""Tests for canonical dataset transformations."""

import pandas as pd
import pytest

from bizintel.data.canonical import build_canonical_customers, build_canonical_products


def test_build_canonical_customers_maps_columns_correctly():
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
    raw = pd.DataFrame(
        {
            "customer_id": ["source-1"],
            "customer_unique_id": ["customer-1"],
            "customer_zip_code_prefix": [12345],
            "customer_city": ["sao paulo"],
            "customer_state": ["SP"],
        }
    )

    original = raw.copy()

    build_canonical_customers(raw)

    pd.testing.assert_frame_equal(raw, original)


def test_build_canonical_customers_missing_column_raises_error():
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