"""Data utility functions."""

from pathlib import Path

import pandas as pd

from src.config.constants import (
    SANITIZED_DATA_DIR,
    PANDAS_DISPLAY_OPTIONS,
)

def load_data(dataset: str) -> pd.DataFrame:
    """
    Load a dataset from the sanitized data directory.
        dataset: The name of the dataset to load (e.g., 'enrollment', 'programs', 'offering').
    """
    dataset = dataset.lower().strip()
    path = Path(SANITIZED_DATA_DIR) / f"{dataset}.parquet"
    return pd.read_parquet(path)


def set_pandas_display_options():
    """Set pandas display options for consistent formatting across the pipeline."""
    for option, value in PANDAS_DISPLAY_OPTIONS.items():
        pd.set_option(option, value)