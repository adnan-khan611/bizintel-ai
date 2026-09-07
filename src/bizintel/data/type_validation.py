from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class TypeValidationResult:
    """Represent the result of a data type validation check."""

    is_valid: bool
    errors: tuple[str, ...]


def validate_column_types(
    dataframe: pd.DataFrame,
    expected_types: dict[str, str],
) -> TypeValidationResult:
    """Validate DataFrame columns against expected pandas dtypes."""
    errors: list[str] = []

    for column, expected_type in expected_types.items():
        if column not in dataframe.columns:
            errors.append(
                f"Column not found: {column}"
            )
            continue

        actual_type = str(dataframe[column].dtype)

        if expected_type == "string":
            if actual_type not in {"object", "string"}:
                errors.append(
                    f"Column '{column}' has type "
                    f"{actual_type}, expected string."
                )

        elif expected_type == "integer":
            if not pd.api.types.is_integer_dtype(
                dataframe[column]
            ):
                errors.append(
                    f"Column '{column}' has type "
                    f"{actual_type}, expected integer."
                )

        elif expected_type == "float":
            if not pd.api.types.is_float_dtype(
                dataframe[column]
            ):
                errors.append(
                    f"Column '{column}' has type "
                    f"{actual_type}, expected float."
                )

        elif expected_type == "datetime":
            if not pd.api.types.is_datetime64_any_dtype(
                dataframe[column]
            ):
                errors.append(
                    f"Column '{column}' has type "
                    f"{actual_type}, expected datetime."
                )

        else:
            raise ValueError(
                f"Unsupported expected type: {expected_type}"
            )

    return TypeValidationResult(
        is_valid=not errors,
        errors=tuple(errors),
    )