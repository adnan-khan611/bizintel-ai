"""Tests for canonical dataset transformations."""

import pandas as pd
import pytest

from bizintel.data.canonical import build_canonical_customers


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