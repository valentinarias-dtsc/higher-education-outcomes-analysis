"""
This module contains lists of column names that are used in the data processing and analysis of enrollment and offering data. 
"""

ENROLLMENT_REDUNDANT_METADATA_COLS = [
    "shift",
    "weekday",
    "schedule_time",
    "delivery_mode",
    "campus",
]


ENROLLMENT_METRIC_COMPONENT_COLS = [
    "dropout_count",
    "insufficient_count",
    "free_status_count",
    "promoted_completion_count",
    "regular_completion_count",
]


OFFERING_TEXT_COLS = [
    "shift",
    "weekday",
    "schedule_time",
    "delivery_mode",
]

