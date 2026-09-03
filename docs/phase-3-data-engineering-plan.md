# Phase 3 — Data Engineering & Data Layer Plan

## 1. Objective

Phase 3 establishes the reproducible data foundation for BizIntel AI.

The goal is to transform raw e-commerce business data into validated, cleaned,
and analysis-ready datasets that can later support analytics, machine learning,
forecasting, anomaly detection, and AI-powered business insights.

Phase 3 focuses on data engineering only.

ML, LLM/RAG, dashboard development, authentication, and production database
deployment are outside the initial implementation scope.

---

## 2. MVP Data Domains

The MVP uses five core entities:

1. customers
2. products
3. orders
4. order_items
5. payment_transactions

Logical relationship:

customers
    |
    | 1-to-many
    v
orders
    |
    | 1-to-many
    v
order_items
    |
    | many-to-one
    v
products

orders
    |
    | 1-to-many
    v
payment_transactions

---

## 3. Entity Contracts

### 3.1 Customers

| Field | Type | Required | Rules |
|---|---|---:|---|
| customer_id | string | Yes | Primary key, unique |
| signup_date | date | Yes | Valid date |
| location | string | No | Normalized text |
| customer_segment | string | No | Controlled category |

Privacy-sensitive information such as passwords, payment credentials,
full addresses, and unnecessary personal information must not be included.

Customer names and email addresses are not required for the MVP.

---

### 3.2 Products

| Field | Type | Required | Rules |
|---|---|---:|---|
| product_id | string | Yes | Primary key, unique |
| product_name | string | Yes | Non-empty |
| category | string | Yes | Non-empty |
| price | decimal | Yes | >= 0 |
| cost | decimal | Yes | >= 0 |
| stock_quantity | integer | Yes | >= 0 |

Business rule:

price and cost must use the same currency and monetary precision.

---

### 3.3 Orders

| Field | Type | Required | Rules |
|---|---|---:|---|
| order_id | string | Yes | Primary key, unique |
| customer_id | string | Yes | Foreign key to customers |
| order_date | datetime | Yes | Valid datetime |
| order_status | string | Yes | Controlled status |
| total_amount | decimal | Yes | >= 0 |

An order must reference an existing customer.

---

### 3.4 Order Items

| Field | Type | Required | Rules |
|---|---|---:|---|
| order_id | string | Yes | Foreign key to orders |
| product_id | string | Yes | Foreign key to products |
| quantity | integer | Yes | > 0 |
| unit_price | decimal | Yes | >= 0 |
| discount | decimal | Yes | >= 0 |

The MVP does not require a separate order_item_id.

The logical key is:

(order_id, product_id)

If the same product can legitimately appear multiple times in one order,
the implementation must introduce an order_item_id rather than silently
deduplicating the rows.

---

### 3.5 Payment Transactions

| Field | Type | Required | Rules |
|---|---|---:|---|
| payment_id | string | Yes | Primary key, unique |
| order_id | string | Yes | Foreign key to orders |
| payment_date | datetime | Yes | Valid datetime |
| payment_method | string | Yes | Controlled category |
| payment_status | string | Yes | Controlled status |
| amount | decimal | Yes | >= 0 |

Payment records must reference valid orders.

Payment credentials, card numbers, CVV values, bank credentials, and other
sensitive financial information must never be stored.

---

## 4. Relationships

### Customer → Orders

One customer may have zero or many orders.

Each order belongs to exactly one customer.

### Order → Order Items

One order may contain one or many order items.

Each order item belongs to exactly one order.

### Product → Order Items

One product may appear in zero or many order items.

Each order item references exactly one product.

### Order → Payment Transactions

An order may have one or multiple payment transactions.

This supports future handling of retries, refunds, or partial payments.

---

## 5. Data Storage Strategy

The MVP uses three logical data zones:

data/raw/
    Original source data.
    Must not be silently modified.

data/processed/
    Validated, cleaned, and transformed data.

data/sample/
    Small safe demonstration datasets suitable for GitHub/public use.

Raw data must be treated as immutable input.

Processed data must be reproducible from the raw data through the ingestion
and transformation pipeline.

---

## 6. Supported Input Formats

The MVP supports:

- CSV
- Excel (.xlsx)

The ingestion layer must detect the input format and convert the source into
a consistent internal tabular representation.

Source-specific logic should remain isolated from validation and
transformation logic.

---

## 7. Validation Rules

The validation layer must check:

### Schema validation

- Required columns exist.
- Unexpected columns are reported.
- Column types are compatible with the expected schema.

### Identifier validation

- Primary keys are present.
- Primary keys are unique.
- Foreign keys reference existing entities.

### Numeric validation

- Prices and costs cannot be negative.
- Quantity must be greater than zero.
- Stock quantity cannot be negative.
- Amounts cannot be negative.

### Date validation

- Dates must be parseable.
- Impossible dates must be rejected.
- Date fields must use a consistent format internally.

