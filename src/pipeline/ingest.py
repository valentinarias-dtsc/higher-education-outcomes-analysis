"""Load raw private datasets."""

from pathlib import Path

from src.utils.io import read_excel_safe, read_csv_safe


def load_enrollment(path: str | Path):
    return read_excel_safe(path)


def load_offering(path: str | Path):
    return read_csv_safe(path)


def load_programs(path: str | Path):
    return read_csv_safe(path)