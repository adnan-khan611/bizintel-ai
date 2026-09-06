from pathlib import Path

import pandas as pd

RAW_DATA_DIR = Path("data/raw")


def profile_order_items() -> None:
    """Profile numerical and date fields in order items."""
    file_path = RAW_DATA_DIR / "olist_order_items_dataset.csv"
    dataframe = pd.read_csv(file_path)

    print("\n" + "=" * 70)
    print("ORDER ITEMS BUSINESS RULE PROFILE")
    print("=" * 70)

    print("\nPrice:")
    print(f"  Minimum: {dataframe['price'].min()}")
    print(f"  Maximum: {dataframe['price'].max()}")
    print(f"  Zero values: {(dataframe['price'] == 0).sum():,}")
    print(f"  Negative values: {(dataframe['price'] < 0).sum():,}")

    print("\nFreight value:")
    print(f"  Minimum: {dataframe['freight_value'].min()}")
    print(f"  Maximum: {dataframe['freight_value'].max()}")
    print(f"  Zero values: {(dataframe['freight_value'] == 0).sum():,}")
    print(f"  Negative values: {(dataframe['freight_value'] < 0).sum():,}")

    shipping_dates = pd.to_datetime(
        dataframe["shipping_limit_date"],
        errors="coerce",
    )

    print("\nShipping limit date:")
    print(f"  Invalid dates: {shipping_dates.isna().sum():,}")
    print(f"  Earliest: {shipping_dates.min()}")
    print(f"  Latest: {shipping_dates.max()}")


def profile_payments() -> None:
    """Profile payment values, types, and installments."""
    file_path = RAW_DATA_DIR / "olist_order_payments_dataset.csv"
    dataframe = pd.read_csv(file_path)

    print("\n" + "=" * 70)
    print("PAYMENTS BUSINESS RULE PROFILE")
    print("=" * 70)

    print("\nPayment value:")
    print(f"  Minimum: {dataframe['payment_value'].min()}")
    print(f"  Maximum: {dataframe['payment_value'].max()}")
    print(f"  Zero values: {(dataframe['payment_value'] == 0).sum():,}")
    print(f"  Negative values: {(dataframe['payment_value'] < 0).sum():,}")

    print("\nPayment installments:")
    print(f"  Minimum: {dataframe['payment_installments'].min()}")
    print(f"  Maximum: {dataframe['payment_installments'].max()}")
    print(f"  Zero values: {(dataframe['payment_installments'] == 0).sum():,}")
    print(
        f"  Negative values: "
        f"{(dataframe['payment_installments'] < 0).sum():,}"
    )

    print("\nPayment types:")
    for payment_type, count in (
        dataframe["payment_type"].value_counts(dropna=False).items()
    ):
        print(f"  {payment_type}: {count:,}")

    zero_installments = dataframe[
        dataframe["payment_installments"] == 0
    ]

    print("\nPayment installments = 0 records:")
    if zero_installments.empty:
        print("  None")
    else:
        print(
            zero_installments[
                [
                    "order_id",
                    "payment_sequential",
                    "payment_type",
                    "payment_installments",
                    "payment_value",
                ]
            ].to_string(index=False)
        )

    zero_payment_value = dataframe[dataframe["payment_value"] == 0]

    print("\nPayment value = 0 records:")
    if zero_payment_value.empty:
        print("  None")
    else:
        print(
            zero_payment_value[
                [
                    "order_id",
                    "payment_sequential",
                    "payment_type",
                    "payment_installments",
                    "payment_value",
                ]
            ].to_string(index=False)
        )


def profile_orders() -> None:
    """Profile order dates and their chronological relationships."""
    file_path = RAW_DATA_DIR / "olist_orders_dataset.csv"
    dataframe = pd.read_csv(file_path)

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in date_columns:
        dataframe[column] = pd.to_datetime(
            dataframe[column],
            errors="coerce",
        )

    print("\n" + "=" * 70)
    print("ORDERS BUSINESS RULE PROFILE")
    print("=" * 70)

    print("\nInvalid date values:")

    for column in date_columns:
        invalid_count = int(dataframe[column].isna().sum())
        print(f"  {column}: {invalid_count:,}")

    purchase = dataframe["order_purchase_timestamp"]
    approved = dataframe["order_approved_at"]
    carrier = dataframe["order_delivered_carrier_date"]
    delivered = dataframe["order_delivered_customer_date"]

    approved_before_purchase = (
        approved.notna()
        & purchase.notna()
        & (approved < purchase)
    )

    carrier_before_purchase = (
        carrier.notna()
        & purchase.notna()
        & (carrier < purchase)
    )

    delivered_before_purchase = (
        delivered.notna()
        & purchase.notna()
        & (delivered < purchase)
    )

    print("\nChronological inconsistencies:")
    print(
        "  Approval before purchase: "
        f"{approved_before_purchase.sum():,}"
    )
    print(
        "  Carrier date before purchase: "
        f"{carrier_before_purchase.sum():,}"
    )
    print(
        "  Delivery before purchase: "
        f"{delivered_before_purchase.sum():,}"
    )

    carrier_anomalies = dataframe[carrier_before_purchase]

    print("\nCarrier date before purchase records:")
    if carrier_anomalies.empty:
        print("  None")
    else:
        print(
            carrier_anomalies[
                [
                    "order_id",
                    "order_status",
                    "order_purchase_timestamp",
                    "order_delivered_carrier_date",
                    "order_delivered_customer_date",
                ]
            ].head(20).to_string(index=False)
        )

        if len(carrier_anomalies) > 20:
            print(
                f"\n  Showing first 20 of "
                f"{len(carrier_anomalies):,} anomalous records."
            )

    print("\nOrder statuses:")
    for status, count in (
        dataframe["order_status"].value_counts(dropna=False).items()
    ):
        print(f"  {status}: {count:,}")


def main() -> None:
    """Run business-rule profiling on the core Olist datasets."""
    profile_order_items()
    profile_payments()
    profile_orders()


if __name__ == "__main__":
    main()