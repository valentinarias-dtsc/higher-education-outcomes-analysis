# Data Confidentiality and Reproducibility

## Purpose

This document defines the confidentiality boundaries, publication rules, and reproducibility scope of the **Higher Education Outcomes Analysis** project.

The project was developed using institutional data subject to a formal confidentiality commitment. As a result, the original datasets and their direct derivatives are not publicly distributed.

The repository instead publishes the complete analytical implementation, methodological documentation, reviewed aggregate outputs, and a fully synthetic demo dataset for downstream execution.

---

## Confidential Data Sources

The original workflow uses three source tables:

### Enrollment

The primary institutional dataset.

- Unit of observation: course section
- Contains enrollment totals and academic outcome counts
- Includes partial operational metadata
- Was provided by the university within the context of an academic course

### Programs

A reference table containing program codes and program names.

Although this table is publicly available, its use within the project is integrated with restricted institutional records.

### Offering

A supporting course-section-level table containing operational metadata, including:

- weekday
- campus
- schedule time
- shift
- delivery mode

This table is used to complement the enrollment dataset, where several operational fields contain substantial missingness.

The original source files, sanitized copies derived from them, and consolidated institutional datasets are treated as non-public project assets.

---

## Pseudonymization Strategy

Institutional entities are pseudonymized before any audit or exploratory output is produced.

The pseudonymized entities include:

- campus names
- course names
- course codes
- program names
- program codes

This stage is implemented through:

```text
scripts/build_sanitized_dataset.py
        │
        └── src/pipeline/
```

Pseudonymization serves two purposes:

1. reduce exposure of institutional identifiers;
2. allow the audit and cleaning notebooks to display real structural and data-quality issues.

Pseudonymization does **not** make the original or derived institutional datasets publicly distributable.

The transformed records still preserve institutional counts, structures, relationships, and observed outcomes. They are therefore excluded from the public repository.

Mappings between real and pseudonymized identifiers are also private and are never distributed.

---

## Publication Boundaries

### Publicly available

The repository may include:

- source code;
- pipeline logic;
- auditing utilities;
- cleaning and standardization functions;
- metric-construction logic;
- statistical-analysis code;
- narrative notebooks with reviewed outputs;
- methodological documentation;
- aggregate figures and findings approved for publication;
- synthetic demo data;
- project reports and summaries.

### Not publicly available

The repository does not include:

- original institutional source files;
- sanitized datasets derived from the original records;
- the real clean analytical base;
- direct row-level derivatives of institutional data;
- pseudonymization mappings;
- real institutional identifiers;
- outputs that could reasonably enable reconstruction of protected records;
- intermediate files produced during the private pipeline.

These restrictions apply regardless of whether a file contains direct identifiers.

---

## Synthetic Demo Dataset

To support public execution of the downstream analytical workflow, the repository provides a fully synthetic demo dataset.

The synthetic dataset:

- contains no original observations;
- preserves the public schema;
- preserves the course-section unit of analysis;
- retains pseudonymized entity labels used by the project;
- satisfies the relevant logical constraints;
- reproduces the qualitative relationships examined in the analysis;
- supports execution of the metric-construction and statistical-analysis notebooks.

The synthetic data are designed for demonstration and reproducibility of the analytical workflow.

They are **not** intended to:

- reproduce exact institutional estimates;
- replicate exact p-values or confidence intervals;
- support substantive conclusions about the university;
- serve as a substitute for the original institutional records.

Results produced from the demo dataset must therefore be interpreted as synthetic workflow outputs.

---

## Reproducibility Scope

The repository intentionally distinguishes between code availability and public executability.

| Stage | Code publicly visible | Required data publicly available | Publicly executable |
|---|---:|---:|---:|
| Institutional pseudonymization | Yes | No | No |
| Data audit | Yes | No | No |
| Data cleaning and consolidation | Yes | No | No |
| Synthetic data generation | Yes | No | No |
| Metric construction | Yes | Yes, synthetic | Yes |
| Statistical analysis | Yes | Yes, synthetic | Yes |

The non-executable stages remain available for technical review. Their lack of public execution reflects the confidentiality restriction on the required inputs, not missing implementation.

The publicly reproducible workflow begins with the synthetic analytical base and continues through:

```text
Synthetic Demo Analytical Base
        ↓
Metric Construction
        ↓
Demo Metrics Dataset
        ↓
Statistical Analysis
```

---

## Relationship Between Public Notebooks and Institutional Results

The project separates two kinds of outputs:

### Institutional analysis outputs

These are produced from the private institutional analytical dataset.

They may appear only as:

- reviewed aggregate tables;
- reviewed figures;
- high-level findings;
- analytical reports;
- executive summaries.

### Demo analysis outputs

These are generated from the synthetic dataset and are publicly reproducible.

They demonstrate:

- the analytical workflow;
- the metric definitions;
- the statistical procedures;
- the use of reusable project modules.

The two sets of outputs may be qualitatively similar, but they should not be expected to match numerically.

---

## Responsible Use

The public code and synthetic dataset are provided for educational, technical-review, and portfolio purposes.

Users should not:

- interpret synthetic outputs as institutional evidence;
- attempt to infer or reconstruct the original data;
- represent demo results as findings about the university;
- assume that pseudonymized labels correspond to publicly identifiable entities.

Any future publication of additional institutional outputs should be preceded by a separate confidentiality and disclosure-risk review.

---

## Summary

This repository publishes the complete analytical implementation while withholding the original institutional data and their direct derivatives.

Pseudonymization enables safe technical documentation of the private workflow, but it is not treated as authorization for redistribution.

Public reproducibility is provided through a fully synthetic analytical dataset that supports the downstream stages of metric construction and statistical analysis without exposing original observations.
