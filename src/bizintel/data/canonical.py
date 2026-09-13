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


def build_canonical_orders(
    orders_dataframe: pd.DataFrame,
    customers_dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Build the canonical orders dataset."""
    required_order_columns = [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    required_customer_columns = [
        "customer_id",
        "customer_unique_id",
    ]

    missing_order_columns = [
        column
        for column in required_order_columns
        if column not in orders_dataframe.columns
    ]

    if missing_order_columns:
        raise ValueError(
            "Missing required order columns: "
            f"{missing_order_columns}"
        )

    missing_customer_columns = [
        column
        for column in required_customer_columns
        if column not in customers_dataframe.columns
    ]

    if missing_customer_columns:
        raise ValueError(
            "Missing required customer columns: "
            f"{missing_customer_columns}"
        )

    if orders_dataframe["order_id"].duplicated().any():
        raise ValueError("Duplicate order_id values found.")

    customer_mapping = customers_dataframe[
        ["customer_id", "customer_unique_id"]
    ].copy()

    if customer_mapping["customer_id"].duplicated().any():
        raise ValueError(
            "Duplicate customer_id values found in customer mapping."
        )

    customer_mapping = customer_mapping.set_index("customer_id")[
        "customer_unique_id"
    ]

    canonical_customer_ids = orders_dataframe["customer_id"].map(
        customer_mapping
    )

    if canonical_customer_ids.isna().any():
        missing_count = int(canonical_customer_ids.isna().sum())
        raise ValueError(
            "Found "
            f"{missing_count:,} orders with unmapped customer_id values."
        )

    canonical_orders = pd.DataFrame(
        {
            "order_id": orders_dataframe["order_id"].copy(),
            "customer_id": canonical_customer_ids,
            "order_status": orders_dataframe["order_status"].copy(),
            "order_date": pd.to_datetime(
                orders_dataframe["order_purchase_timestamp"],
                errors="coerce",
            ),
            "order_approved_at": pd.to_datetime(
                orders_dataframe["order_approved_at"],
                errors="coerce",
            ),
            "order_delivered_carrier_at": pd.to_datetime(
                orders_dataframe["order_delivered_carrier_date"],
                errors="coerce",
            ),
            "order_delivered_customer_at": pd.to_datetime(
                orders_dataframe["order_delivered_customer_date"],
                errors="coerce",
            ),
            "order_estimated_delivery_at": pd.to_datetime(
                orders_dataframe["order_estimated_delivery_date"],
                errors="coerce",
            ),
        }
    )

    return canonical_orders