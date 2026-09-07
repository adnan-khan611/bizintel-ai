from decimal import Decimal, InvalidOperation

import pandas as pd


def convert_to_minor_units(
    series: pd.Series,
) -> pd.Series:
    """Convert monetary values to integer minor units."""
    def convert_value(value: object) -> int:
        if pd.isna(value):
            return 0

        try:
            decimal_value = Decimal(str(value))
        except (InvalidOperation, ValueError):
            raise ValueError(
                f"Invalid monetary value: {value}"
            ) from None

        return int(
            (decimal_value * Decimal("100")).quantize(
                Decimal("1")
            )
        )

    return series.map(convert_value).astype("int64")