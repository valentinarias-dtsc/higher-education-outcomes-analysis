# Report table sources

The CSV files in this directory come from different data sources and should not be interpreted as one homogeneous result set.

## Reviewed institutional results

- `welch_anova_summary.csv`
- `residual_normality_summary.csv`
- `games_howell_delivery_summary.csv`
- `games_howell_shift_summary.csv`

These tables contain reviewed aggregate results from the private institutional processed dataset.

## Public synthetic demo results

- `demo_dataset_summary.csv`
- `demo_group_descriptive_statistics.csv`

These tables contain exclusively synthetic descriptive results generated from `data/demo/demo_processed_data.parquet`. They demonstrate the public workflow and must not be used as institutional estimates.

## Original-versus-synthetic validation

- `synthetic_dataset_validation.csv`
- `synthetic_inferential_validation.csv`

These tables compare aggregate properties and Welch ANOVA results from the original and synthetic analytical bases. They validate the public demo's broad analytical behavior; they do not establish that synthetic row-level outcomes reproduce confidential institutional observations.

All tables are generated deterministically by `scripts/generate_report_tables.py`.
