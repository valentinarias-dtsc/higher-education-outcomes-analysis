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


SUM_COLS = {
    "completion_count": ["promoted_completion_count", "regular_completion_count"],
    "attrition_count": ["dropout_count", "free_status_count"],
    "adverse_outcomes_count": ["dropout_count", "insufficient_count", "free_status_count"]
}


METRIC_COMPONENT_COLS = [
    "dropout_count",
    "insufficient_count",
    "free_status_count",
    "promoted_completion_count",
    "regular_completion_count",
    "completion_count",
    "attrition_count",
    "adverse_outcomes_count",
]


NEW_RATE_METRIC_COLS = [
    "dropout_rate",
    "insufficient_rate",
    "free_status_rate",
    "promoted_completion_rate",
    "regular_completion_rate",
    "completion_rate",
    "attrition_rate",
    "adverse_outcomes_rate",
]