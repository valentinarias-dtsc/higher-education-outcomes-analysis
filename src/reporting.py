"""Report-ready statistical table transformations and exports.

The functions in this module only reshape, label, interpret, and round results.
They do not change the statistical tests used by the analysis.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import pingouin as pg


ALPHA = 0.05
FACTOR_LABELS = {
    "delivery_mode": "Delivery mode",
    "shift": "Shift",
    "program": "Academic program",
    "program_name": "Academic program",
}
FACTOR_ORDER = ["Delivery mode", "Shift", "Academic program"]
GROUP_LABELS = {
    "hybrid": "Hybrid",
    "on-site": "On-site",
    "online": "Online",
    "morning": "Morning",
    "afternoon": "Afternoon",
    "night": "Night",
}
GROUP_ORDER = {
    "Delivery mode": ["On-site", "Online", "Hybrid"],
    "Shift": ["Morning", "Afternoon", "Night"],
}


def _find_column(
    data: pd.DataFrame, candidates: Iterable[str], field_name: str
) -> str:
    """Return the first available alias or raise a clear schema error."""
    for candidate in candidates:
        if candidate in data.columns:
            return candidate
    aliases = ", ".join(candidates)
    raise ValueError(
        f"Missing required field '{field_name}'. Expected one of: {aliases}. "
        f"Available columns: {', '.join(map(str, data.columns))}"
    )


def validate_required_columns(data: pd.DataFrame, columns: Iterable[str]) -> None:
    """Validate columns with an error that identifies every missing field."""
    missing = [column for column in columns if column not in data.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")


def clean_factor_label(value: object) -> str:
    """Map a factor identifier to its report label."""
    key = str(value)
    if key not in FACTOR_LABELS:
        raise ValueError(f"Unknown factor label: {key}")
    return FACTOR_LABELS[key]


def clean_group_label(value: object) -> str:
    """Map known categories and preserve already-readable program labels."""
    key = str(value)
    return GROUP_LABELS.get(key, key)


def format_p_value(value: float) -> str:
    """Create a display value while retaining numeric p-values separately."""
    return "< 0.001" if value < 0.001 else f"{value:.4f}"


def round_p_value(value: float) -> float:
    """Round p-values without turning a positive result into numeric zero."""
    rounded = round(float(value), 4)
    return float(value) if value > 0 and rounded == 0 else rounded


def interpret_partial_eta_squared(value: float) -> str:
    """Interpret partial eta squared using documented descriptive thresholds."""
    if value < 0.01:
        return "Negligible"
    if value < 0.06:
        return "Small"
    if value < 0.14:
        return "Medium"
    return "Large"


def export_report_table(data: pd.DataFrame, path: str | Path) -> Path:
    """Export a deterministic CSV after basic report-table validation."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result = data.copy()
    if "p_value" in result.columns:
        if not pd.api.types.is_numeric_dtype(result["p_value"]):
            raise TypeError("p_value must remain numeric in report tables.")
        if ((result["p_value"] == 0) & result["p_value"].notna()).any():
            raise ValueError("A p-value rounded to zero; retain additional precision.")
    result.to_csv(output_path, index=False)
    return output_path


def format_welch_anova(raw: pd.DataFrame) -> pd.DataFrame:
    """Transform concatenated Pingouin Welch ANOVA output for reporting."""
    source = _find_column(raw, ["Source", "source", "factor"], "factor")
    numerator = _find_column(raw, ["ddof1", "numerator_df"], "numerator_df")
    denominator = _find_column(raw, ["ddof2", "denominator_df"], "denominator_df")
    statistic = _find_column(raw, ["F", "f_statistic"], "f_statistic")
    p_value = _find_column(raw, ["p-unc", "p_unc", "p_value"], "p_value")
    effect = _find_column(raw, ["np2", "partial_eta_squared"], "partial_eta_squared")

    result = pd.DataFrame(
        {
            "factor": raw[source].map(clean_factor_label),
            "numerator_df": pd.to_numeric(raw[numerator]),
            "denominator_df": pd.to_numeric(raw[denominator]),
            "f_statistic": pd.to_numeric(raw[statistic]),
            "p_value": pd.to_numeric(raw[p_value]),
            "partial_eta_squared": pd.to_numeric(raw[effect]),
        }
    )
    result["p_value_display"] = result["p_value"].map(format_p_value)
    result["significant"] = result["p_value"] < ALPHA
    result["effect_size_interpretation"] = result["partial_eta_squared"].map(
        interpret_partial_eta_squared
    )
    result["numerator_df"] = result["numerator_df"].round(2)
    result["denominator_df"] = result["denominator_df"].round(2)
    result["f_statistic"] = result["f_statistic"].round(3)
    result["p_value"] = result["p_value"].map(round_p_value)
    result["partial_eta_squared"] = result["partial_eta_squared"].round(3)
    order = {label: index for index, label in enumerate(FACTOR_ORDER)}
    return result.sort_values("factor", key=lambda x: x.map(order)).reset_index(drop=True)[
        [
            "factor",
            "numerator_df",
            "denominator_df",
            "f_statistic",
            "p_value",
            "p_value_display",
            "partial_eta_squared",
            "significant",
            "effect_size_interpretation",
        ]
    ]


