"""Generate a reproducible synthetic analytical base for public demos.

The source analytical base contains pseudonymized institutional structure that
can be shared, but the outcome counts are regenerated here. The synthetic data
is designed to preserve the qualitative behavior used by the analysis notebooks
without redistributing original observations.
"""

from __future__ import annotations

from contextlib import redirect_stdout
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import pingouin as pg

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config.constants import (
    CLEAN_DATA_DIR,
    DEMO_DATA_DIR,
    RANDOM_SEED
)
from src.reporting import (
    export_report_table,
    synthetic_dataset_validation,
    synthetic_inferential_validation,
)

INPUT_PATH = Path(CLEAN_DATA_DIR) / "analytical_base.parquet"
OUTPUT_PATH = Path(DEMO_DATA_DIR) / "demo_analytical_base.parquet"
VALIDATION_LOG_PATH = Path("reports/appendix/synthetic_generator_validation.txt")
TABLE_OUTPUT_DIR = Path("reports/tables")

STRUCTURE_COLUMNS = [
    "course_name",
    "section",
    "total_enrollment",
    "course_code",
    "program_code",
    "workload",
    "shift",
    "weekday",
    "schedule_time",
    "delivery_mode",
    "campus",
    "program_name",
]

OUTCOME_COLUMNS = [
    "dropout_count",
    "insufficient_count",
    "free_status_count",
    "promoted_completion_count",
    "regular_completion_count",
]

OUTPUT_COLUMNS = [
    "course_name",
    "section",
    "total_enrollment",
    "dropout_count",
    "insufficient_count",
    "free_status_count",
    "promoted_completion_count",
    "regular_completion_count",
    "course_code",
    "program_code",
    "workload",
    "shift",
    "weekday",
    "schedule_time",
    "delivery_mode",
    "campus",
    "program_name",
]


def completion_rate(df: pd.DataFrame) -> pd.Series:
    """Reconstruct completion rate from outcome counts."""
    completed = (
        df["promoted_completion_count"] + df["regular_completion_count"]
    )
    return completed / df["total_enrollment"]


def estimate_completion_model(df: pd.DataFrame) -> tuple[float, pd.Series, pd.Series, float]:
    """Estimate the simple additive components used for synthetic generation."""
    original_completion = completion_rate(df)
    global_mean = float(original_completion.mean())

    delivery_effect = (
        original_completion.groupby(df["delivery_mode"]).mean() - global_mean
    )
    shift_effect = original_completion.groupby(df["shift"]).mean() - global_mean

    fitted = (
        global_mean
        + df["delivery_mode"].map(delivery_effect)
        + df["shift"].map(shift_effect)
    )
    residual_sd = float((original_completion - fitted).std(ddof=1))

    return global_mean, delivery_effect, shift_effect, residual_sd


def centered_group_noise(
    noise: np.ndarray,
    groups: pd.DataFrame,
    group_columns: list[str],
    iterations: int = 3,
) -> np.ndarray:
    """Keep random noise from shifting the main analytical group averages."""
    centered = pd.Series(noise, index=groups.index, dtype="float64")

    for _ in range(iterations):
        for column in group_columns:
            centered = centered - centered.groupby(groups[column]).transform("mean")

    return centered.to_numpy()


def generate_synthetic_outcomes(df: pd.DataFrame) -> pd.DataFrame:
    """Copy structure columns and regenerate synthetic outcome counts."""
    rng = np.random.default_rng(RANDOM_SEED)
    global_mean, delivery_effect, shift_effect, residual_sd = estimate_completion_model(df)

    program_effects = pd.Series(
        rng.normal(loc=0.0, scale=0.015, size=df["program_name"].nunique()),
        index=pd.Index(df["program_name"].drop_duplicates(), name="program_name"),
    )

    noise = rng.normal(loc=0.0, scale=residual_sd, size=len(df))
    noise = centered_group_noise(noise, df, ["delivery_mode", "shift"])
    synthetic_completion = (
        global_mean
        + df["delivery_mode"].map(delivery_effect).to_numpy()
        + df["shift"].map(shift_effect).to_numpy()
        + df["program_name"].map(program_effects).to_numpy()
        + noise
    )
    synthetic_completion = np.clip(synthetic_completion, 0.0, 1.0)

    total_enrollment = df["total_enrollment"].to_numpy()
    completed = np.rint(synthetic_completion * total_enrollment).astype(int)
    completed = np.clip(completed, 0, total_enrollment)

    promoted = rng.binomial(completed, 0.42)
    regular = completed - promoted

    remaining = total_enrollment - completed
    remaining_split = np.array(
        [rng.multinomial(int(n), [0.35, 0.40, 0.25]) for n in remaining]
    )

    synthetic = df[STRUCTURE_COLUMNS].copy()
    synthetic["dropout_count"] = remaining_split[:, 0]
    synthetic["insufficient_count"] = remaining_split[:, 1]
    synthetic["free_status_count"] = remaining_split[:, 2]
    synthetic["promoted_completion_count"] = promoted
    synthetic["regular_completion_count"] = regular

    for column in OUTCOME_COLUMNS:
        synthetic[column] = synthetic[column].astype(df[column].dtype)

    return synthetic[OUTPUT_COLUMNS]


