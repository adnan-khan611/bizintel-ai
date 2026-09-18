"""Analytics service layer for BizIntel AI."""

from pathlib import Path
from typing import Any

import pandas as pd

from bizintel.analytics.summary import build_analytics_summary
from bizintel.api.analytics_data import load_analytics_datasets


def _series_to_dict(series: pd.Series) -> dict[str, Any]:
    """Convert a pandas Series into a JSON-compatible dictionary."""
    return {
        str(key): value.item()
        if hasattr(value, "item")
        else value
        for key, value in series.items()
    }


def _serialize_analytics_summary(
    summary: dict[str, Any],
) -> dict[str, Any]:
    """Convert analytics results into JSON-compatible Python types."""
    serialized_summary = dict(summary)

    for section_name, section in serialized_summary.items():
        if not isinstance(section, dict):
            continue

        serialized_section = dict(section)

        for key, value in serialized_section.items():
            if isinstance(value, pd.Series):
                serialized_section[key] = _series_to_dict(value)

        serialized_summary[section_name] = serialized_section

    return serialized_summary


def get_analytics_summary(
    processed_data_dir: Path,
) -> dict[str, Any]:
    """Load canonical datasets and build the analytics summary."""
    datasets = load_analytics_datasets(
        processed_data_dir
    )

    summary = build_analytics_summary(
        customers=datasets["customers"],
        orders=datasets["orders"],
        products=datasets["products"],
        order_items=datasets["order_items"],
        order_payments=datasets["order_payments"],
    )

    return _serialize_analytics_summary(summary)