### Categorical validation

Statuses and payment methods must use controlled values.

Invalid categorical values must be reported rather than silently changed.

---

## 8. Missing Values

Missing values must be handled according to field importance.

Required identifiers and relationship fields:

- reject or quarantine invalid records.

Required business fields:

- report missing values.
- apply deterministic handling only when justified.

Optional fields:

- may remain null.

Missing values must never be replaced with arbitrary values merely to make
the dataset pass validation.

---

## 9. Duplicate Handling

Duplicates must be detected using entity-specific keys.

Examples:

customers:
    customer_id

products:
    product_id

orders:
    order_id

payment_transactions:
    payment_id

order_items:
    logical key defined by the final schema.

Duplicate records must be reported.

The pipeline must not silently delete records unless the duplicate handling
rule explicitly identifies them as exact duplicates.

---

## 10. Invalid Records

Invalid records should be identifiable and traceable.

The pipeline should distinguish between:

- valid records
- rejected records
- warnings

A validation failure should provide a useful reason, such as:

- missing required column
- duplicate primary key
- invalid date
- negative amount
- unknown foreign key
- invalid category

---

## 11. Date, Time and Currency Conventions

Internal processing should use consistent datetime representations.

Timezone assumptions must be documented.

The MVP should use one clearly documented business currency.

Currency must not be inferred from symbols alone.

Monetary calculations should use decimal-safe handling rather than relying on
binary floating-point arithmetic for financial totals.

---

## 12. Reproducibility

The same raw input and configuration should produce the same processed output.

The pipeline should:

- avoid random transformations unless explicitly seeded
- document transformation rules
- preserve source files
- provide deterministic output
- record validation results
- avoid environment-specific hidden assumptions

---

## 13. Data Quality Acceptance Criteria

A dataset is considered valid for downstream analytics when:

1. Required entities are present.
2. Required columns exist.
3. Primary keys satisfy uniqueness requirements.
4. Foreign-key relationships are valid.
5. Required numeric fields satisfy business constraints.
6. Dates are valid and parseable.
7. Invalid records are identified.
8. Missing required values are identified.
9. Processing is reproducible.
10. No sensitive credentials or unnecessary PII are included.

---

## 14. Privacy and Public Demo Data

The public GitHub repository must contain only safe demonstration data.

Do not commit:

- passwords
- API keys
- access tokens
- payment credentials
- card numbers
- CVV
- bank credentials
- unnecessary personally identifiable information
- confidential business data

`.env` files and secrets must remain outside version control.

---

## 15. Directory Structure

The Phase 3 data layer will use:

data/
├── raw/
├── processed/
└── sample/

Potential future structure:

src/bizintel/
├── data/
│   ├── ingestion/
│   ├── validation/
│   └── transformation/

The exact Python module structure will be finalized immediately before
implementation.

---

## 16. Phase 3 Implementation Order

Implementation must follow this order:

### Step 1

Finalize this data engineering contract.

### Step 2

Select a reproducible e-commerce dataset/source.

### Step 3

Define the exact source-to-target mapping.

### Step 4

Create safe sample/raw input data.

### Step 5

Implement ingestion for CSV and Excel.

### Step 6

Implement schema and data-quality validation.

### Step 7

Implement deterministic cleaning and transformation.

### Step 8

Generate processed/curated datasets.

### Step 9

Add automated tests for ingestion, validation, and transformation.

### Step 10

Run full verification.

### Step 11

Commit the completed Phase 3 data-layer increment.

Only after these steps should downstream analytics and ML implementation begin.

---

## 17. Explicitly Out of Scope

The following are not part of the initial Phase 3 implementation:

- PostgreSQL production deployment
- authentication
- multi-user access
- React/Next.js dashboard
- machine learning models
- sales forecasting
- anomaly detection models
- LLM integration
- RAG
- production cloud deployment
- Docker deployment
- CI/CD implementation
- automated business alerts

These will be added in later phases after the data foundation is stable.

---

## 18. Open Decisions

Before implementation, the following must be explicitly finalized:

1. Exact public/synthetic dataset source.
2. Exact source column names and mappings.
3. Final allowed values for order_status.
4. Final allowed values for payment_status.
5. Final allowed payment_method values.
6. Business currency.
7. Timezone convention.
8. Whether the source dataset contains all five entities or requires
   deterministic generation of missing entities.
9. Exact order_items uniqueness strategy if repeated products occur in an order.

No implementation should silently invent answers to these decisions.

---

## 19. Definition of Done

Phase 3 data engineering is complete only when:

- raw input can be ingested reproducibly
- schema validation works
- data-quality errors are reported clearly
- transformations are deterministic
- processed data is generated successfully
- automated tests cover the important behavior
- no secrets or unsafe PII are committed
- Ruff passes
- Pytest passes
- git diff --check passes
- the implementation is documented
- changes are committed and pushed to GitHub

Development principle:

Build → Test → Verify → Commit → Next