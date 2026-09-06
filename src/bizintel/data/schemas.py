from typing import Final

CUSTOMER_SCHEMA: Final = {
    "customer_id": "string",
    "customer_unique_id": "string",
    "customer_zip_code_prefix": "int64",
    "customer_city": "string",
    "customer_state": "string",
}


ORDER_SCHEMA: Final = {
    "order_id": "string",
    "customer_id": "string",
    "order_status": "string",
    "order_purchase_timestamp": "datetime",
    "order_approved_at": "datetime",
    "order_delivered_carrier_date": "datetime",
    "order_delivered_customer_date": "datetime",
    "order_estimated_delivery_date": "datetime",
}


ORDER_ITEM_SCHEMA: Final = {
    "order_id": "string",
    "order_item_id": "int64",
    "product_id": "string",
    "seller_id": "string",
    "shipping_limit_date": "datetime",
    "price": "float64",
    "freight_value": "float64",
}


PAYMENT_SCHEMA: Final = {
    "order_id": "string",
    "payment_sequential": "int64",
    "payment_type": "string",
    "payment_installments": "int64",
    "payment_value": "float64",
}


DATASET_SCHEMAS: Final = {
    "customers": CUSTOMER_SCHEMA,
    "orders": ORDER_SCHEMA,
    "order_items": ORDER_ITEM_SCHEMA,
    "order_payments": PAYMENT_SCHEMA,
}