def format_residual_normality(raw: pd.DataFrame) -> pd.DataFrame:
    """Transform concatenated Pingouin Shapiro-Wilk results for reporting."""
    source = _find_column(raw, ["Source", "source", "factor"], "factor")
    statistic = _find_column(raw, ["W", "w_statistic"], "w_statistic")
    p_value = _find_column(raw, ["pval", "p-unc", "p_value"], "p_value")
    result = pd.DataFrame(
        {
            "factor": raw[source].map(clean_factor_label),
            "w_statistic": pd.to_numeric(raw[statistic]),
            "p_value": pd.to_numeric(raw[p_value]),
        }
    )
    result["p_value_display"] = result["p_value"].map(format_p_value)
    result["normal_at_alpha_0_05"] = result["p_value"] >= ALPHA
    result["interpretation"] = np.where(
        result["normal_at_alpha_0_05"],
        "No statistically significant departure from normality",
        "Statistically significant departure from normality",
    )
    result["w_statistic"] = result["w_statistic"].round(3)
    result["p_value"] = result["p_value"].map(round_p_value)
    order = {label: index for index, label in enumerate(FACTOR_ORDER)}
    return result.sort_values("factor", key=lambda x: x.map(order)).reset_index(drop=True)[
        [
            "factor",
            "w_statistic",
            "p_value",
            "p_value_display",
            "normal_at_alpha_0_05",
            "interpretation",
        ]
    ]


def format_games_howell(raw: pd.DataFrame, factor: str) -> pd.DataFrame:
    """Transform Pingouin Games-Howell output, accepting common column aliases."""
    group_a = _find_column(raw, ["A", "group_a"], "group_a")
    group_b = _find_column(raw, ["B", "group_b"], "group_b")
    mean_a = _find_column(raw, ["mean(A)", "mean_A", "group_a_mean"], "group_a_mean")
    mean_b = _find_column(raw, ["mean(B)", "mean_B", "group_b_mean"], "group_b_mean")
    difference = _find_column(raw, ["diff", "mean_difference"], "mean_difference")
    standard_error = _find_column(raw, ["se", "standard_error"], "standard_error")
    statistic = _find_column(raw, ["T", "t", "t_statistic"], "t_statistic")
    degrees = _find_column(raw, ["df", "degrees_of_freedom"], "degrees_of_freedom")
    p_value = _find_column(raw, ["pval", "p-unc", "p_value"], "p_value")
    hedges = _find_column(raw, ["hedges", "hedges_g"], "hedges_g")

    result = pd.DataFrame(
        {
            "group_a": raw[group_a].map(clean_group_label),
            "group_b": raw[group_b].map(clean_group_label),
            "group_a_mean": pd.to_numeric(raw[mean_a]),
            "group_b_mean": pd.to_numeric(raw[mean_b]),
            "mean_difference": pd.to_numeric(raw[difference]),
            "standard_error": pd.to_numeric(raw[standard_error]),
            "t_statistic": pd.to_numeric(raw[statistic]),
            "degrees_of_freedom": pd.to_numeric(raw[degrees]),
            "p_value": pd.to_numeric(raw[p_value]),
            "hedges_g": pd.to_numeric(raw[hedges]),
        }
    )
    result["p_value_display"] = result["p_value"].map(format_p_value)
    result["significant"] = result["p_value"] < ALPHA

    def comparison_summary(row: pd.Series) -> str:
        if not row["significant"]:
            return "No statistically significant difference"
        direction = "lower than" if row["group_a_mean"] < row["group_b_mean"] else "higher than"
        return f"{row['group_a']} {direction} {str(row['group_b']).lower()}"

    result["comparison_summary"] = result.apply(comparison_summary, axis=1)
    for column in [
        "group_a_mean",
        "group_b_mean",
        "mean_difference",
        "standard_error",
        "t_statistic",
        "hedges_g",
    ]:
        result[column] = result[column].round(3)
    result["degrees_of_freedom"] = result["degrees_of_freedom"].round(2)
    result["p_value"] = result["p_value"].map(round_p_value)

    factor_label = clean_factor_label(factor)
    ordered_groups = GROUP_ORDER[factor_label]
    group_rank = {label: index for index, label in enumerate(ordered_groups)}
    result = result.assign(
        _first=result[["group_a", "group_b"]].apply(
            lambda row: min(group_rank[row.iloc[0]], group_rank[row.iloc[1]]), axis=1
        ),
        _second=result[["group_a", "group_b"]].apply(
            lambda row: max(group_rank[row.iloc[0]], group_rank[row.iloc[1]]), axis=1
        ),
    ).sort_values(["_first", "_second"])
    return result.drop(columns=["_first", "_second"]).reset_index(drop=True)[
        [
            "group_a",
            "group_b",
            "group_a_mean",
            "group_b_mean",
            "mean_difference",
            "standard_error",
            "t_statistic",
            "degrees_of_freedom",
            "p_value",
            "p_value_display",
            "hedges_g",
            "significant",
            "comparison_summary",
        ]
    ]


