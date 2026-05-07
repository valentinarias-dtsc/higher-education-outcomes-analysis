"""Reusable input/output utilities."""

from pathlib import Path

import pandas as pd


def read_excel_safe(path: str | Path) -> pd.DataFrame | None:
    try:
        path = Path(path)
        if not path.exists():
            print(f"File not found: {path}")
            return None
        return pd.read_excel(path)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None
    

def read_csv_safe(path: str | Path) -> pd.DataFrame | None:
    try:
        path = Path(path)
        if not path.exists():
            print(f"File not found: {path}")
            return None
        return pd.read_csv(path)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None


def export_parquet(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(path, index=False)