# Phase 3 — Canonical Processed-Data Schema

## 1. Purpose

This document defines the canonical processed-data schema used internally by BizIntel AI after raw source data has been ingested, validated, and standardized.

The canonical schema provides a stable internal contract between the data-engineering layer and downstream analytics, machine-learning, API, and dashboard components.

The canonical schema is intentionally different from the raw Olist source schema where necessary.

Raw source data must remain unchanged.

The transformation flow is:

Raw Olist CSV
→ Ingestion
→ Schema Validation
→ Business Validation
→ Referential Integrity Validation
→ Type Validation
→ Date Standardization
→ Monetary Standardization
→ Canonical Processed Data


## 2. MVP Canonical Datasets

The MVP contains five canonical datasets:

1. `customers`
2. `products`
3. `orders`
4. `order_items`
5. `order_payments`

Supporting Olist datasets such as sellers, reviews, geolocation, and category translation are not canonical MVP entities.

They may be incorporated in future phases when a clear business requirement exists.


## 3. Canonical Naming Conventions

Canonical naming follows these rules:

- Use lowercase names.
- Use `snake_case`.
- Use business-oriented names where the meaning is clear.
- Avoid source-specific prefixes where they do not add value.
- Preserve identifiers when they already represent the correct canonical concept.
- Use `_id` for identifiers.
- Use `_date` for business dates.
- Use `_at` for timestamps representing an event or point in time.
- Use explicit names for monetary values.
- Avoid ambiguous abbreviations.

Examples:

- `customer_id`
- `source_customer_id`
- `order_id`
- `order_date`
- `order_approved_at`
- `price_minor`
- `payment_value_minor`


## 4. Data Type Conventions

### 4.1 Identifiers

Identifiers are treated as strings.

Examples:

- `customer_id`
- `source_customer_id`
- `order_id`
- `product_id`
- `seller_id`
- `payment_id`

Identifiers must not be converted into numeric types even when they contain only digits.

### 4.2 Integer Values

Non-null integer fields use integer types.

Nullable integer fields must use a nullable integer representation such as pandas `Int64`.

Examples:

- `order_item_id`
- `payment_sequential`
- `payment_installments`
- `product_name_length`
- `product_description_length`
- `product_photos_qty`

### 4.3 Monetary Values

Monetary values use integer minor units.

For the Olist dataset:

- Currency: Brazilian Real (BRL)
- Minor unit: centavo
- `R$10.50` is stored as `1050`

Floating-point monetary values must not be used in canonical processed datasets.

### 4.4 Date and Timestamp Values

Timestamp fields are standardized to pandas `datetime64[ns]` during the MVP processing workflow.

Missing timestamps remain missing.

The system must never fabricate dates to fill missing source values.


## 5. Customers Dataset

### 5.1 Purpose

The `customers` dataset represents the canonical customer identity used by BizIntel AI.

Olist contains both an order-level customer identifier and a unique customer identifier.

BizIntel AI uses the unique customer identifier as the canonical customer identity.

### 5.2 Schema

| Canonical Column | Source Column | Data Type | Nullable | Description |
|---|---|---|---|---|
| `customer_id` | `customer_unique_id` | string | No | Canonical unique customer identifier |
| `source_customer_id` | `customer_id` | string | No | Original Olist order-level customer identifier |
| `customer_zip_code_prefix` | `customer_zip_code_prefix` | integer | No | Customer ZIP-code prefix |
| `customer_city` | `customer_city` | string | No | Customer city from source |
| `customer_state` | `customer_state` | string | No | Customer state from source |

### 5.3 Primary Key

`customer_id`

### 5.4 Foreign Keys

None.

### 5.5 Transformations

- Rename `customer_unique_id` to canonical `customer_id`.
- Rename original Olist `customer_id` to `source_customer_id`.
- Preserve geographic attributes as supplied by Olist.
- Do not fabricate missing customer attributes.

### 5.6 Source Limitation

The canonical customer entity is based on `customer_unique_id`.

The Olist `customer_id` represents an order-associated customer identifier and must not be treated as the canonical long-term customer identity.


## 6. Products Dataset

### 6.1 Purpose

The `products` dataset represents products referenced by order items.

### 6.2 Schema

| Canonical Column | Source Column | Data Type | Nullable | Description |
|---|---|---|---|---|
| `product_id` | `product_id` | string | No | Canonical product identifier |
| `product_category_name` | `product_category_name` | string | Yes | Product category in the source language |
| `product_name_length` | `product_name_lenght` | Int64 | Yes | Product-name character length |
| `product_description_length` | `product_description_lenght` | Int64 | Yes | Product-description character length |
| `product_photos_qty` | `product_photos_qty` | Int64 | Yes | Number of product photos |
| `product_weight_g` | `product_weight_g` | float64 | Yes | Product weight in grams |
| `product_length_cm` | `product_length_cm` | float64 | Yes | Product length in centimeters |
| `product_height_cm` | `product_height_cm` | float64 | Yes | Product height in centimeters |
| `product_width_cm` | `product_width_cm` | float64 | Yes | Product width in centimeters |

### 6.3 Primary Key

`product_id`

### 6.4 Foreign Keys

None.

### 6.5 Transformations

- Preserve `product_id`.
- Rename source misspellings such as `product_name_lenght` to `product_name_length`.
- Rename `product_description_lenght` to `product_description_length`.
- Preserve available product attributes.
- Missing category values remain missing.
- Missing physical attributes remain missing.
- No artificial values are inserted.

### 6.6 Source Limitations

The Olist product dataset does not provide reliable business attributes required for:

- product cost
- inventory/stock
- profit margin
- supplier cost
- product name
- current availability

These values must not be invented or inferred as factual source data.

The product category translation dataset is not part of the canonical MVP product schema.


## 7. Orders Dataset

### 7.1 Purpose

The `orders` dataset represents customer orders and their lifecycle.

### 7.2 Schema

| Canonical Column | Source Column | Data Type | Nullable | Description |
|---|---|---|---|---|
| `order_id` | `order_id` | string | No | Unique order identifier |
| `customer_id` | Derived through customer mapping | string | No | Canonical customer identifier |
| `order_status` | `order_status` | string | No | Current/source order status |
| `order_date` | `order_purchase_timestamp` | datetime64[ns] | No | Order purchase timestamp |
| `order_approved_at` | `order_approved_at` | datetime64[ns] | Yes | Order approval timestamp |
| `order_delivered_carrier_at` | `order_delivered_carrier_date` | datetime64[ns] | Yes | Date/time handed to carrier |
| `order_delivered_customer_at` | `order_delivered_customer_date` | datetime64[ns] | Yes | Date/time delivered to customer |
| `order_estimated_delivery_at` | `order_estimated_delivery_date` | datetime64[ns] | Yes | Estimated delivery timestamp |

### 7.3 Primary Key

`order_id`

### 7.4 Foreign Keys

`customer_id` → `customers.customer_id`

### 7.5 Customer ID Mapping

The raw Olist orders table contains:

`orders.customer_id`

The canonical customers table contains:

`customers.source_customer_id`

and:

`customers.customer_id`

Therefore the canonical order customer mapping is:

```text
orders.customer_id
        ↓
customers.source_customer_id
        ↓
customers.customer_id