# Demo Data Card

The demo data supports the public metric-construction and statistical-analysis notebooks.

## Files

| File | Rows | Purpose |
|---|---:|---|
| `demo_analytical_base.parquet` | 297 | Input to `03_metric_construction.ipynb`. |
| `demo_processed_data.parquet` | 297 | Metric-enriched input to `04_analysis.ipynb`. |

## Provenance

The dataset preserves the pseudonymized course-section structure, operational attributes, and `total_enrollment` values of the clean analytical base. The following outcome fields are generated with a fixed random seed:

- `dropout_count`;
- `insufficient_count`;
- `free_status_count`;
- `promoted_completion_count`;
- `regular_completion_count`.

Generated outcomes are constrained to sum to `total_enrollment` and are calibrated to preserve the broad relationships explored by the analysis. The processed file adds the metrics defined in [Methodology](../../docs/methodology.md).

## Intended use

The files are suitable for running the public notebooks, reviewing the schema, testing metric logic, and examining the statistical workflow. Results should be described as demo results rather than institutional estimates.

The demo data preserves the qualitative conclusions of the reported comparisons, but it does not reproduce the institutional analysis numerically. Means, confidence intervals, test statistics, effect sizes, and p-values produced by the public notebooks therefore differ from the reviewed institutional results intended for the technical report.

For the broader publication boundary, see [Data confidentiality](../../docs/confidentiality.md).
