# Methodology

This document records the methodology implemented in the completed Version 1.0 workflow: how the source data was assessed, transformed into a section-level analytical base, converted into outcome metrics, and evaluated statistically. Candidate methods for later releases are maintained separately in [Version notes and roadmap](version_notes.md).

## Scope

Version 1.0 examines **2024 C1**, one academic term at one institution. The unit of analysis is the **course section**. Each row contains aggregated enrollment outcomes and operational characteristics; the project does not use student-level observations.

The main comparisons evaluate completion rates across delivery modes, class shifts, and academic programs.

## Data sources

| Source | Analytical role |
|---|---|
| Enrollment | Primary source for total enrollment and five academic-outcome counts. |
| Offering | Canonical source for workload, campus, weekday, schedule time, shift, and delivery mode. |
| Programs | Reference source for program names. |

Enrollment includes operational fields, but several are substantially incomplete. The audit therefore establishes Offering as the canonical source for those attributes.

## Data audit

The audit evaluates whether the three inputs can support reliable integration and analysis. Checks include:

- schema and data types;
- candidate-key uniqueness and duplicate records;
- missingness and categorical consistency;
- referential integrity and merge coverage;
- consistency between enrollment totals and outcome components.

The notebook records the evidence behind each subsequent cleaning rule rather than treating cleaning as an opaque preprocessing step.

## Cleaning and consolidation

The cleaning workflow applies a small set of explicit transformations:

1. Remove incomplete operational fields from Enrollment.
2. Normalize Offering text and map shift, weekday, and delivery mode to canonical categories.
3. Convert workload to a nullable integer.
4. Reconcile total enrollment when its difference from the five outcome components is no greater than two, retaining reconciliation flags.
5. Join Offering by `course_code` and `section`, then Programs by `program_code`.
6. Exclude six Enrollment records that cannot be matched to Offering and therefore lack reliable operational metadata.

The resulting analytical base contains **297 of 303** sanitized Enrollment records.

## Metric construction

The feature-engineering stage converts raw outcome counts into measures that can be compared across sections of different sizes.

| Metric | Definition |
|---|---|
| `completion_count` | Promoted completions + regular completions |
| `attrition_count` | Dropouts + free-status outcomes |
| `adverse_outcomes_count` | Dropouts + insufficient outcomes + free-status outcomes |
| Component rates | Each component count / total enrollment |
| `completion_rate` | Completion count / total enrollment |
| `attrition_rate` | Attrition count / total enrollment |
| `adverse_outcomes_rate` | Adverse outcomes count / total enrollment |
| `excellence_ratio` | Promoted completions / all completions |

`excellence_ratio` describes the composition of successful outcomes rather than the share of all enrolled students. It is represented as zero for sections with no completions. Validation checks enforce expected bounds, completeness, and additive identities.

## Statistical analysis

The analysis uses `completion_rate` as its principal outcome.

### Baseline

Descriptive statistics, a distribution plot, and a Student's *t* confidence interval summarize the overall section-level completion rate.

### Group comparisons

Delivery mode, shift, and program are evaluated with Welch's one-way ANOVA. Welch's method is appropriate here because group sizes are unbalanced and equal variances are not assumed. Shapiro-Wilk tests assess model residuals, and significant omnibus results are followed by Games-Howell pairwise comparisons.

Partial eta-squared accompanies significance tests to distinguish statistical evidence from practical magnitude. Programs with fewer than ten sections are excluded from the program comparison to avoid presenting highly unstable estimates.

For report tables, partial eta-squared is described using a single consistent rule: values below 0.01 are **negligible**, 0.01 through 0.059 are **small**, 0.06 through 0.139 are **medium**, and values of 0.14 or greater are **large**. These labels are descriptive and do not alter the inferential conclusion. Statistical significance is evaluated at alpha = 0.05 and is always retained as an explicit Boolean field alongside the numeric p-value.

Raw institutional Pingouin outputs are preserved under `reports/appendix/statistical_outputs/`. Cleaned institutional inferential summaries are exported to `reports/tables/` alongside public demo descriptives and original-versus-synthetic validation tables by `scripts/generate_report_tables.py`. The exclusively synthetic descriptive outputs are named `demo_dataset_summary.csv` and `demo_group_descriptive_statistics.csv`; their `demo_` prefix distinguishes them from reviewed institutional results. The validation tables contain both original and synthetic aggregate results. This source distinction is intentional: the public notebooks produce demo estimates, while the technical report presents reviewed institutional inference and clearly labels demo-only context.

### Multivariate exploration

A shift-by-delivery-mode heatmap explores how completion patterns vary across combinations of operational factors. This view is descriptive; the notebook does not estimate a formal interaction model.

## Interpretation boundaries

The project is an observational, section-level case study. Its main interpretation boundaries are:

- one institution and one academic term;
- no student-level characteristics or longitudinal trajectories;
- possible dependence among sections that share courses, programs, instructors, or students;
- bounded outcome rates and unequal group sizes;
- potential selection effects from the six unmatched sections excluded during integration;
- associations that should not be interpreted as causal effects.

The demo data reproduces the public downstream workflow and broad analytical patterns, but its numerical outputs are demonstration results rather than institutional estimates. See [Project limitations](limitations.md) for the concise interpretation boundary and [Version notes and roadmap](version_notes.md) for extensions beyond Version 1.0.
