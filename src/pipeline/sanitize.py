"""Deterministic pseudonymization utilities."""

from pathlib import Path

import pandas as pd

from src.config.constants import (
        MAPPINGS_DIR,
)

PRIVATE_MAPPINGS_DIR = Path(MAPPINGS_DIR)


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
    "campus": {
        "prefix": "CAMPUS",
        "mapping_file": "campus_mapping.csv",
    }
}


def public_program_name(
        df: pd.DataFrame,
        public_code: pd.Series,
        program_name_column: str = "program_name",
        ):
    df = df.copy()

    public_code = public_code.astype(str)
    unique_codes = (
        pd.Series(public_code.dropna().unique())
        .sort_values()
        .reset_index(drop=True)
    )

    def _excel_style_label(index: int) -> str:
        label = ""
        while index >= 0:
            label = chr(ord("A") + (index % 26)) + label
            index = index // 26 - 1
        return label

    mapping = {
        code: f"Program {_excel_style_label(idx)}"
        for idx, code in enumerate(unique_codes)
    }

    df[program_name_column] = public_code.map(mapping)
    return df


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

    incoming_values = set(
        values.dropna().astype(str).unique()
    )

    if mapping_path.exists():
        mapping_df = pd.read_csv(mapping_path)

        existing_values = set(
            mapping_df["original_value"].astype(str)
        )

        unseen_values = sorted(
            incoming_values - existing_values
        )

        if unseen_values:
            current_n = len(mapping_df)

            new_rows = pd.DataFrame({
                "original_value": unseen_values,
                "public_value": [
                    f"{prefix}_{str(i).zfill(3)}"
                    for i in range(current_n + 1, current_n + len(unseen_values) + 1)
                ]
            })

            mapping_df = pd.concat(
                [mapping_df, new_rows],
                ignore_index=True,
            )

            assert mapping_df["original_value"].is_unique
            assert mapping_df["public_value"].is_unique

            mapping_df.to_csv(mapping_path, index=False)

        return mapping_df

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



def sanitize_programs(df: pd.DataFrame) -> pd.DataFrame:
    df = sanitize_column(df, "program_code")
    df = public_program_name(df, df["program_code"])

    return df



def sanitize_offering(df: pd.DataFrame) -> pd.DataFrame:
    df = sanitize_column(df, "course_code")
    df = sanitize_column(df, "campus")

    return df