"""End-to-end sanitized dataset builder."""

from pathlib import Path

from src.pipeline.export import export_dataset
from src.pipeline.ingest import (
    load_enrollment,
    load_offering,
    load_program_lookup,
)
from src.pipeline.normalize import (
    normalize_enrollment,
    normalize_offering,
    normalize_program_lookup,
)
from src.pipeline.sanitize import (
    sanitize_enrollment,
    sanitize_offering,
    sanitize_program_lookup,
)
from src.pipeline.validate import (
    validate_row_count,
    validate_unique_keys,
)
from src.config.constants import (
    SANITIZED_DATA_DIR,
    RAW_DATA_DIR,
)


RAW_DIR = Path(RAW_DATA_DIR)
SANITIZED_DIR = Path(SANITIZED_DATA_DIR)



def main():
    print("Loading raw datasets...")

    enrollment_raw = load_enrollment(
        RAW_DIR / "enrollment.xlsx"
    )
    assert enrollment_raw is not None, "Failed to load enrollment dataset"

    offering_raw = load_offering(
        RAW_DIR / "offering.csv"
    )
    assert offering_raw is not None, "Failed to load offering dataset"

    programs_raw = load_program_lookup(
        RAW_DIR / "program_lookup.csv"
    )
    assert programs_raw is not None, "Failed to load program lookup dataset"

    print("Applying structural normalization...")

    enrollment = normalize_enrollment(enrollment_raw)
    offering = normalize_offering(offering_raw)
    programs = normalize_program_lookup(programs_raw)

    print("Applying deterministic sanitization...")

    enrollment_sanitized = sanitize_enrollment(enrollment)
    offering_sanitized = sanitize_offering(offering)
    programs_sanitized = sanitize_program_lookup(programs)

    print("Running validation checks...")

    validate_row_count(enrollment, enrollment_sanitized)
    validate_row_count(offering, offering_sanitized)
    validate_row_count(programs, programs_sanitized)

    validate_unique_keys(
        programs_sanitized,
        ["program_code"],
    )
    validate_unique_keys(
        enrollment_sanitized,
        ["course_code", "section"],
    )
    validate_unique_keys(
        offering_sanitized,
        ["course_code", "section"],
    )

    print("Exporting sanitized datasets...")

    export_dataset(
        enrollment_sanitized,
        SANITIZED_DIR / "enrollment.parquet",
    )

    export_dataset(
        offering_sanitized,
        SANITIZED_DIR / "offering.parquet",
    )

    export_dataset(
        programs_sanitized,
        SANITIZED_DIR / "program_lookup.parquet",
    )

    print("Sanitized datasets successfully built.")


if __name__ == "__main__":
    main() 