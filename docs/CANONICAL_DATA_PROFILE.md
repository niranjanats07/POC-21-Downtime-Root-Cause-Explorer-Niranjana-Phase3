@'
# Canonical Data Profile

## 1. Purpose

This report documents the structural and statistical profile of the canonical dataset used for Phase 3 Post #2.

The sole analytical source is:

`data/canonical/intelligence_data.csv`

The generated machine-readable profile is:

`data-science/outputs/canonical_profile.json`

The profile is descriptive. It does not establish operational representativeness, causal relationships, or predictive readiness.

## 2. Dataset Structure

| Measure | Observed result |
|---|---:|
| Canonical measurement records | 60 |
| Columns | 22 |
| Distinct source incidents | 30 |
| Measurement metrics | 2 |
| Valid observation timestamps | 60 |
| Valid geographic coordinate pairs | 0 |
| Synthetic records | 60 |
| Canonical data version | 1.1.0 |

Each source incident is represented by two measurement records: downtime duration and failure frequency. These are measurements associated with an incident, not independent incidents.

The canonical dataset therefore contains **60 measurement records representing 30 synthetic downtime incidents**.

## 3. Field-Level Profiling

The generated profile records, for every canonical field:

- Expected field role.
- Non-null and null counts.
- Completeness percentage.
- Unique-value count.
- Top observed values.
- Representative examples.
- Leading/trailing whitespace counts.

Refer to `data-science/outputs/canonical_profile.json` for the complete field-level results.

## 4. Metric Profiling

The profile includes the following statistical measures for each metric:

- Valid and invalid numeric counts.
- Minimum and maximum.
- Mean and median.
- Sample standard deviation.
- Population standard deviation.
- Observed measurement units.

The available metrics are `downtime_minutes` and `failure_frequency`.

These statistics describe the supplied synthetic sample only. They must not be interpreted as estimates of real operational performance.

## 5. Temporal Coverage

All 60 observation timestamps were successfully parsed.

The generated profile records:

- Earliest and latest timestamps.
- Number of distinct observation dates.
- Observation counts by date.
- Gaps between observed dates.
- Timezone-aware and timezone-naive timestamp counts.
- Timezone consistency assessment.

The dataset provides incident observations across the available synthetic observation period. It does not establish a sufficiently long representative operational time series for trend forecasting or seasonality analysis.

## 6. Uniqueness and Entity Relationships

The profile records:

- Unique canonical record identifiers.
- Duplicate record identifiers.
- Distinct source incident identifiers.
- Repeated source incident measurement records.
- Distinct entity-to-incident relationships.

The 60 measurement records represent 30 source incidents. Analyses must account for this relationship and must not treat the two metric records associated with an incident as separate incidents.

## 7. Categorical Coverage

Categorical distributions are profiled for the available record, entity, category, subcategory, status, stage, shift, severity and metric fields.

The generated profile also flags:

- Rare category values below the configured 10% threshold.
- Near-constant fields with a dominant value at or above the configured 95% threshold.
- Dominant values and their proportions.

These are screening indicators, not automatic evidence of data defects.

## 8. Geographic Coverage

No complete valid latitude/longitude pairs are present in the canonical dataset.

Consequently:

- Geographic distribution cannot be assessed.
- Geographic clustering cannot be assessed.
- Location-based comparisons are unsupported.

Missing geographic information must not be fabricated or inferred.

## 9. Text Profiling

The profile records:

- Number of non-empty text values.
- Minimum, average and maximum text lengths.
- Leading/trailing whitespace.
- A possible-truncation review indicator.

The truncation indicator is a screening heuristic, not confirmation that text has been truncated.

## 10. Provenance and Version Coverage

The generated profile records:

- Source-name distribution.
- Distinct source incident count.
- Synthetic/non-synthetic value distribution.
- Canonical data-version distribution.

All records in the supplied sample are synthetic and use canonical data version `1.1.0`. They must not be represented as verified real operational observations.

## 11. Dataset Regeneration and Expansion History

The synthetic source dataset was previously expanded from **10 incidents to 30 incidents** to provide broader descriptive coverage for the Phase 3 analytical workflow.

The current canonical package is based on those **30 synthetic downtime incidents** and contains **60 canonical measurement records**, with two measurement records associated with each source incident.

This was an earlier controlled synthetic-data expansion. The current Post #2 evidence correction aligns validation reports and documentation with the already-expanded dataset; it does not claim the creation of a new real operational dataset.

All records remain synthetic and the expansion does not establish representativeness of actual industrial downtime.

## 12. Profiling Limitations

The profile is based exclusively on the canonical CSV.

The following limitations remain:

- Synthetic records do not establish real operational behaviour.
- Thirty synthetic incidents provide broader descriptive coverage than the earlier 10-incident dataset, but do not establish real-world operational representativeness.
- Two measurement records per incident are not independent incidents.
- Missing coordinates prevent geographic analysis.
- Missing optional fields remain missing.
- A profile cannot independently establish source accuracy.
- Text-length heuristics cannot confirm source truncation.
- Statistical distributions from this synthetic sample cannot establish population-level patterns.

## 13. Conclusion

The canonical CSV has been successfully profiled across structure, completeness, numeric metrics, temporal coverage, uniqueness, categorical coverage, geography, text and provenance.

The resulting profile supports controlled data validation and descriptive assessment of the supplied **30 synthetic incidents represented by 60 canonical measurement records**.

The dataset is approved for **Track A — Comparative Intelligence** using deterministic descriptive calculations.

It does not establish readiness for operational generalization, predictive modelling, forecasting, anomaly detection or unsupported causal conclusions.
'@ | Set-Content .\docs\CANONICAL_DATA_PROFILE.md -Encoding UTF8