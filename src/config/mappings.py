"""Column mappings and categorical normalization maps."""

ENROLLMENT_COLUMN_MAP = {
    "MATERIA": "course_name",
    "COMISION": "section",
    "CODIGO": "course_code",
    "CARRERA": "program_code",
    "TOTAL_ALUMNOS": "total_enrollment",
    "ABANDONO": "dropout_count",
    "LIBRE": "free_status_count",
    "REGULAR": "regular_completion_count",
    "PROMOCIONO": "promoted_completion_count",
    "TURNO": "shift",
    "DIA": "weekday",
    "HORA": "schedule_time",
    "MODALIDAD": "delivery_mode",
    "SEDE": "campus",
}

PROGRAM_COLUMN_MAP = {
    "Cod_Carrera": "program_code",
    "Carrera": "program_name",
}

OFFERING_COLUMN_MAP = {
    "COD. ASIG": "course_code",
    "COMISIÓN": "section",
    "CARGA HORARIA": "workload",
    "TURNO": "shift",
    "DIA": "weekday",
    "HORA": "schedule_time",
    "MODALIDAD": "delivery_mode",
    "SEDE": "campus",
}

SHIFT_MAP = {
    "mañana": "morning",
    "tarde": "afternoon",
    "noche": "night",
}

DELIVERY_MODE_MAP = {
    "presencial": "in_person",
    "virtual": "online",
    "híbrida": "hybrid",
}