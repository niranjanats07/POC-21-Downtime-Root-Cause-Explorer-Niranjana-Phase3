# Analytical Track Execution Plan

## Project

**Project ID:** POC-21  
**PoC Title:** Downtime Root Cause Explorer

---

## Target User

Users reviewing the approved synthetic downtime investigation dataset and identifying groups that warrant closer descriptive review.

---

## Canonical Data Source

`data/canonical/intelligence_data.csv`

No alternative dataset, manually edited dataset, replacement dataset, or external source will be used for the Track A analytical calculations.

---

## Canonical Data Version

**1.1.0**

The analysis must use the approved canonical package version represented in the canonical data records.

---

## Confirmed Data Archetype

Incident-centric structured event records with repeated metric measurements per source incident.

The canonical dataset contains two measurement rows for each source incident:

- `downtime_minutes`
- `failure_frequency`

Analytical comparisons reconstruct incident-level metric pairs using `source_record_id`.

The approved dataset contains:

- 60 canonical measurement rows
- 30 distinct source incidents
- 2 measurement rows per incident
- Synthetic records only

---

## Primary Analytical Question

Which recorded root-cause categories, machines, and shifts have the highest observed downtime totals and failure-frequency values within the approved synthetic incident dataset?

---

## Decision to Be Supported

Identify the highest-observed groups for closer descriptive review within the synthetic downtime investigation demonstration.

Results are prioritised descriptive observations only and must not be interpreted as:

- Real-world operational performance
- Causal evidence
- Predictive outcomes
- Population-level conclusions

---

## Approved Primary Analytical Track

**Track A - Comparative Intelligence**

---

## Supporting Track

No supporting analytical track is implemented in this Post #3 package.

**Track H - Text and Theme Intelligence** was conditionally supported for controlled exploratory review during Post #2, but it is outside the approved primary implementation scope for this submission.

---

## Fields to Be Used

### Grouping Dimensions

- `category`
- `entity_id`
- `shift`

### Metrics

- `metric_name`
- `metric_value`

### Incident Reconstruction

- `source_record_id`

### Version and Evidence Control

- `data_version`
- `is_synthetic`

---

## Fields Excluded from Analytical Calculations

The following fields are not used as ranking inputs:

- `record_id`
- `observed_at`
- `related_entity_id`
- `entity_name`
- `subcategory`
- `status`
- `stage`
- `metric_unit`
- `text_value`
- `latitude`
- `longitude`
- `source_name`
- `severity`

Identifiers are used only for incident reconstruction, grouping, version verification, or evidence traceability and are not treated as predictive features.

---

## Analytical Baseline

The analytical baseline is a descriptive group comparison using:

- Incident count
- Total downtime
- Average downtime
- Total failure frequency
- Average failure frequency

Groups are ranked primarily by descending total downtime.

This baseline establishes the direct descriptive comparison against which the Track A comparative intelligence output is validated.

---

## Selected Analytical Method

**Deterministic comparative aggregation**

The method:

1. Loads the approved canonical CSV.
2. Reads the canonical measurement records.
3. Identifies the available data version.
4. Reconstructs incidents using `source_record_id`.
5. Requires both `downtime_minutes` and `failure_frequency` for a complete incident.
6. Groups complete incidents by:
   - Root-cause category
   - Machine
   - Shift
7. Calculates:
   - Incident count
   - Total downtime
   - Average downtime
   - Total failure frequency
   - Average failure frequency
8. Applies deterministic ranking.
9. Records minimum group-size evidence.
10. Generates structured intelligence outputs.

No predictive modelling, causal modelling, simulation, anomaly modelling, or unsupported inference is included.

---

## Ranking Method

Groups are ranked using the following deterministic order:

1. Descending total downtime.
2. Descending incident count when downtime totals are tied.
3. Ascending group name for deterministic tie handling.

Each resulting group receives a `rank_by_total_downtime` value.

---

## Minimum Group Size

**1 incident**

All groups meeting the minimum group size are retained because the approved dataset contains only 30 synthetic incidents and all observed groups are relevant to descriptive review.

Small-group sensitivity must be documented in the validation and weak-case review.

A group satisfying the minimum size requirement does not imply that the group is representative of a wider operational population.

---

## Validation Approach

Track A validation will include:

- Independent recalculation of selected group totals.
- Verification that complete incidents are included exactly once within each grouping dimension.
- Verification of incident reconstruction using `source_record_id`.
- Verification of downtime and failure-frequency metric pairing.
- Minimum group-size checks.
- Deterministic tie-handling checks.
- Ranking stability review.
- Sensitivity review for small groups.
- Missing-group and blank-value review.
- Baseline comparison.
- Data-version verification.
- Synthetic-data limitation verification.

---

## Expected Structured Outputs

The analytical package will generate:

- `data-science/outputs/intelligence_results.json`
- `data-science/outputs/intelligence_summary.json`
- `data-science/outputs/validation_metrics.json`
- `data-science/outputs/weak_case_review.json`

---

## Execution Scripts

The Post #3 analytical workflow is supported by:

- `data-science/scripts/run_comparative_intelligence.py`
- `data-science/scripts/run_analytical_track.py`
- `data-science/scripts/validate_analytical_track.py`
- `data-science/scripts/export_intelligence_results.py`

Track-specific comparative logic is maintained under:

- `data-science/scripts/track-specific/comparative_intelligence.py`

---

## Notebook Evidence

The analytical development and validation notebook is:

`data-science/notebooks/02_analytical_track_development_and_validation.ipynb`

The notebook must provide reproducible evidence of the approved Track A calculations and validation results.

---

## Analytical Scope

This implementation is limited to the approved synthetic canonical dataset.

The analysis supports descriptive comparison of observed groups only.

Results must not be interpreted as evidence of:

- Actual industrial performance
- Root-cause causality
- Future downtime prediction
- Population representativeness
- Geographic patterns
- Lifecycle-stage progression

---

## Known Limitations

The analytical results are subject to the following limitations:

- All 30 source incidents are synthetic.
- Only 4 machines are represented.
- The observation period is limited.
- Sampling methodology and population inclusion probabilities are not established.
- The wider machine population is unknown.
- Geographic coordinates are unavailable.
- Lifecycle-stage information is unavailable.
- Related-entity information is unavailable.
- Source accuracy is not independently verified.
- Small group sizes may affect ranking stability.

Therefore, results must remain limited to descriptive comparison within the approved synthetic demonstration dataset.

---

## Evidence Preservation Requirements

The Post #3 workflow must preserve:

- Canonical source path
- Data version
- Measurement-row count
- Distinct incident count
- Complete incident count used for comparison
- Group-level calculations
- Ranking logic
- Validation evidence
- Weak-case evidence
- Synthetic-data limitations

---

## Final Execution Decision

**DATA READY FOR ANALYTICAL TRACK DEVELOPMENT - TRACK A COMPARATIVE INTELLIGENCE**

The approved implementation is deterministic descriptive comparative analysis using the canonical synthetic dataset version **1.1.0**.

No new data architecture, predictive modelling, or unsupported causal conclusions will be introduced.
