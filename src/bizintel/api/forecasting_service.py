"""Forecasting service layer for BizIntel AI."""

from pathlib import Path

from bizintel.api.analytics_data import load_analytics_datasets
from bizintel.api.forecasting_schemas import ForecastResponse
from bizintel.ml.dataset import build_monthly_revenue_dataset
from bizintel.ml.features import build_forecasting_features
from bizintel.ml.training import train_forecasting_model


def get_forecast(
    processed_data_dir: Path,
) -> ForecastResponse:
    """Build the forecasting dataset and generate the next-month forecast."""
    datasets = load_analytics_datasets(
        processed_data_dir
    )

    monthly_dataset = build_monthly_revenue_dataset(
        datasets["orders"],
        datasets["order_items"],
        include_partial_months=True,
        start_month="2016-10",
        end_month="2018-08",
    )

    forecasting_dataset = build_forecasting_features(
        monthly_dataset
    )

    complete_dataset = forecasting_dataset.dropna(
        subset=[
            column
            for column in forecasting_dataset.columns
            if column not in {"month", "revenue"}
        ]
        + ["revenue"]
    ).reset_index(drop=True)

    model = train_forecasting_model(
        monthly_dataset,
        min_training_rows=1,
    )

    latest_features = complete_dataset.iloc[[-1]]

    forecast_value = float(
        model.predict(
            latest_features.drop(
                columns=["month", "revenue"]
            )
        )[0]
    )

    last_month = latest_features["month"].iloc[0]
    forecast_month = last_month + 1

    return ForecastResponse(
        forecast_month=str(forecast_month),
        forecast_revenue=forecast_value,
    )