# Limitations

## 1. Scope of the Data

Version 1.0 covers a single institution and one academic term: the first semester of 2024.

The findings therefore describe a specific operational context and should not be generalized to:

- other institutions;
- other academic periods;
- long-term student trajectories;
- broader higher-education populations.

The analysis is cross-sectional rather than longitudinal.

---

## 2. Unit of Analysis

The unit of analysis is the **course section**, not the individual student.

This aggregation prevents the analysis from accounting for:

- prior academic performance;
- socioeconomic background;
- age or employment status;
- repeated enrollment;
- student-level persistence;
- within-section heterogeneity.

As a result, the findings characterize section-level outcomes only.

---

## 3. Observational Design

The project uses observational institutional data.

Differences associated with delivery mode, shift, or program should therefore be interpreted as **associations**, not causal effects.

Unobserved factors may explain part of the observed variation, including:

- course difficulty;
- instructor practices;
- curriculum design;
- student composition;
- assessment policies;
- scheduling constraints.

---

## 4. Dependence Between Observations

The statistical analyses treat course sections as independent observations.

This assumption may be imperfect because some sections can share:

- the same course;
- the same program;
- the same instructor;
- similar student populations;
- common institutional conditions.

Possible dependence may affect standard errors and significance tests.

Multilevel or clustered models would provide a stronger framework if the required identifiers and repeated-period data were available.

---

## 5. Bounded Outcome Variables

Completion rates are restricted to the interval `[0, 1]`.

Although the selected methods are reasonably robust for the observed sample sizes, bounded outcomes may exhibit:

- skewness;
- non-constant variance;
- concentration near the limits.

Alternative approaches such as beta regression, generalized linear models, bootstrap inference, or permutation methods could be evaluated in future versions.

---

## 6. Group Imbalance and Statistical Power

Some analytical groups contain substantially fewer course sections than others.

Unequal group sizes can reduce precision and make smaller groups more sensitive to extreme observations.

Welch's ANOVA and Games–Howell comparisons were used to reduce sensitivity to unequal variances and unbalanced samples, but they do not eliminate limitations caused by sparse groups.

A non-significant result should not be interpreted as proof that no difference exists.

---

## 7. Multiple Comparisons

The project evaluates several group-based research questions.

Although post hoc procedures control error rates within individual comparisons, the broader analytical workflow still involves multiple inferential decisions.

Reported p-values should therefore be interpreted together with:

- confidence intervals;
- effect sizes;
- descriptive patterns;
- practical relevance.

---

## 8. Data Quality and Source Integration

The analytical base is constructed from three source tables with different purposes and levels of completeness.

The offering table is used to supplement operational metadata missing from the primary enrollment table.

Although the audit and cleaning workflow includes consistency checks, residual limitations may remain due to:

- incomplete source records;
- ambiguous matches;
- undocumented source-system conventions;
- differences in update timing across tables.

---

## 9. Confidentiality and Reproducibility

The original institutional datasets and their direct derivatives cannot be distributed.

As a result:

- the pseudonymization, audit, and cleaning stages are visible but not publicly executable;
- public execution begins with a synthetic demo analytical base;
- demo outputs reproduce the workflow and qualitative analytical patterns, not exact institutional results.

The public synthetic dataset should not be used to make claims about the institution.

See [`confidentiality.md`](confidentiality.md) for the full publication boundary.

---

## 10. Interpretation of Results

The conclusions are conditional on:

- the available variables;
- the selected metrics;
- the statistical procedures;
- the assumptions of those procedures;
- the current version of the cleaned analytical base.

Future methodological changes may alter estimates, uncertainty intervals, or levels of statistical significance without necessarily changing the broader qualitative conclusions.

---

## 11. Future Improvements

Potential extensions include:

- additional academic terms;
- longitudinal student-level data;
- multilevel models;
- clustered standard errors;
- bootstrap sensitivity analysis;
- beta regression or generalized linear models;
- explicit control for course and instructor effects;
- richer covariates describing student and section composition.
