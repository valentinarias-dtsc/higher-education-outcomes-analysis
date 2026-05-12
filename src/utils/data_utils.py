"""Data utility functions."""

from pathlib import Path

import pandas as pd

from src.config.constants import SANITIZED_DATA_DIR

def load_data(dataset: str) -> pd.DataFrame:
    """
    Load a dataset from the sanitized data directory.
        dataset: The name of the dataset to load (e.g., 'enrollment', 'programs', 'offering').
    """
    dataset = dataset.lower().strip()
    path = Path(SANITIZED_DATA_DIR) / f"{dataset}.parquet"
    return pd.read_parquet(path)

