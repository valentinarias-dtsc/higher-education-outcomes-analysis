# Project Limitations

Version 1.0 is complete within its defined scope: a section-level analysis of academic completion during 2024 C1 at one institution. The following boundaries guide interpretation without invalidating the implemented workflow or its findings.

## Analytical boundaries

- **Observational design.** The reported relationships are associations. Delivery mode, shift, and academic program were not randomly assigned, so the analysis does not establish causal effects.
- **Course-section unit.** Each row aggregates student outcomes within a course section. The data do not support individual risk estimates or adjustment for student characteristics, prior achievement, or longitudinal trajectories.
- **Single academic term and institution.** Results describe 2024 C1 in the analyzed setting; temporal stability and external generalizability were not evaluated.
- **Possible dependence among sections.** Sections may share courses, academic programs, campuses, instructors, or students. Version 1.0 uses one-factor section-level comparisons and does not model clustering.
- **Unbalanced groups and a bounded outcome.** Welch's ANOVA and Games–Howell comparisons address unequal variances and group sizes, but sparse groups and completion rates at zero or one still affect precision and motivate sensitivity analysis in later versions.
- **Integration exclusions.** Six of the 303 Enrollment sections (2.0%) were excluded because no reliable Offering metadata was available. Their exclusion is unlikely to materially affect the overall findings but slightly reduces the analytical coverage of the original dataset.
- **Descriptive joint pattern.** The shift × delivery-mode heatmap summarizes cell means and counts; it is not a formal interaction test.

## Public reproducibility boundary

The repository publishes synthetic analytical-base and processed datasets, not synthetic raw source tables. Public users can run metric construction and statistical analysis from committed data, while sanitization, audit, and cleaning require private inputs. The complete implementation remains inspectable, and [Version notes and roadmap](version_notes.md) identifies a synthetic raw-data layer as the principal future reproducibility extension.

The [Technical report](../reports/technical_report.md) incorporates these boundaries into the interpretation of each result. They define the appropriate use of Version 1.0 rather than indicating an unfinished analysis.
