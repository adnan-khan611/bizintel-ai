# Phase 5 — Machine Learning Plan

## 1. Objective

The objective of Phase 5 is to add a production-oriented machine learning forecasting capability to BizIntel AI.

The first ML feature will be **sales/revenue forecasting**.

The system will use historical business transactions to forecast future merchandise revenue while preventing data leakage and maintaining a proper time-based evaluation strategy.

The goal is not simply to train a model, but to build a reliable ML pipeline that can later be integrated into the BizIntel AI business dashboard.

---

## 2. Business Problem

Small and medium-sized e-commerce businesses need to understand how their future sales may perform.

BizIntel AI should help answer questions such as:

- What revenue can the business expect next month?
- Is revenue expected to increase or decrease?
- How accurate is the forecasting model?
- Is the model performing better than a simple baseline?
- Can the forecast be generated consistently from the latest available business data?

The forecasting system should provide a measurable prediction rather than an unsupported business assumption.

---

## 3. Prediction Target

The first forecasting target will be:

**Monthly Merchandise Revenue**

Merchandise revenue is defined as the sum of `price_minor` from canonical order items.

```text
Monthly Merchandise Revenue
= SUM(order_items.price_minor)