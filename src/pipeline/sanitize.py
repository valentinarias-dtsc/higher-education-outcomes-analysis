"""Deterministic pseudonymization utilities."""

from pathlib import Path

import pandas as pd


PRIVATE_MAPPINGS_DIR = Path("private/mappings")


MAPPING_SPECS = {
    "course_code": {
        "prefix": "CRS",
        "mapping_file": "course_mapping.csv",
    },
    "course_name": {
        "prefix": "COURSE",
        "mapping_file": "course_name_mapping.csv",
    },  
    "program_code": {
        "prefix": "PRG",
        "mapping_file": "program_mapping.csv",
    },
    "program_name": {
        "prefix": "PROGRAM",
        "mapping_file": "program_name_mapping.csv",
    },

    "campus": {
        "prefix": "CAMPUS",
        "mapping_file": "campus_mapping.csv",
    }
}


def build_deterministic_mapping(
    values: pd.Series,
    prefix: str,
) -> pd.DataFrame:
    unique_values = (
        values
        .dropna()
        .astype(str)
        .sort_values()
        .unique()
    )

    mapping_df = pd.DataFrame({
        "original_value": unique_values,
        "public_value": [
            f"{prefix}_{str(i + 1).zfill(3)}"
            for i in range(len(unique_values))
        ]
    })

    return mapping_df


def load_or_create_mapping(
    values: pd.Series,
    mapping_path: str | Path,
    prefix: str,
) -> pd.DataFrame:
    mapping_path = Path(mapping_path)

    if mapping_path.exists():
        return pd.read_csv(mapping_path)

    mapping_df = build_deterministic_mapping(values, prefix)

    mapping_path.parent.mkdir(parents=True, exist_ok=True)
    mapping_df.to_csv(mapping_path, index=False)

    return mapping_df


def apply_mapping(
    df: pd.DataFrame,
    source_column: str,
    mapping_df: pd.DataFrame,
) -> pd.DataFrame:
    df = df.copy()

    mapping = dict(
        zip(
            mapping_df["original_value"],
            mapping_df["public_value"]
        )
    )

    df[source_column] = df[source_column].map(mapping)

    return df


def sanitize_column(
    df: pd.DataFrame,
    column_name: str,
) -> pd.DataFrame:
    spec = MAPPING_SPECS[column_name]

    mapping_path = (
        PRIVATE_MAPPINGS_DIR
        / spec["mapping_file"]
    )

    mapping_df = load_or_create_mapping(
        values=df[column_name],
        mapping_path=mapping_path,
        prefix=spec["prefix"],
    )

    return apply_mapping(
        df=df,
        source_column=column_name,
        mapping_df=mapping_df,
    )


def sanitize_enrollment(df: pd.DataFrame) -> pd.DataFrame:
    df = sanitize_column(df, "course_code")
    df = sanitize_column(df, "program_code")

    return df



def sanitize_program_lookup(df: pd.DataFrame) -> pd.DataFrame:
    df = sanitize_column(df, "program_code")
    df = sanitize_column(df, "program_name")

    return df



def sanitize_offering(df: pd.DataFrame) -> pd.DataFrame:
    df = sanitize_column(df, "course_code")
    df = sanitize_column(df, "campus")

    return df