def group_descriptive_statistics(data: pd.DataFrame) -> pd.DataFrame:
    """Summarize completion rates by every report factor and group."""
    validate_required_columns(
        data, ["completion_rate", "delivery_mode", "shift", "program_name"]
    )
    frames: list[pd.DataFrame] = []
    for factor in ["delivery_mode", "shift", "program_name"]:
        summary = (
            data.groupby(factor, observed=True)["completion_rate"]
            .agg(section_count="count", mean_completion_rate="mean", standard_deviation="std", median_completion_rate="median")
            .reset_index(names="group")
        )
        sem = summary["standard_deviation"] / np.sqrt(summary["section_count"])
        # Matches the 1.96 * SEM confidence intervals used for group figures.
        summary["ci_95_lower"] = summary["mean_completion_rate"] - 1.96 * sem
        summary["ci_95_upper"] = summary["mean_completion_rate"] + 1.96 * sem
        summary.insert(0, "factor", clean_factor_label(factor))
        summary["group"] = summary["group"].map(clean_group_label)
        frames.append(summary)

    result = pd.concat(frames, ignore_index=True)
    factor_rank = {label: index for index, label in enumerate(FACTOR_ORDER)}

    def group_rank(row: pd.Series) -> int:
        if row["factor"] == "Academic program":
            return ord(str(row["group"]).split()[-1][0].upper())
        return GROUP_ORDER[row["factor"]].index(row["group"])

    result["_factor_rank"] = result["factor"].map(factor_rank)
    result["_group_rank"] = result.apply(group_rank, axis=1)
    result = result.sort_values(["_factor_rank", "_group_rank"]).drop(
        columns=["_factor_rank", "_group_rank"]
    )
    for column in [
        "mean_completion_rate",
        "standard_deviation",
        "median_completion_rate",
        "ci_95_lower",
        "ci_95_upper",
    ]:
        result[column] = result[column].round(3)
    return result.reset_index(drop=True)


def dataset_summary(data: pd.DataFrame) -> pd.DataFrame:
    """Create a concise summary of the section-level analytical dataset."""
    validate_required_columns(
        data,
        [
            "completion_rate",
            "program_name",
            "course_code",
            "total_enrollment",
        ],
    )
    completion = data["completion_rate"]
    rows = [
        ("Number of course sections", int(len(data))),
        ("Number of academic programs", int(data["program_name"].nunique())),
        ("Number of courses", int(data["course_code"].nunique())),
        ("Mean completion rate", round(float(completion.mean()), 3)),
        ("Standard deviation of completion rate", round(float(completion.std(ddof=1)), 3)),
        ("Median completion rate", round(float(completion.median()), 3)),
        ("Minimum completion rate", round(float(completion.min()), 3)),
        ("Maximum completion rate", round(float(completion.max()), 3)),
        ("Total enrollment", int(data["total_enrollment"].sum())),
        ("Median section enrollment", round(float(data["total_enrollment"].median()), 3)),
    ]
    return pd.DataFrame(rows, columns=["metric", "value"], dtype=object)


