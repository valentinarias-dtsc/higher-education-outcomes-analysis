"""Data utility functions."""

from pathlib import Path

import pandas as pd

from src.config.constants import SANITIZED_DATA_DIR

from src.utils.io import read_parquet_safe

def load_data(dataset: str) -> pd.DataFrame | None:
    """
    Load a dataset from the sanitized data directory.
        dataset: The name of the dataset to load (e.g., 'enrollment', 'programs', 'offering').
    """
    dataset = dataset.lower().strip()
    path = Path(SANITIZED_DATA_DIR) / f"{dataset}.parquet"
    return read_parquet_safe(path)

