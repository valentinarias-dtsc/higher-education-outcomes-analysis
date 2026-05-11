"""
Reusable auditing utilities for schema validation and data quality checks.
"""

import pandas as pd

from src.config.contracts import FIELD_ROLES


def inspect_schema(
    df: pd.DataFrame,
    expected_schema: dict,
    field_roles: dict = FIELD_ROLES,
) -> pd.DataFrame:
    """
    Compare observed dataframe schema against expected contract.
    """

    audit = pd.DataFrame({
        "column": df.columns,
        "observed_dtype": [str(df[col].dtype) for col in df.columns],
        "expected_dtype": [expected_schema.get(col) for col in df.columns],
        "non_null_count": [df[col].notna().sum() for col in df.columns],
        "null_pct": [df[col].isna().mean() * 100 for col in df.columns],
        "n_unique": [df[col].nunique(dropna=True) for col in df.columns],
    })

    audit["dtype_match"] = (
        audit["observed_dtype"] == audit["expected_dtype"]
    )

    audit["field_role"] = audit["column"].map(field_roles)

    cols = [
        "column",
        "field_role",
        "observed_dtype",
        "expected_dtype",
        "dtype_match",
        "non_null_count",
        "null_pct",
        "n_unique",
    ]

    cols = [c for c in cols if c in audit.columns]

    return audit[cols].sort_values(
        by=["null_pct", "n_unique"],
        ascending=[False, False],
    ).reset_index(drop=True)


def check_duplicates(
    df: pd.DataFrame,
    subset: list[str],
) -> pd.DataFrame:
    """
    Return duplicated rows based on subset columns.
    """

    mask = df.duplicated(subset=subset, keep=False)
    return df.loc[mask].sort_values(subset)


def check_key_uniqueness(
    df: pd.DataFrame,
    keys: list[str],
) -> pd.DataFrame:
    """
    Validate uniqueness of a candidate key.
    """

    duplicated = df.duplicated(subset=keys).sum()

    pku = pd.DataFrame({
        "key_columns": [", ".join(keys)],
        "rows": [len(df)],
        "unique_keys": [df[keys].drop_duplicates().shape[0]],
        "duplicate_rows": [int(duplicated)],
        "is_unique": [duplicated == 0],
    })
    
    return pku