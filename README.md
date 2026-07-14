# Higher Education Outcomes Analysis

An end-to-end data analytics project examining academic outcomes in higher education through a reproducible workflow built from confidential institutional data.

The project covers the complete analytical lifecycle: data auditing, cleaning, metric construction, exploratory analysis, statistical inference, visualization, and communication of results.

Its central research question is:

> **How do academic outcomes vary across course sections, programs, and instructional contexts?**

---

## Overview

Higher Education Outcomes Analysis investigates patterns and differences in academic performance across course sections belonging to different courses, academic programs, campuses, and instructional contexts.

The project was designed to demonstrate how a real-world institutional dataset can be transformed into a structured and documented analytical product while addressing data quality, methodological, reproducibility, and confidentiality requirements.

The main output is a reproducible analytical workflow. This workflow produces:

1. a statistical assessment of academic outcomes;
2. evidence that may support institutional decision-making;
3. technical documentation explaining the analytical and preprocessing decisions.

Version **1.0** covers the first academic term of 2024, identified throughout the project as **2024 C1**.

---

## Objectives

The project has five main objectives:

* design and implement a complete data analytics workflow;
* audit and transform raw institutional data into an analysis-ready dataset;
* construct interpretable academic outcome metrics;
* identify statistically relevant differences across institutional and instructional contexts;
* communicate the results through reproducible notebooks, visualizations, and technical documentation.

---

## Analytical Scope

### Unit of analysis

The unit of analysis is the **course section**.

Each observation represents a specific section associated with:

* one academic course;
* one academic program;
* one campus;
* a set of instructional and institutional characteristics;
* aggregated academic outcome metrics for that section.

The dataset does not represent individual student-level observations. Consequently, the analyses and conclusions apply to variation across course sections rather than to individual student trajectories.

### Time period

Version **1.0** is limited to **2024 C1**.

The integration of previous and subsequent academic terms is outside the scope of this release and is documented as future work.

---

## Analytical Workflow

The project follows a sequential analytical process:

```text
Raw institutional data
        ↓
Pseudonymization
        ↓
Data audit and quality assessment
        ↓
Cleaning and categorical standardization
        ↓
Metric construction and feature engineering
        ↓
Exploratory data analysis
        ↓
Statistical inference
        ↓
Visualization and result communication
```

Each stage is implemented separately to improve traceability, maintainability, and reproducibility.

### 1. Pseudonymization

Program, course, and campus names are pseudonymized immediately after ingesting the raw institutional data.

This transformation produces a protected version of the dataset that is then used throughout the rest of the analytical workflow, including the data audit stage.

This allows comparisons to remain interpretable while preventing the public identification of institutional entities.

### 2. Data audit

The initial audit evaluates the structure and quality of the pseudonymized dataset, including:

* missing values;
* duplicated records;
* inconsistent categories;
* invalid or unexpected values;
* data-type inconsistencies;
* logical relationships between variables.

### 3. Data cleaning and standardization

The cleaning stage applies documented transformation rules to produce consistent analytical variables.

This includes:

* normalization of column names;
* categorical standardization;
* treatment of missing and inconsistent values;
* validation of expected ranges and relationships;
* exclusion or correction of records according to explicit criteria.

### 4. Metric construction

Academic outcome metrics are constructed at the course-section level from the available institutional variables.

The project documents:

* the definition of each metric;
* its numerator and denominator;
* the treatment of missing or invalid cases;
* the interpretation and analytical limitations of the resulting measure.

### 5. Exploratory analysis

Exploratory data analysis is used to examine:

* metric distributions;
* variation across programs and courses;
* differences between instructional contexts;
* potential outliers;
* relationships between academic outcome indicators.

### 6. Statistical inference

Inferential methods are used to assess whether observed differences are compatible with systematic variation rather than sampling variability alone.

### 7. Communication

Results are presented through:

* reproducible notebooks;
* analytical figures;
* a technical report;
* an executive summary;
* methodological and limitation documents.

---

## Statistical Methods

The inferential analysis includes:

* descriptive statistics;
* confidence intervals;
* Welch’s analysis of variance;
* Games–Howell post hoc comparisons;
* Kruskal–Wallis tests;
* effect-size estimation.

Methods were selected according to the structure of the data, the analytical question, and the relevant statistical assumptions.

Statistical significance is not interpreted as sufficient evidence of institutional or practical relevance. Results are evaluated together with effect sizes, uncertainty, group distributions, and the observational limitations of the dataset.

Further details are available in `docs/methodology.md`.

---

## Key Findings

> This section will be completed using the final validated outputs from the analytical notebooks.

The final version should summarize between three and five findings, prioritizing:

* the most relevant variation in academic outcome metrics;
* differences across programs or instructional contexts;
* effect sizes and uncertainty where appropriate;
* findings with potential institutional relevance;
* results that can be communicated without exposing confidential information.

