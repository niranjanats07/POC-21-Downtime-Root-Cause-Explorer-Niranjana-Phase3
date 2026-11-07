# Intelligence Output Contract

## Project

**Project ID:** POC-21  
**PoC Title:** Downtime Root Cause Explorer

---

## Purpose

This document defines the intelligence output contract for Phase 3 Post #3.

The approved analytical implementation is:

**Track A - Comparative Intelligence**

All calculations use only the approved canonical dataset:

`data/canonical/intelligence_data.csv`

**Data Version:** `1.1.0`  
**Method Version:** `1.0.0`

The intelligence outputs are prepared for future integration. This Post #3 package does not implement a Data Intelligence page, production analytical API, chatbot, or dashboard integration.

---

## 1. Required Intelligence Output Files

The Post #3 analytical package generates:

- `data-science/outputs/intelligence_results.json`
- `data-science/outputs/intelligence_summary.json`
- `data-science/outputs/validation_metrics.json`
- `data-science/outputs/weak_case_review.json`

---

## 2. Intelligence Results Contract

The primary detailed output is:

`data-science/outputs/intelligence_results.json`

The output uses a **structured grouped-comparison format** for the approved Track A implementation.

### Required top-level metadata

The output must preserve:

- `project_id`
- `poc_title`
- `analytical_track`
- `data_version`
- `method_version`
- `source_file`
- `source_measurement_rows`
- `distinct_source_incidents`
- `complete_incidents_used_for_comparison`
- `minimum_group_size`
- `ranking_method`
- `calculation_scope`
- `synthetic_data_limitation`
- `overall_metrics`
- `comparisons`

### Overall metrics

`overall_metrics` must provide descriptive totals for the approved complete incidents, including:

- `incident_count`
- `total_downtime_minutes`
- `average_downtime_minutes`
- `total_failure_frequency`
- `average_failure_frequency`

### Comparison dimensions

`comparisons` must contain the approved Track A grouping dimensions:

- `root_cause_category`
- `machine`
- `shift`

Each comparison dimension contains one or more group-level results.

### Required group-level fields

Each group-level result must contain:

- `group`
- `incident_count`
- `downtime_measurement_count`
- `failure_frequency_measurement_count`
- `total_downtime_minutes`
- `average_downtime_minutes`
- `total_failure_frequency`
- `average_failure_frequency`
- `meets_minimum_group_size`
- `rank_by_total_downtime`

This grouped structure is the approved contract for the current deterministic Track A implementation.

---

## 3. Track A Comparative Result Types

The approved Track A implementation supports deterministic descriptive comparison across:

- Root-cause categories
- Machines
- Shifts

The comparative calculations include:

- Incident counts
- Total downtime
- Average downtime
- Total failure frequency
- Average failure frequency
- Deterministic rankings

The approved current implementation does not require unsupported predictive, causal, or externally inferred results.

Where additional descriptive measures are explicitly implemented and validated, they must be documented and reproducibly generated from the approved canonical dataset.

All outputs remain descriptive observations and do not establish causal relationships.

---

## 4. Ranking Contract

The approved deterministic ranking method is:

1. Descending total downtime.
2. Descending incident count when total downtime is tied.
3. Ascending group name for deterministic tie handling.

The resulting rank is stored as:

`rank_by_total_downtime`

The ranking describes only the approved observed synthetic dataset.

---

## 5. Minimum Group Size

The approved minimum group size is:

**1 incident**

All observed groups meeting this threshold are retained because the approved dataset contains only 30 synthetic incidents and all observed groups are relevant to descriptive review.

The threshold of 1 is acceptable for this synthetic demonstration because the purpose is to preserve all observed groups for deterministic descriptive comparison, not to estimate a wider population or make statistically generalizable claims.

A group meeting the minimum size requirement must not be interpreted as representative of a wider operational population.

Small-group sensitivity and ranking stability are reviewed separately in:

- `data-science/outputs/weak_case_review.json`
- `docs/WEAK_CASE_AND_LIMITATION_REVIEW.md`
- `docs/ANALYTICAL_VALIDATION_REPORT.md`

---

## 6. Missing Groups and Blank Values

Track A reconstructs complete incidents using `source_record_id`.

A complete incident requires both:
