"""Canonical dataset transformations for BizIntel AI."""

import pandas as pd


def build_canonical_customers(
    customers: pd.DataFrame,
) -> pd.DataFrame:
    """Transform raw Olist customers into canonical customers."""

    required_columns = [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in customers.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required customer columns: "
            f"{', '.join(missing_columns)}"
        )

    canonical = customers[
        [
            "customer_unique_id",
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state",
        ]
    ].copy()

    canonical = canonical.rename(
        columns={
            "customer_unique_id": "customer_id",
        }
    )

    if canonical["customer_id"].isna().any():
        raise ValueError(
            "Canonical customer_id cannot contain missing values."
        )

    canonical = canonical.drop_duplicates(
        subset=["customer_id"],
        keep="first",
    ).reset_index(drop=True)

    return canonical
def build_canonical_products(
    products: pd.DataFrame,
) -> pd.DataFrame:
    """Transform raw Olist products into canonical products."""

    required_columns = [
        "product_id",
        "product_category_name",
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in products.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required product columns: "
            f"{', '.join(missing_columns)}"
        )

    canonical = products[required_columns].copy()

    canonical = canonical.rename(
        columns={
            "product_name_lenght": "product_name_length",
            "product_description_lenght": "product_description_length",
        }
    )

    nullable_integer_columns = [
        "product_name_length",
        "product_description_length",
        "product_photos_qty",
    ]

    for column in nullable_integer_columns:
        canonical[column] = canonical[column].astype("Int64")

    if canonical["product_id"].isna().any():
        raise ValueError(
            "Canonical product_id cannot contain missing values."
        )

    if not canonical["product_id"].is_unique:
        raise ValueError(
            "Canonical product_id must be unique."
        )

    return canonical