"""Data utility functions."""

from pathlib import Path

import pandas as pd

from src.config.constants import (
    SANITIZED_DATA_DIR,
    CLEAN_DATA_DIR,
    PROCESSED_DATA_DIR,
    DEMO_DATA_DIR,
    PANDAS_DISPLAY_OPTIONS,
)

def set_pandas_display_options():
    """Set pandas display options for consistent formatting across the pipeline."""
    for option, value in PANDAS_DISPLAY_OPTIONS.items():
        pd.set_option(option, value)


def load_data(
        stage: str = "sanitized", 
        dataset: str | None = None,
) -> pd.DataFrame:
    """
    Load a dataset from the specified data directory.
        stage: The stage of the data pipeline (e.g., 'sanitized', 'clean', 'processed', 'demo').
        dataset: Only applicable for 'sanitized' stage. The name of the dataset to load (e.g., 'enrollment', 'programs', 'offering').
    """
    if stage.lower().strip() not in ['sanitized', 'clean', 'processed', 'demo']:
        raise ValueError(f"Invalid stage: {stage}. Must be one of 'sanitized', 'clean', 'processed', 'demo'.")
    
    elif stage.lower().strip() == "sanitized" and not dataset:
        raise ValueError("Dataset name must be provided when stage is 'sanitized'.")
    
    elif stage.lower().strip() == "sanitized" and str(dataset).lower().strip() not in ['enrollment', 'programs', 'offering']:
        raise ValueError(f"Invalid dataset: {dataset}. Must be one of 'enrollment', 'programs', 'offering'.")
    
    elif stage.lower().strip() == "sanitized" and dataset is not None:
        dataset = dataset.lower().strip()
        path = Path(SANITIZED_DATA_DIR) / f"{dataset}.parquet"
        return pd.read_parquet(path)
    
    elif stage.lower().strip() == "clean":
        path = Path(CLEAN_DATA_DIR) / "analytical_base.parquet"
        return pd.read_parquet(path)

    elif stage.lower().strip() == "processed":
        path = Path(PROCESSED_DATA_DIR) / "processed_data.parquet"
        return pd.read_parquet(path)
    
    else:
        path = Path(DEMO_DATA_DIR) / "demo_data.parquet"
        return pd.read_parquet(path)