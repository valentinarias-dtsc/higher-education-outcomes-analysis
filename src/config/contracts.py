"""
Analytical data contracts for schema validation, relational integrity,
and field-level semantic classification.
"""

# ==================================================
# Expected schemas
# ==================================================

ENROLLMENT_SCHEMA = {
    "course_name": "str",
    "section": "int64",
    "total_enrollment": "int64",
    "dropout_count": "int64",
    "insufficient_count": "int64",
    "free_status_count": "int64",
    "promoted_completion_count": "int64",
    "regular_completion_count": "int64",
    "course_code": "str",
    "program_code": "str",
    "shift": "str",
    "weekday": "str",
    "schedule_time": "str",
    "delivery_mode": "str",
    "campus": "str",
}

OFFERING_SCHEMA = {
    "course_code": "str",
    "section": "int64",
    "workload": "int64",
    "schedule_time": "str",
    "shift": "str",
    "weekday": "str",
    "delivery_mode": "str",
    "campus": "str",
}

PROGRAMS_SCHEMA = {
    "program_code": "str",
    "program_name": "str",
}


# ==================================================
# Primary keys
# ==================================================

PRIMARY_KEYS = {
    "enrollment": ["course_code", "section"],
    "offering": ["course_code", "section"],
    "programs": ["program_code"],
}


# ==================================================
# Field semantic roles
# ==================================================

FIELD_ROLES = {
    "course_code": "identifier",
    "course_name": "descriptor",
    "section": "identifier",
    "program_code": "foreign_key",
    "program_name": "descriptor",
    "total_enrollment": "metric",
    "dropout_count": "metric",
    "insufficient_count": "metric",
    "free_status_count": "metric",
    "promoted_completion_count": "metric",
    "regular_completion_count": "metric",
    "workload": "metric",
    "schedule_time": "categorical",
    "shift": "categorical",
    "weekday": "categorical",
    "delivery_mode": "categorical",
    "campus": "categorical",
}