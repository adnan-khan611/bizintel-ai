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
- `order_id`
- `product_id`
- `seller_id`
- `payment_id`

Identifiers must not be converted into numeric types even when they contain only digits.

### 4.2 Integer Values

Non-null integer fields use integer types.

Nullable integer fields use a nullable integer representation such as pandas `Int64`.

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

The Olist source contains both:

- `customer_id` — an order-associated customer identifier
- `customer_unique_id` — the identifier representing the same real customer across orders

BizIntel AI uses `customer_unique_id` as the canonical customer identity.

Therefore, the canonical customers dataset contains one row per unique `customer_unique_id`.

The raw Olist `customer_id` is not stored as a column in the canonical customers entity because multiple source customer IDs can belong to the same canonical customer.


### 5.2 Schema

| Canonical Column | Source Column | Data Type | Nullable | Description |
|---|---|---|---|---|
| `customer_id` | `customer_unique_id` | string | No | Canonical unique customer identifier |
| `customer_zip_code_prefix` | `customer_zip_code_prefix` | integer | No | Customer ZIP-code prefix |
| `customer_city` | `customer_city` | string | No | Customer city from source |
| `customer_state` | `customer_state` | string | No | Customer state from source |

### 5.3 Primary Key

`customer_id`

`customer_id` must be unique in the canonical customers dataset.

### 5.4 Foreign Keys

None.

### 5.5 Transformations

- Use `customer_unique_id` as canonical `customer_id`.
- Deduplicate the source customer records by `customer_unique_id`.
- Produce exactly one canonical customer row for each unique `customer_unique_id`.
- Preserve customer geographic attributes from the source.
- Do not fabricate missing customer attributes.
- The canonical transformation must be deterministic.
- When duplicate source records for the same `customer_unique_id` contain conflicting geographic attributes, retain the first source record according to the original source row order.
- Conflicting geographic attributes are treated as a source-data limitation and are not resolved through inference.

### 5.6 Source Customer ID Mapping

The raw Olist `customer_id` is required to map orders to canonical customers.

The mapping concept is:

```text
olist_customers.customer_id
        ↓
olist_customers.customer_unique_id
        ↓
canonical customers.customer_id