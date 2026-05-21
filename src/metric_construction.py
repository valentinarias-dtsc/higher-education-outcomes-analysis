"""
Reusable metric construction utilities.
"""

import pandas as pd


def add_component_rates(
    df: pd.DataFrame,
    component_features: list[str],
    total_feature: str,
    new_column_names: list[str] | None = None,
    suffix: str = "_rate",
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Add rate columns from component features divided by a total feature.
    """

    df = df.copy()

    if new_column_names is None:
        new_column_names = [
            f"{feature}{suffix}"
            for feature in component_features
        ]

    if len(new_column_names) != len(component_features):
        raise ValueError(
            "`new_column_names` must have the same length as "
            "`component_features`."
        )

    required_columns = component_features + [total_feature]
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise KeyError(
            f"Columns not found in dataframe: {missing_columns}"
        )

    for component_feature, new_column_name in zip(
        component_features,
        new_column_names,
    ):
        df[new_column_name] = (
            df[component_feature]
            / df[total_feature]
        )

    if verbose:
        print(
            f"Rate columns created against `{total_feature}`: "
            f"{new_column_names}"
        )

    return df


def add_columns_sum(
    df: pd.DataFrame,
    columns_to_sum: list[str],
    new_column_name: str,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Add a new column from the row-wise sum of two or more columns.
    """

    df = df.copy()

    if len(columns_to_sum) < 2:
        raise ValueError(
            "`columns_to_sum` must contain two or more columns."
        )

    missing_columns = [
        column
        for column in columns_to_sum
        if column not in df.columns
    ]

    if missing_columns:
        raise KeyError(
            f"Columns not found in dataframe: {missing_columns}"
        )

    df[new_column_name] = (
        df[columns_to_sum]
        .sum(axis=1)
    )

    if verbose:
        print(
            f"Column `{new_column_name}` created from: "
            f"{columns_to_sum}"
        )

    return df