def completion_rate(data: pd.DataFrame) -> pd.Series:
    """Use an existing completion rate or reconstruct it from outcome counts."""
    if "completion_rate" in data.columns:
        return data["completion_rate"]
    validate_required_columns(
        data,
        ["promoted_completion_count", "regular_completion_count", "total_enrollment"],
    )
    completed = data["promoted_completion_count"] + data["regular_completion_count"]
    return completed / data["total_enrollment"]


def synthetic_dataset_validation(
    original: pd.DataFrame, synthetic: pd.DataFrame
) -> pd.DataFrame:
    """Compare dataset-level structure and completion-rate distributions."""
    validate_required_columns(original, ["program_name", "course_code", "delivery_mode", "shift"])
    validate_required_columns(synthetic, ["program_name", "course_code", "delivery_mode", "shift"])
    original_completion = completion_rate(original)
    synthetic_completion = completion_rate(synthetic)
    rows: list[tuple[str, float, float]] = [
        ("Row count", float(len(original)), float(len(synthetic))),
        ("Program count", float(original["program_name"].nunique()), float(synthetic["program_name"].nunique())),
        ("Course count", float(original["course_code"].nunique()), float(synthetic["course_code"].nunique())),
        ("Mean completion rate", float(original_completion.mean()), float(synthetic_completion.mean())),
        ("Completion-rate standard deviation", float(original_completion.std(ddof=1)), float(synthetic_completion.std(ddof=1))),
    ]
    for factor, label in [("delivery_mode", "Delivery mode"), ("shift", "Shift")]:
        original_proportions = original[factor].value_counts(normalize=True)
        synthetic_proportions = synthetic[factor].value_counts(normalize=True)
        categories = sorted(set(original_proportions.index) | set(synthetic_proportions.index))
        for category in categories:
            metric = f"{label}: {clean_group_label(category)} proportion"
            rows.append(
                (
                    metric,
                    float(original_proportions.get(category, 0.0)),
                    float(synthetic_proportions.get(category, 0.0)),
                )
            )
    result = pd.DataFrame(rows, columns=["metric", "original_value", "synthetic_value"])
    result["absolute_difference"] = (
        result["original_value"] - result["synthetic_value"]
    ).abs()
    for column in ["original_value", "synthetic_value", "absolute_difference"]:
        result[column] = result[column].round(4)
    count_rows = result["metric"].isin(["Row count", "Program count", "Course count"])
    for column in ["original_value", "synthetic_value", "absolute_difference"]:
        result[column] = result[column].astype(object)
        result.loc[count_rows, column] = result.loc[count_rows, column].map(int)
    return result


def _welch_row(data: pd.DataFrame, factor: str, dataset: str) -> dict[str, object]:
    working = data.assign(completion_rate=completion_rate(data))
    if factor == "program_name":
        counts = working[factor].value_counts()
        working = working[working[factor].isin(counts[counts >= 10].index)]
    result = pg.welch_anova(dv="completion_rate", between=factor, data=working)
    p_column = _find_column(result, ["p-unc", "p_unc", "p_value"], "p_value")
    return {
        "factor": clean_factor_label(factor),
        "dataset": dataset,
        "f_statistic": float(result.loc[0, "F"]),
        "p_value": float(result.loc[0, p_column]),
        "partial_eta_squared": float(result.loc[0, "np2"]),
    }


def synthetic_inferential_validation(
    original: pd.DataFrame, synthetic: pd.DataFrame
) -> pd.DataFrame:
    """Compare the same Welch ANOVA outputs for original and synthetic data."""
    rows = []
    for factor in ["delivery_mode", "shift", "program_name"]:
        rows.append(_welch_row(original, factor, "Original"))
        rows.append(_welch_row(synthetic, factor, "Synthetic"))
    result = pd.DataFrame(rows)
    result["significant"] = result["p_value"] < ALPHA
    result["f_statistic"] = result["f_statistic"].round(3)
    result["p_value"] = result["p_value"].map(round_p_value)
    result["partial_eta_squared"] = result["partial_eta_squared"].round(3)
    return result[
        [
            "factor",
            "dataset",
            "f_statistic",
            "p_value",
            "partial_eta_squared",
            "significant",
        ]
    ]
