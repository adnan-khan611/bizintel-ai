# Phase 4 — Analytics & KPI Plan

## 1. Purpose

Phase 4 transforms the validated canonical datasets into business-facing
analytics and Key Performance Indicators (KPIs).

The goal is to provide reliable, reproducible metrics that can later power
the BizIntel AI API, dashboard, forecasting, anomaly detection, and AI
business insights.

This phase will calculate metrics only from available canonical data.

No unavailable business attributes such as profit, cost, inventory, or
discounts will be fabricated.

---

## 2. Analytics Principles

The analytics layer must follow these principles:

- Use canonical processed datasets as the primary input.
- Keep business definitions explicit and documented.
- Keep calculations deterministic and reproducible.
- Separate metric calculation from API and UI logic.
- Use integer minor units for monetary calculations.
- Do not silently invent missing business information.
- Handle cancelled and unavailable orders according to documented rules.
- Add automated tests for every important metric.
- Keep raw data immutable.
- Make metric definitions understandable to business users.

---

## 3. Source Datasets

The MVP analytics layer will use:

- customers
- products
- orders
- order_items
- order_payments

Primary relationships:

```text
customers
    ↑
    |
orders
    ↑
    |
order_items → products

orders
    ↑
    |
order_payments