# Higher Education Outcomes Analysis

## Executive Summary

### 1. Project Overview

Version 1.0 investigates how academic completion outcomes vary across course sections, academic programs, delivery modes, and class shifts. It addresses a common analytics challenge: turning fragmented institutional records into a reliable analytical dataset before drawing conclusions from them. The study covers **2024 C1**, one academic term at one institution, and uses the **course section** as its unit of analysis rather than the individual student.

The final analytical base contains **297 course sections**, representing **131 courses** and **13 academic programs**. Each section combines aggregate enrollment outcomes with consistent operational information such as delivery mode, shift, schedule, workload, and campus. The central metric, `completion_rate`, is the share of enrolled students whose final status was either promoted completion or regular completion.

The repository documents a complete analytical workflow, covering data preparation, metric construction, statistical inference, and technical reporting of findings. Together, these components illustrate an end-to-end Data Analytics case study rather than an isolated analysis notebook.

### 2. Analytical Approach

The analytical workflow integrates three sources: Enrollment for section-level enrollment and outcome counts, Offering for canonical operational metadata, and Programs for academic program descriptors. The implemented sequence is:

**pseudonymization and sanitization → data audit → cleaning and standardization → source integration → metric construction → statistical analysis → communication of findings**

The audit identified substantial missingness in Enrollment's operational fields, inconsistent categorical labels, four minor enrollment-total discrepancies, and six Enrollment sections without matching Offering records. The pipeline standardized categories, reconciled eligible totals, validated merge relationships, and excluded the six unmatched sections because reliable operational metadata was unavailable. Completion rates were then evaluated using descriptive statistics, confidence intervals, Welch's ANOVA, Games–Howell comparisons after significant omnibus tests, and partial eta-squared effect sizes. A public synthetic dataset preserves the pseudonymized section structure and supports reproducible execution of the final metric-construction and analysis stages.

### 3. Key Findings

| Dimension | Main result | Statistical conclusion |
|---|---|---|
| Delivery mode | Hybrid had the lowest mean completion rate | Significant overall difference; small effect |
| Shift | Night had the highest mean completion rate | Significant overall difference; small effect |
| Academic program | Program means varied descriptively | No statistically significant overall difference |

**Delivery mode was associated with completion, but the effect was small.** Mean completion was 0.589 for On-site, 0.590 for Online, and 0.493 for Hybrid sections. Welch's ANOVA found an overall difference, *F*(2, 91.31) = 3.769, *p* = 0.0267, partial η² = 0.028. Games–Howell comparisons showed that Hybrid was significantly lower than On-site (*p* = 0.0232). Hybrid was not statistically distinguishable from Online (*p* = 0.0783), despite a similar observed mean gap, and On-site and Online were nearly identical (*p* = 0.9992).

![Institutional completion rates by delivery mode](figures/delivery_violin.png)

*Figure 1. Distribution of institutional section-level completion rates by delivery mode; internal lines indicate quartiles and the median.*

**Night sections showed the highest average completion.** Mean completion was 0.606 for Night, compared with 0.529 for Morning and 0.508 for Afternoon. The overall shift result was significant, *F*(2, 119.15) = 5.583, *p* = 0.0048, partial η² = 0.036. Pairwise comparisons supported differences between Night and both Morning and Afternoon, while Morning and Afternoon did not differ significantly. As with delivery mode, the effect was small: shift identifies a supported pattern but explains only a limited share of total section-level variation.

**The analysis did not find statistically significant evidence of overall differences across academic programs.** For the 12 programs with at least ten sections, Welch's ANOVA produced *F*(11, 91.66) = 1.213, *p* = 0.2901, partial η² = 0.043. Visible differences in program means therefore should not be interpreted as a definitive performance ranking or as proof that programs are equivalent.

**The combined shift-by-delivery view adds a useful descriptive hypothesis.** Hybrid completion was lowest in Morning and Afternoon cells and closer to other delivery modes at Night. Because the repository does not implement a formal interaction model and some cells are small, this pattern is presented as exploratory rather than as a tested interaction effect.

Together, the results show analytical selectivity rather than a simple hierarchy: delivery mode and shift have statistically supported associations with completion, both with small effects, while academic program does not show a supported overall difference in the current data.

### 4. Technical Value

The project demonstrates the ability to convert imperfect, multi-source records into a validated analytical product. The repository provides evidence of data-contract design, missingness and integrity auditing, deterministic pseudonymization, categorical normalization, source reconciliation, validated joins, metric engineering, statistical inference under unequal variances and unbalanced groups, and report-ready visualization.

Reusable Python modules separate audit, cleaning, validation, metric, and reporting logic from notebook narration. Generated tables preserve exact statistical results in a presentation-ready format, while the synthetic-data generator creates a safe public execution path without publishing original institutional records. The technical report and supporting documentation then translate that implementation into clear, appropriately qualified findings. For a recruiter or analytics lead, the project demonstrates both hands-on analytical execution and the judgment required to communicate what the evidence does—and does not—support.

### 5. Deliverables and Repository Navigation

- [README](../README.md): project orientation, workflow, and headline findings.
- [Technical report](technical_report.md): complete account of data preparation, methodology, results, and limitations.
- [Notebooks](../notebooks/): executed audit, cleaning, metric-construction, and analysis workflow.
- [Source modules](../src/): reusable pipeline and analytical implementation.
- [Public demo data](../data/demo/README.md): data card and reproducible analytical inputs.
- [Methodology and architecture](../docs/): analytical decisions, system design, and confidentiality boundary.
- [Version notes and roadmap](../docs/version_notes.md): implemented Version 1.0 scope and prioritized extensions.
- [`reports/figures/`](../reports/figures/) and [`reports/tables/`](../reports/tables/): publication-ready visuals and statistical summaries.

The original institutional data are not publicly distributed. The repository instead provides a publishable synthetic demo dataset, inspectable code, and documented methods for reproducing the public analytical stages.

### 6. Closing Assessment

Higher Education Outcomes Analysis Version 1.0 is a complete end-to-end Data Analytics case study. It begins with imperfect source data, establishes a defensible analytical base, applies statistical methods suited to the observed group structure, and communicates evidence-based findings without overstating their implications. Although its conclusions are observational, section-level, and limited to a single academic term, the repository demonstrates a complete analytical workflow spanning data preparation, statistical inference, reproducible analytical practices, and technical communication.
