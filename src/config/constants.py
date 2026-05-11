"""Global constants used across the pipeline."""

# Academic period for which the data is being processed.
ACADEMIC_PERIOD = "2024_C1"

# Directory paths for raw and sanitized data, as well as mappings.
SANITIZED_DATA_DIR = "data/sanitized"
RAW_DATA_DIR = "data/raw"
MAPPINGS_DIR = "private/mappings"

# Random seed for reproducibility in any operations that require randomness.
RANDOM_SEED = 42

# Thresholds for data quality checks.
NULL_WARN_THRESHOLD = 0.05
HIGH_CARDINALITY_THRESHOLD = 50
TOP_N_CATEGORIES = 10

# Tolerance level for metric comparisons in tests.
METRIC_TOLERANCE = 0 

# Display options for pandas DataFrames to ensure consistent formatting across the pipeline.
PANDAS_DISPLAY_OPTIONS = {
    "display.max_columns": 50,
    "display.max_rows": 200,
    "display.width": 140,
    "display.float_format": "{:.2f}".format,
    "display.max_colwidth": 80,
}