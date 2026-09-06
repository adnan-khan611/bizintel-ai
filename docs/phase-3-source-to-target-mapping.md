# Phase 3 — Source-to-Target Mapping & Ingestion Contract

## 1. Purpose

This document defines how source data from the Olist Brazilian E-Commerce Public Dataset maps to the BizIntel AI canonical data model.

The mapping is designed to:

- preserve source data meaning
- avoid fabricated business facts
- make transformations explicit
- define validation rules before ingestion
- document known source limitations
- provide a stable contract for the ingestion layer

The ingestion implementation must follow this document.

---

## 2. Source Dataset

Primary source:

Olist Brazilian E-Commerce Public Dataset.

Source files used for the MVP:

1. `olist_customers_dataset.csv`
2. `olist_orders_dataset.csv`
3. `olist_order_items_dataset.csv`
4. `olist_order_payments_dataset.csv`
5. `olist_products_dataset.csv`

Supporting/enrichment files:

6. `olist_sellers_dataset.csv`
7. `olist_order_reviews_dataset.csv`
8. `olist_geolocation_dataset.csv`
9. `product_category_name_translation.csv`

Raw source files are stored locally under:

```text
data/raw/