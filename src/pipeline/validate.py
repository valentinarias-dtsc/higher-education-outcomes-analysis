"""Validation checks for public datasets."""

import pandas as pd


def validate_row_count(raw_df: pd.DataFrame, public_df: pd.DataFrame) -> None:
    assert len(raw_df) == len(public_df), (
        "Row count mismatch between raw and public datasets."
    )


def validate_unique_keys(
    df: pd.DataFrame,
    key_columns: list[str],
) -> None:
    duplicated = df.duplicated(subset=key_columns)

    assert not duplicated.any(), (
        f"Duplicate keys detected for: {key_columns}"
    )