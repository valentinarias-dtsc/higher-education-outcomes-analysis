# Data Confidentiality

Version 1.0 does not distribute the original institutional records. Public materials include the implementation, documented analytical decisions, reviewed aggregate outputs, and a synthetic analytical dataset that supports the final two notebook stages.

## Pseudonymization

Campus names, course names and codes, and program names and codes are replaced before the audit stage. The mappings and original identifiers remain private.

Pseudonymization makes the workflow suitable for technical review, but it does not turn the original or intermediate institutional datasets into public artifacts.

## Published data

The committed demo dataset retains pseudonymized section structure and operational fields while replacing the five academic-outcome counts with generated values. It begins at the analytical-base stage; it is not a synthetic copy of the three raw source tables. Its exact field provenance and intended use are documented in the [demo data card](../data/demo/README.md).

The original source files, pseudonymization mappings, sanitized tables, clean institutional base, processed institutional data, and original row-level outcomes are excluded from version control.

## Use of results

Results produced by the public notebooks describe the demo data. They demonstrate the analytical approach and should be distinguished from any separately reviewed institutional findings.

The project code is published under the repository license; that license does not grant rights over the original institutional data.
