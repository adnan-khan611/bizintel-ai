import pandas as pd
import pytest

from bizintel.data.integrity import validate_foreign_key


def test_valid_foreign_key():
    """Test that valid child references pass."""
    parent = pd.DataFrame(
        {"customer_id": ["C001", "C002", "C003"]}
    )

    child = pd.DataFrame(
        {"customer_id": ["C001", "C002"]}
    )

    result = validate_foreign_key(
        child,
        "customer_id",
        parent,
        "customer_id",
    )

    assert result.is_valid is True
    assert result.missing_count == 0
    assert result.message == "Referential integrity check passed."


def test_missing_parent_reference():
    """Test that missing parent references are detected."""
    parent = pd.DataFrame(
        {"customer_id": ["C001", "C002"]}
    )

    child = pd.DataFrame(
        {"customer_id": ["C001", "C999"]}
    )

    result = validate_foreign_key(
        child,
        "customer_id",
        parent,
        "customer_id",
    )

    assert result.is_valid is False
    assert result.missing_count == 1
    assert "missing parent references" in result.message


def test_empty_child_table_passes():
    """Test that an empty child table passes."""
    parent = pd.DataFrame(
        {"customer_id": ["C001", "C002"]}
    )

    child = pd.DataFrame(
        {"customer_id": []}
    )

    result = validate_foreign_key(
        child,
        "customer_id",
        parent,
        "customer_id",
    )

    assert result.is_valid is True
    assert result.missing_count == 0


def test_missing_child_column_raises_error():
    """Test that a missing child column raises an error."""
    parent = pd.DataFrame(
        {"customer_id": ["C001"]}
    )

    child = pd.DataFrame(
        {"wrong_column": ["C001"]}
    )

    with pytest.raises(
        ValueError,
        match="Child column not found",
    ):
        validate_foreign_key(
            child,
            "customer_id",
            parent,
            "customer_id",
        )


def test_missing_parent_column_raises_error():
    """Test that a missing parent column raises an error."""
    parent = pd.DataFrame(
        {"wrong_column": ["C001"]}
    )

    child = pd.DataFrame(
        {"customer_id": ["C001"]}
    )

    with pytest.raises(
        ValueError,
        match="Parent column not found",
    ):
        validate_foreign_key(
            child,
            "customer_id",
            parent,
            "customer_id",
        )