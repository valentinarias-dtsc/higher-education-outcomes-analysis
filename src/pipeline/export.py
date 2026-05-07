"""Export public-ready datasets."""

from pathlib import Path

from src.utils.io import export_parquet


def export_dataset(df, output_path: str | Path):
    export_parquet(df, output_path)