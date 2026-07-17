# Higher Education Outcomes Analysis

An end-to-end analytics project exploring how academic outcomes vary across course sections, programs, delivery modes, and class schedules.

Built from a real institutional use case, the project demonstrates a complete analytical workflow: source-data validation, deterministic cleaning, feature engineering, statistical analysis, and clear communication of results. The implementation combines narrative notebooks with reusable Python modules so that analytical decisions remain visible without being embedded entirely in notebook code.

## The question

> **How do academic outcomes vary across course sections, programs, and instructional contexts?**

Version 1.0 examines **2024 C1**, one academic term at one institution. Each observation represents a course section with aggregated enrollment and outcome counts.

## What makes the project technically interesting

- Three source tables are validated and consolidated through explicit data contracts and relationship checks.
- Institutional identifiers are pseudonymized before analytical inspection.
- Data-quality findings drive deterministic cleaning and reconciliation rules.
- Reusable modules separate audit, cleaning, and metric logic from notebook presentation.
- A public demo dataset supports execution of metric construction and statistical analysis.
- Statistical comparisons account for unequal variances and unbalanced group sizes.

## Workflow

```mermaid
flowchart TD
    subgraph Original["Original institutional workflow"]
        A["Source tables"] --> B["Pseudonymization"]
        B --> C["Data audit and QA"]
        C --> D["Cleaning and consolidation"]
        D --> E["Feature engineering"]
        E --> F["Statistical analysis"]
        F --> G["Result synthesis and communication<br/>(in progress)"]
    end

    subgraph Demo["Subsequent public demo workflow"]
        H["Demo data generation"] --> I["Demo analytical base"]
        I --> J["Feature engineering"]
        J --> K["Statistical analysis"]
    end

    D -->|"clean-base input"| H
    F -.->|"public adaptation created afterward"| H
```

The project was first completed through feature engineering and statistical analysis on the institutional data. The demo dataset was generated afterward so that visitors can execute the same downstream logic with public inputs. Synthesis and technical communication of the institutional results remain in progress. See [Project architecture](docs/project_architecture.md) for the component and data-flow design.

## Analytical approach

The analysis focuses on section-level completion rates and compares outcomes by:

- delivery mode;
- class shift;
- academic program.

Methods include descriptive statistics, confidence intervals, Welch's one-way ANOVA, Games-Howell comparisons, residual checks, and partial eta-squared effect sizes. Detailed definitions and decision rules are documented in [Methodology](docs/methodology.md).

## Key findings

The public analysis produces the following patterns from the project demo data:

- Average section-level completion is slightly above one-half, with substantial variation between sections.
- Online and on-site sections have comparable completion outcomes.
- Hybrid sections show lower completion overall, with the difference concentrated descriptively in morning and afternoon schedules.
- Night sections have higher completion than morning and afternoon sections.
- Observed program-level differences are not statistically supported.

The demo dataset was calibrated so that these qualitative conclusions match those obtained from the private institutional analysis. Numerical estimates—including means, test statistics, effect sizes, confidence intervals, and p-values—differ between the two datasets. The planned technical report will present the reviewed aggregate results from the institutional analysis, while the public notebooks remain the reproducible demonstration of the same analytical workflow.

These findings are section-level associations from one academic term, not causal or student-level conclusions.

## Repository structure

```text
higher-education-outcomes-analysis/
├── data/
│   ├── raw/          # local source files
│   ├── sanitized/    # pseudonymized source tables
│   ├── clean/        # consolidated analytical base
│   ├── processed/    # private metric output
│   └── demo/         # public demo datasets and data card
├── docs/
│   ├── project_architecture.md
│   ├── methodology.md
│   └── confidentiality.md
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_metric_construction.ipynb
│   └── 04_analysis.ipynb
├── scripts/
│   └── build_sanitized_dataset.py
├── src/              # reusable pipeline and analytical modules
├── reports/
└── requirements.txt
```

## Explore the project

For a quick technical review:

1. Start with `notebooks/04_analysis.ipynb` for the questions, visualizations, and statistical results.
2. Review `notebooks/01_data_audit.ipynb` and `02_data_cleaning.ipynb` for the data-quality workflow.
3. Inspect `src/` for the reusable implementation behind the notebooks.
4. Read [Project architecture](docs/project_architecture.md) for the full component map.

To run the public downstream workflow, install the dependencies and execute the last two notebooks in order:

```bash
python -m pip install -r requirements.txt
```

1. `notebooks/03_metric_construction.ipynb`
2. `notebooks/04_analysis.ipynb`

The [demo data card](data/demo/README.md) describes the two public Parquet files. [Data confidentiality](docs/confidentiality.md) summarizes the publication boundary for the original institutional material.

## Technology

Python, pandas, NumPy, SciPy, statsmodels, Pingouin, Matplotlib, Seaborn, Jupyter, and Parquet.

## Author

**Valentín Arias** — Data Science undergraduate, Universidad Nacional Guillermo Brown

## License

The project code is distributed under the terms in [LICENSE](LICENSE).
