"""
Data cleaning functions for the higher education outcomes analysis.
"""

import pandas as pd

import numpy as np

from src.utils.text import normalize_text

def normalize_text_columns(
        df: pd.DataFrame, 
        text_cols: list | str,
        normalize_text = normalize_text,
    ) -> pd.DataFrame:
    """Normalize text columns in the dataframe using the provided normalization function."""

    df = df.copy()

    if isinstance(text_cols, str):
        text_cols = [text_cols]

    df[text_cols] = df[text_cols].map(normalize_text)

    return df


def drop_columns(
        df: pd.DataFrame, 
        cols_to_drop: list[str] = [],
        verbose: bool = True,
    ) -> pd.DataFrame:
    """Drop columns from the dataframe."""

    df = df.copy()

    try:
        df = df.drop(columns=cols_to_drop)

    except KeyError as e:
        print(f"Error dropping columns: {e}")
        print(f"Available columns: {df.columns.tolist()}")
        
        raise e
    
    if verbose:
        print(f"Columns succesfully dropped: {list(cols_to_drop)}")

    return df


def normalize_categorical_values(
    df: pd.DataFrame,
    column: str,
    category_map: dict[str, list[str]],
    unmapped: str = "ignore",
    normalize_func = None,
) -> pd.DataFrame:
    """
    Normalize categorical values into canonical categories.
    """

    df = df.copy()

    if normalize_func is not None:
        series = df[column].map(normalize_func)
    else:
        series = df[column].astype("string")

    reverse_map = {}

    for canonical, aliases in category_map.items():
        reverse_map[canonical.lower()] = canonical

        for alias in aliases:
            reverse_map[alias.lower()] = canonical

    normalized = series.map(reverse_map)

    if unmapped == "ignore":
        normalized = normalized.fillna(series)

    elif unmapped == "raise":
        unknown = series[normalized.isna()].dropna().unique()

        if len(unknown) > 0:
            raise ValueError(
                f"Unmapped categories detected: {unknown}"
            )
    elif unmapped == "nan":
        pass
    

    df[column] = normalized

    return df

def correct_typo_variants(
    df: pd.DataFrame,
    column: str,
    typo_map: dict[str, list[str]],
    unmapped: str = "ignore",
    verbose: bool = True,
    normalize_func = None,
) -> pd.DataFrame:
    """
    Correct common typos in categorical values.
    """
    if verbose:
        print(f"Column: '{column}'")
        print(f"Number of unique categories before typo correction: {df[column].nunique(dropna=False)}")
    results = normalize_categorical_values(
            df=df,
            column=column,
            category_map=typo_map,
            unmapped=unmapped,
            normalize_func=normalize_func,
    )
    if verbose:
        print(f"Number of unique categories after typo correction: {results[column].nunique(dropna=False)}")
        print(f"{results[column].unique()}")
    return results


def apply_canonical_taxonomy(
    df: pd.DataFrame,
    column: str,
    canonical_map: dict[str, str],
    verbose: bool = True,
) -> pd.DataFrame:
    """
    Map categorical values to a canonical taxonomy.
    """
    df = df.copy()

    df[column] = df[column].astype("string")

    df[column] = df[column].map(canonical_map)

    if verbose:
        print(f"Column: '{column}'")
        print(f"Unique categories after applying canonical taxonomy: {df[column].unique()}")
    return df


def reconcile_metric_totals(
    df: pd.DataFrame,
    component_columns: list[str],
    reported_column: str,
    tolerance: int = 2,
    overwrite: bool = False,
) -> pd.DataFrame:
    """
    Reconcile reported aggregate metrics against totals computed
    from component columns.
    """

    df = df.copy()

    reported_backup_col = f"reported_{reported_column}"
    computed_col = f"computed_{reported_column}"
    difference_col = f"{reported_column}_difference"
    reconciled_col = f"reconciled_{reported_column}"

    # Preserve original reported values
    df[reported_backup_col] = df[reported_column]

    # Compute aggregate from components
    df[computed_col] = (
        df[component_columns]
        .sum(axis=1)
    )

    # Compute discrepancy
    df[difference_col] = (
        df[reported_backup_col]
        - df[computed_col]
    )

    # Determine rows eligible for reconciliation
    reconciliation_mask = (
        df[difference_col]
        .abs()
        <= tolerance
    )

    # Build reconciled metric
    df[reconciled_col] = np.where(
        reconciliation_mask,
        df[computed_col],
        df[reported_backup_col],
    )

    # Optional overwrite
    if overwrite:
        df[reported_column] = df[reconciled_col]

    return df