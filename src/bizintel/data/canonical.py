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