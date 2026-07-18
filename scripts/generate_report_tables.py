"""Generate raw statistical outputs and report-ready CSV tables."""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import pingouin as pg
from statsmodels.formula.api import ols

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.reporting import (
    dataset_summary,
    export_report_table,
    format_games_howell,
    format_residual_normality,
    format_welch_anova,
    group_descriptive_statistics,
    synthetic_dataset_validation,
    synthetic_inferential_validation,
)


RAW_OUTPUT_DIR = PROJECT_ROOT / "reports" / "appendix" / "statistical_outputs"
TABLE_OUTPUT_DIR = PROJECT_ROOT / "reports" / "tables"
ORIGINAL_PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "processed_data.parquet"
DEMO_PROCESSED_PATH = PROJECT_ROOT / "data" / "demo" / "demo_processed_data.parquet"
ORIGINAL_BASE_PATH = PROJECT_ROOT / "data" / "clean" / "analytical_base.parquet"
SYNTHETIC_BASE_PATH = PROJECT_ROOT / "data" / "demo" / "demo_analytical_base.parquet"


def build_raw_statistical_outputs(data: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Run the same Pingouin tests used in the institutional analysis notebook."""
    required = {"completion_rate", "delivery_mode", "shift", "program_name"}
    missing = sorted(required - set(data.columns))
    if missing:
        raise ValueError(f"Institutional processed data is missing: {', '.join(missing)}")

    factor_data: dict[str, pd.DataFrame] = {
        "delivery_mode": data,
        "shift": data,
    }
    program_counts = data["program_name"].value_counts()
    factor_data["program_name"] = data[
        data["program_name"].isin(program_counts[program_counts >= 10].index)
    ]

    anova_frames = []
    shapiro_frames = []
    for factor, working in factor_data.items():
        anova_frames.append(
            pg.welch_anova(dv="completion_rate", between=factor, data=working)
        )
        residuals = ols(f"completion_rate ~ C({factor})", data=working).fit().resid
        normality = pg.normality(residuals).copy()
        normality.insert(0, "Source", factor)
        shapiro_frames.append(normality)

    return {
        "welch_anova": pd.concat(anova_frames, ignore_index=True),
        "residual_shapiro": pd.concat(shapiro_frames, ignore_index=True),
        "games_howell_delivery": pg.pairwise_gameshowell(
            dv="completion_rate", between="delivery_mode", data=data
        ),
        "games_howell_shift": pg.pairwise_gameshowell(
            dv="completion_rate", between="shift", data=data
        ),
    }


def main() -> None:
    """Write the complete deterministic report table suite."""
    original_processed = pd.read_parquet(ORIGINAL_PROCESSED_PATH)
    demo_processed = pd.read_parquet(DEMO_PROCESSED_PATH)
    original_base = pd.read_parquet(ORIGINAL_BASE_PATH)
    synthetic_base = pd.read_parquet(SYNTHETIC_BASE_PATH)

    RAW_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    raw = build_raw_statistical_outputs(original_processed)
    raw_paths = {
        "welch_anova": RAW_OUTPUT_DIR / "welch_anova_raw.csv",
        "residual_shapiro": RAW_OUTPUT_DIR / "residual_shapiro_raw.csv",
        "games_howell_delivery": RAW_OUTPUT_DIR / "games_howell_delivery_raw.csv",
        "games_howell_shift": RAW_OUTPUT_DIR / "games_howell_shift_raw.csv",
    }
    for name, frame in raw.items():
        frame.to_csv(raw_paths[name], index=False)

    export_report_table(
        format_welch_anova(raw["welch_anova"]),
        TABLE_OUTPUT_DIR / "welch_anova_summary.csv",
    )
    export_report_table(
        format_residual_normality(raw["residual_shapiro"]),
        TABLE_OUTPUT_DIR / "residual_normality_summary.csv",
    )
    export_report_table(
        format_games_howell(raw["games_howell_delivery"], "delivery_mode"),
        TABLE_OUTPUT_DIR / "games_howell_delivery_summary.csv",
    )
    export_report_table(
        format_games_howell(raw["games_howell_shift"], "shift"),
        TABLE_OUTPUT_DIR / "games_howell_shift_summary.csv",
    )
    export_report_table(
        group_descriptive_statistics(demo_processed),
        TABLE_OUTPUT_DIR / "group_descriptive_statistics.csv",
    )
    export_report_table(
        dataset_summary(demo_processed), TABLE_OUTPUT_DIR / "dataset_summary.csv"
    )
    export_report_table(
        synthetic_dataset_validation(original_base, synthetic_base),
        TABLE_OUTPUT_DIR / "synthetic_dataset_validation.csv",
    )
    export_report_table(
        synthetic_inferential_validation(original_base, synthetic_base),
        TABLE_OUTPUT_DIR / "synthetic_inferential_validation.csv",
    )

    for path in [*raw_paths.values(), *sorted(TABLE_OUTPUT_DIR.glob("*.csv"))]:
        print(path.relative_to(PROJECT_ROOT))


if __name__ == "__main__":
    main()
