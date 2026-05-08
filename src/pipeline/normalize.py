"""Structural normalization logic."""

import pandas as pd

from src.config.mappings import (
    ENROLLMENT_COLUMN_MAP,
    OFFERING_COLUMN_MAP,
    PROGRAM_COLUMN_MAP,
)
from src.utils.text import normalize_text


def normalize_column_names(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    df = df.copy()
    df.columns = [column.strip() for column in df.columns]

    return df.rename(columns=mapping)


def normalize_enrollment(df: pd.DataFrame) -> pd.DataFrame:
    return normalize_column_names(df, ENROLLMENT_COLUMN_MAP)


def normalize_program_lookup(df: pd.DataFrame) -> pd.DataFrame:
    return normalize_column_names(df, PROGRAM_COLUMN_MAP)


def normalize_offering(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_column_names(df, OFFERING_COLUMN_MAP)
    return df