"""Column mappings and categorical normalization maps."""

ENROLLMENT_COLUMN_MAP = {
    "MATERIA": "course_name",
    "COMISION": "section",
    "CODIGO": "course_code",
    "CARRERA": "program_code",
    "TOTAL_ALUMNOS": "total_enrollment",
    "INSUFICIENTE": "insufficient_count",
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
    "cod_carrera": "program_code",
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

SHIFT_CANONICAL_MAP = {
    "manana": "morning",
    "tarde": "afternoon",
    "noche": "night",
}

DELIVERY_MODE_CANONICAL_MAP = {
    "presencial": "on_site",
    "virtual": "online",
    "hibrida": "hybrid",
}

WEEKDAY_CANONICAL_MAP = {
    "lunes": "monday",
    "martes": "tuesday",
    "miercoles": "wednesday",
    "jueves": "thursday",
    "viernes": "friday",
    "sabado": "saturday",
}

CANONICAL_MAPPINGS = {
    "shift": SHIFT_CANONICAL_MAP,
    "delivery_mode": DELIVERY_MODE_CANONICAL_MAP,
    "weekday": WEEKDAY_CANONICAL_MAP,
}

SHIFT_TYPO_MAP = {
    "manana": ["manana", "mañana", "manama"],
    "tarde": ["tarde"],
    "noche": ["noche"],
}

DELIVERY_MODE_TYPO_MAP = {
    "presencial": ["presencial", "peesencial", " presencial"],
    "virtual": ["virtual"],
}

WEEKDAY_TYPO_MAP = {
    "lunes": ["lunes"],
    "martes": ["martes"],
    "miercoles": ["miercoles", "mierc"],
    "jueves": ["jueves"],
    "viernes": ["viernes", "mierc y viernes"],
    "sabado": ["sabado"],
}


TYPO_MAPPINGS = {
    "shift": SHIFT_TYPO_MAP,
    "delivery_mode": DELIVERY_MODE_TYPO_MAP,
    "weekday": WEEKDAY_TYPO_MAP,
}