def welch_summary(df: pd.DataFrame, factor: str) -> pd.Series:
    """Return Welch ANOVA statistics for a factor."""
    data = df.assign(completion_rate=completion_rate(df))

    if factor == "program_name":
        counts = data[factor].value_counts()
        valid_groups = counts[counts >= 10].index
        data = data[data[factor].isin(valid_groups)]

    result = pg.welch_anova(dv="completion_rate", between=factor, data=data)
    p_column = "p-unc" if "p-unc" in result.columns else "p_unc"

    return pd.Series(
        {
            "F": result.loc[0, "F"],
            "p": result.loc[0, p_column],
            "np2": result.loc[0, "np2"],
        }
    )


def print_validation_report(original: pd.DataFrame, synthetic: pd.DataFrame) -> None:
    """Print concise data quality and statistical validation output."""
    synthetic_completion = completion_rate(synthetic)

    print("\nSynthetic dataset validation")
    print("-" * 30)
    print(f"Rows: {len(synthetic):,}")
    print(f"Programs: {synthetic['program_name'].nunique():,}")
    print(f"Courses: {synthetic['course_code'].nunique():,}")
    print(f"Mean completion: {synthetic_completion.mean():.4f}")
    print(f"Standard deviation: {synthetic_completion.std(ddof=1):.4f}")
    print(
        "Completion range: "
        f"{synthetic_completion.min():.4f} to {synthetic_completion.max():.4f}"
    )

    print("\nDelivery proportions")
    print(synthetic["delivery_mode"].value_counts(normalize=True).sort_index().round(4))

    print("\nShift proportions")
    print(synthetic["shift"].value_counts(normalize=True).sort_index().round(4))

    print("\nMean completion by delivery mode")
    print(synthetic_completion.groupby(synthetic["delivery_mode"]).mean().round(4))

    print("\nMean completion by shift")
    print(synthetic_completion.groupby(synthetic["shift"]).mean().round(4))

    print("\nWelch ANOVA validation")
    print("-" * 30)
    for factor in ["delivery_mode", "shift", "program_name"]:
        original_stats = welch_summary(original, factor)
        synthetic_stats = welch_summary(synthetic, factor)

        print(f"\n{factor}")
        print(
            "Original : "
            f"F={original_stats['F']:.4f}, "
            f"p={original_stats['p']:.4f}, "
            f"partial_eta_sq={original_stats['np2']:.4f}"
        )
        print(
            "Synthetic: "
            f"F={synthetic_stats['F']:.4f}, "
            f"p={synthetic_stats['p']:.4f}, "
            f"partial_eta_sq={synthetic_stats['np2']:.4f}"
        )


def validate_counts(synthetic: pd.DataFrame) -> None:
    """Fail fast if generated counts do not reconcile row by row."""
    component_sum = synthetic[OUTCOME_COLUMNS].sum(axis=1)
    if not component_sum.equals(synthetic["total_enrollment"]):
        raise ValueError("Synthetic outcome counts do not sum to total_enrollment.")


def main() -> None:
    original = pd.read_parquet(INPUT_PATH)
    synthetic = generate_synthetic_outcomes(original)

    validate_counts(synthetic)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    synthetic.to_parquet(OUTPUT_PATH, index=False)

    VALIDATION_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_LOG_PATH.open("w", encoding="utf-8") as validation_log:
        with redirect_stdout(validation_log):
            print(f"Wrote synthetic analytical base to: {OUTPUT_PATH}")
            print_validation_report(original, synthetic)

    export_report_table(
        synthetic_dataset_validation(original, synthetic),
        TABLE_OUTPUT_DIR / "synthetic_dataset_validation.csv",
    )
    export_report_table(
        synthetic_inferential_validation(original, synthetic),
        TABLE_OUTPUT_DIR / "synthetic_inferential_validation.csv",
    )

    print(f"Wrote synthetic analytical base to: {OUTPUT_PATH}")
    print(f"Wrote detailed validation log to: {VALIDATION_LOG_PATH}")
    print(f"Wrote structured validation tables to: {TABLE_OUTPUT_DIR}")


if __name__ == "__main__":
    main()