The section should avoid causal language because the project is based on observational and aggregated data.

---

## Repository Structure

```text
higher-education-outcomes-analysis/
│
├── data/
│   ├── raw/
│   ├── sanitized/
│   ├── clean/
│   ├── processed/
│   └── demo/
│
├── docs/
│   ├── methodology.md
│   ├── limitations.md
│   ├── confidentiality.md
│   └── version_notes.md
│
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_metric_construction.ipynb
│   └── 04_analysis.ipynb
│
├── reports/
│   ├── figures/
│   ├── analytical_report.pdf
│   └── executive_summary.pdf
│
├── src/
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

### Directory responsibilities

* `data/`: local, processed, and synthetic data resources;
* `notebooks/`: sequential analytical workflow and documented analysis;
* `src/`: reusable data-processing and analytical functions;
* `reports/`: final figures and written analytical deliverables;
* `docs/`: methodological, confidentiality, limitation, and version documentation.

The original institutional dataset is not included in the repository.

---

## Reproducibility

The repository is designed to make the analytical process inspectable and reproducible without redistributing confidential institutional records.

It includes:

* the complete data-processing logic;
* documented cleaning decisions;
* reusable Python functions;
* sequential analytical notebooks;
* metric definitions;
* statistical procedures;
* synthetic demonstration data;
* dependency specifications.

Because the original dataset cannot be publicly distributed, exact reproduction of the institutional results requires authorized access to the source data.

The synthetic dataset is intended to reproduce the expected schema and demonstrate the workflow. It does not reproduce the original institutional observations or necessarily preserve their empirical distributions.

---

## Confidentiality and Data Governance

The analysis was conducted using institutional data subject to confidentiality restrictions.

To preserve reproducibility while respecting those restrictions, this repository provides the complete analytical workflow, documentation, and reproducible code while excluding the original dataset.

The public version applies the following safeguards:

* program names are pseudonymized;
* course names are pseudonymized;
* campus names are pseudonymized;
* individual-level institutional records are not published;
* raw and intermediate confidential datasets are excluded;
* public results are presented at an aggregated analytical level;
* synthetic data is used for workflow demonstration.

Additional information is available in `docs/confidentiality.md`.

---

## Limitations

The results should be interpreted within the scope of the available data and the project design.

Principal limitations include:

* the analysis covers only one academic term;
* observations are aggregated at the course-section level;
* individual student trajectories are not available;
* the analysis is observational and does not establish causal relationships;
* course sections are nested within courses and programs;
* findings may not generalize beyond the institution and period studied;
* statistical comparisons may be affected by unequal group sizes and dependence between institutional units.

A detailed discussion is available in `docs/limitations.md`.

---

## Technology Stack

### Language

* Python

### Core libraries

* pandas
* NumPy
* SciPy
* statsmodels
* pingouin
* Matplotlib
* Seaborn

### Development environment

* Jupyter Notebook

---

## Project Deliverables

Version **1.0** includes three ordered deliverables.

### 1. Reproducible analytical workflow

A documented sequence covering data audit, cleaning, metric construction, exploratory analysis, statistical inference, and reporting.

### 2. Statistical assessment of academic outcomes

An analysis of how course-section academic outcomes vary across programs and instructional contexts.

### 3. Evidence for institutional decision-making

A structured set of findings that may be used to identify patterns, formulate questions, and prioritize areas for further institutional investigation.

The project does not claim that the statistical results alone determine institutional decisions.

---

## Future Work

Potential extensions include:

* integrating academic terms before and after 2024 C1;
* developing longitudinal comparisons;
* evaluating the stability of findings across periods;
* incorporating hierarchical or mixed-effects models;
* implementing additional sensitivity analyses;
* expanding synthetic-data coverage;
* developing an interactive reporting layer;
* evaluating additional institutional and instructional variables.

These extensions are not required to reproduce the scope of version **1.0**.

---

## Documentation

Project documentation is organized as follows:

* `docs/methodology.md`: analytical and statistical decisions;
* `docs/limitations.md`: scope and interpretation constraints;
* `docs/confidentiality.md`: data-protection measures;
* `docs/version_notes.md`: version 1.0 scope and future work;
* `reports/analytical_report.pdf`: full technical report;
* `reports/executive_summary.pdf`: concise summary for non-technical readers.

---

## Version

**Version 1.0**

This release includes the complete workflow for the analysis of 2024 C1, from data audit to statistical result communication.

See `docs/version_notes.md` for the complete release scope.

---

## License

This project is distributed under the terms specified in the `LICENSE` file.

The software license does not grant access to, ownership of, or redistribution rights over the original institutional dataset.

---

## Author

**Valentín Arias**

Data Science undergraduate
Universidad Nacional Guillermo Brown
