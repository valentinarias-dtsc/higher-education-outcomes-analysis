# Methodology

## 1. Purpose and Scope

This project analyzes academic outcomes in higher education using institutional course-section data from the first semester of 2024.

The unit of analysis is the **course section**. The project follows a staged workflow covering pseudonymization, data audit, cleaning, metric construction, and statistical analysis.

Version 1.0 is cross-sectional, observational, and limited to one academic term.

---

## 2. Data Sources

The workflow uses three tables:

### Enrollment

Primary institutional table at the course-section level.

It contains:

- total enrollment;
- academic outcome counts;
- course and section identifiers;
- partial operational metadata.

### Programs

Reference table containing program codes and program names.

### Offering

Supporting course-section table containing operational metadata such as:

- campus;
- weekday;
- schedule time;
- shift;
- delivery mode.

This table complements the enrollment data because several operational fields in the primary table contain substantial missingness.

---

## 3. Pseudonymization

Pseudonymization is performed before data auditing so that real data-quality issues can be documented without exposing institutional entities.

The following identifiers are replaced:

- campus names;
- course names and codes;
- program names and codes.

Implementation:

```text
scripts/build_sanitized_dataset.py
        │
        └── src/pipeline/
```

Pseudonymization supports safe documentation, but it does not make the underlying institutional records publicly distributable.

See [`confidentiality.md`](confidentiality.md) for the full publication boundary.

---

## 4. Data Audit

The audit stage reviews the sanitized source tables before corrective transformations are applied.

Implementation:

```text
notebooks/01_data_audit.ipynb
        │
        └── src/auditing.py
```

Main checks include:

- schema and data types;
- missing values;
- duplicates;
- categorical inconsistencies;
- key integrity;
- relationships across tables;
- consistency between enrollment totals and outcome counts.

---

## 5. Data Cleaning and Consolidation

The cleaning stage integrates the three sanitized sources into a single analytical base.

Implementation:

```text
notebooks/02_data_cleaning.ipynb
        │
        └── src/cleaning.py
```

Main operations include:

- text normalization;
- correction of inconsistent labels;
- categorical standardization;
- type conversion;
- completion of missing operational metadata from the offering table;
- program-level enrichment;
- consolidation at the course-section level;
- validation of outcome counts.

Output:

```text
data/clean/analytical_base.parquet
```

---

## 6. Metric Construction

The clean analytical base is transformed into the metrics required for analysis.

Implementation:

```text
notebooks/03_metric_construction.ipynb
        │
        └── src/metric_construction.py
```

Main derived variables include:

- total completion count;
- non-completion count;
- completion rate;
- promoted completion rate;
- regular completion rate;
- dropout rate;
- insufficient rate;
- free-status rate;
- excellence rate.

All rate variables are validated to remain within `[0, 1]`, and component sums are checked for internal consistency.

The exported dataset is the direct input to the statistical analysis stage.

---

## 7. Statistical Methodology

The statistical analysis is implemented in:

```text
notebooks/04_analysis.ipynb
```

The workflow includes:

- preliminary dataset characterization;
- descriptive statistics;
- confidence intervals for estimated means;
- Welch's one-way ANOVA for group comparisons;
- Games–Howell post hoc tests when omnibus tests are significant;
- partial eta-squared for effect-size estimation;
- residual-normality assessment;
- interpretation of statistical and practical significance.

The main analytical comparisons concern:

- delivery mode;
- shift;
- academic program.

Welch's ANOVA is used because it does not require equal variances and is appropriate for unequal group sizes.

The analysis is descriptive and inferential, not causal.

---

## 8. Reproducibility

The original institutional datasets and their direct derivatives are not public.

Accordingly:

- pseudonymization, audit, cleaning, and synthetic generation code are visible but require private inputs;
- metric construction and statistical analysis are publicly executable using synthetic demo data.

Public workflow:

```text
Synthetic Demo Analytical Base
        ↓
Metric Construction
        ↓
Demo Metrics Dataset
        ↓
Statistical Analysis
```

See [`project_architecture.md`](project_architecture.md) for the complete workflow.

---

## 9. Methodological Boundaries

The conclusions should be interpreted within the following limits:

- one institution;
- one academic term;
- course-section-level aggregation;
- no individual student covariates;
- observational design;
- possible dependence across related course sections;
- bounded outcome variables;
- results conditional on the selected models and assumptions.

Alternative approaches, including bootstrap methods, beta regression, and multilevel models, may be considered in future versions.
