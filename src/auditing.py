"""
Reusable auditing utilities for schema validation and data quality checks.
"""

import pandas as pd

from src.config.contracts import FIELD_ROLES

from src.config.constants import (
    NULL_WARN_THRESHOLD,
    TOP_N_CATEGORIES,
    )


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

    if not mask.any():
        print(f"No duplicates found for subset: {', '.join(subset)}") 

        return pd.DataFrame(columns=df.columns)
    
    else: 
        print(f"Found {mask.sum()} duplicate rows for subset: {', '.join(subset)}")

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

    if duplicated > 0:
        print(f"Found {duplicated} duplicate rows for key: {', '.join(keys)}")
    else: 
        print(f"Key is unique: {', '.join(keys)}")
    
    return pku


def check_one_to_one_mapping(
    df: pd.DataFrame,
    key_col: str,
    value_col: str,
) -> pd.DataFrame:
    """
    Validate one-to-one consistency between two columns.
    """

    mapping_check = (
        df.groupby(key_col)[value_col]
        .nunique(dropna=True)
        .reset_index(name="unique_values")
    )

    inconsistent = (
        mapping_check
        .query("unique_values > 1")
        .sort_values("unique_values", ascending=False)
        .reset_index(drop=True)
    )

    if inconsistent.empty:
        print(
            f"No inconsistencies detected between "
            f"`{key_col}` and `{value_col}`."
        )
    else:
        print(
            f"{len(inconsistent)} `{key_col}` values are associated "
            f"with multiple `{value_col}` values."
        )

    return inconsistent


def profile_missingness(
    df: pd.DataFrame,
    warn_threshold: float = NULL_WARN_THRESHOLD,
) -> pd.DataFrame:
    """
    Profile missing values across dataframe columns.
    """

    missingness = pd.DataFrame({
        "column": df.columns,
        "null_count": [df[col].isna().sum() for col in df.columns],
        "null_pct": [df[col].isna().mean() * 100 for col in df.columns],
    })

    missingness["status"] = missingness["null_pct"].apply(
        lambda x:
            "critical" if x >= 50
            else "warning" if x >= warn_threshold * 100
            else "ok"
    )

    missingness = (
        missingness
        .sort_values("null_pct", ascending=False)
        .reset_index(drop=True)
    )

    critical_cols = (missingness["status"] == "critical").sum()
    warning_cols = (missingness["status"] == "warning").sum()

    print(
        f"{critical_cols} critical and "
        f"{warning_cols} warning-level columns detected."
    )

    return missingness


def profile_categoricals(
    df: pd.DataFrame,
    columns: list[str],
    top_n: int = TOP_N_CATEGORIES,
) -> dict:
    """
    Profile categorical distributions and cardinality.
    """

    profiles = {}

    for col in columns:

        value_counts = (
            df[col]
            .value_counts(dropna=False)
            .rename_axis(col)
            .reset_index(name="count")
        )

        value_counts["pct"] = (
            value_counts["count"] / len(df) * 100
        )

        profiles[col] = {
            "n_unique": df[col].nunique(dropna=True),
            "top_categories": value_counts.head(top_n),
        }

        print(
            f"`{col}` → "
            f"{df[col].nunique(dropna=True)} unique categories detected."
        )

    return profiles


def check_referential_integrity(
    left_df: pd.DataFrame,
    right_df: pd.DataFrame,
    keys: list[str],
) -> dict:
    """
    Assess referential integrity and merge coverage between two datasets.
    """

    left_keys = set(
        map(tuple, left_df[keys].drop_duplicates().values)
    )

    right_keys = set(
        map(tuple, right_df[keys].drop_duplicates().values)
    )

    matched = left_keys & right_keys

    left_only = left_keys - right_keys
    right_only = right_keys - left_keys

    coverage_pct = (
        len(matched) / len(left_keys) * 100
        if left_keys else 0
    )

    print(
        f"{len(matched)} matched keys | "
        f"{len(left_only)} unmatched left keys | "
        f"{len(right_only)} unmatched right keys"
    )

    results = {
        "matched_keys": len(matched),
        "left_only_keys": len(left_only),
        "right_only_keys": len(right_only),
        "coverage_pct": round(coverage_pct, 2),
        "left_only_samples": list(left_only)[:10],
        "right_only_samples": list(right_only)[:10],
    }

    return results


def validate_metric_consistency(
    df: pd.DataFrame,
    component_cols: list[str],
    total_col: str,
) -> pd.DataFrame:
    """
    Validate additive consistency between component metrics and a total column.
    """

    validation_df = df.copy()

    validation_df["computed_total"] = (
        validation_df[component_cols]
        .sum(axis=1)
    )

    validation_df["difference"] = (
        validation_df["computed_total"]
        - validation_df[total_col]
    )

    inconsistent_rows = (
        validation_df
        .loc[validation_df["difference"] != 0]
        .reset_index(drop=True)
    )

    if inconsistent_rows.empty:
        print(
            f"All rows satisfy metric consistency against `{total_col}`."
        )
    else:
        print(
            f"{len(inconsistent_rows)} inconsistent rows detected "
            f"against `{total_col}`."
        )

    return inconsistent_rows