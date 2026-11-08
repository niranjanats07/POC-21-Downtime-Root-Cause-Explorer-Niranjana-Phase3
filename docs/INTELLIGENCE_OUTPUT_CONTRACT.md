# Intelligence Output Contract

## Project

**Project ID:** POC-21
**PoC Title:** Downtime Root Cause Explorer
**Approved Primary Analytical Track:** Track A — Comparative Intelligence
**Data Version:** 1.1.0
**Method Version:** 1.0.0

---

## Purpose

This document defines the standard output contract for the Phase 3 analytical intelligence package.

The intelligence output is generated from the approved canonical data source:

`/data/canonical/intelligence_data.csv`

The output contains deterministic comparative findings produced by Track A — Comparative Intelligence.

The output is intended for future Data Intelligence page integration and must remain reproducible, explainable, and versioned.

---

## Output File

The primary analytical output file is:

`/data-science/outputs/intelligence_results.json`

The final exported structure is a **flat JSON array of standardized analytical findings**.

The output does **not** use the older grouped-results structure.

Each item in the array represents one independently identifiable analytical finding.

For the current approved dataset and Track A implementation, the export contains **11 standardized findings**.

---

## Required Top-Level Structure

The `intelligence_results.json` file must have the following structure:

```json
[
  {
    "result_id": "RES-0001",
    "result_type": "comparative_group_ranking",
    "record_id": null,
    "entity_id": null,
    "group_key": "example_group",
    "period_start": null,
    "period_end": null,
    "metric_name": "total_downtime_minutes",
    "result_value": 0.0,
    "result_unit": "minutes",
    "result_category": "root_cause_category",
    "priority_rank": 1,
    "finding": "Example deterministic comparative finding.",
    "evidence": [],
    "method_version": "1.0.0",
    "data_version": "1.1.0",
    "generated_at": "ISO-8601 UTC timestamp",
    "quality_status": "validated",
    "limitation": "Descriptive result based on the approved synthetic canonical dataset."
  }
]
```

The exported JSON must be a **valid JSON array**.

---

## Standard Result Fields

Each exported analytical finding must use the following standardized fields.

| Field | Required | Description |
|---|---|---|
| `result_id` | Yes | Unique identifier for the analytical result |
| `result_type` | Yes | Type of analytical result |
| `record_id` | Yes | Source record identifier when applicable; otherwise `null` |
| `entity_id` | Yes | Entity identifier when applicable; otherwise `null` |
| `group_key` | Yes | Group or comparison value represented by the finding |
| `period_start` | Yes | Start period when applicable; otherwise `null` |
| `period_end` | Yes | End period when applicable; otherwise `null` |
| `metric_name` | Yes | Name of the measured metric |
| `result_value` | Yes | Numeric value of the analytical metric |
| `result_unit` | Yes | Unit of the result |
| `result_category` | Yes | Result classification or category |
| `priority_rank` | Yes | Deterministic comparative rank when applicable; otherwise `null` |
| `finding` | Yes | Human-readable deterministic finding |
| `evidence` | Yes | Structured evidence supporting the finding |
| `method_version` | Yes | Analytical method version |
| `data_version` | Yes | Canonical data version |
| `generated_at` | Yes | Generation timestamp |
| `quality_status` | Yes | Validation status of the result |
| `limitation` | Yes | Applicable analytical limitation |

Fields that are not applicable must remain present and use `null` where appropriate.

---

## Approved Comparison Dimensions

Track A compares the approved canonical dataset across the following dimensions:

1. Root-cause category
2. Machine
3. Shift

The approved comparative metrics include:

- Incident count
- Total downtime minutes
- Average downtime minutes
- Total failure frequency
- Average failure frequency
- Comparative ranking by total downtime

---

## Minimum Group-Size Rule

The minimum group size is:

**3 incidents**

Each comparison group must be evaluated against this rule.

The exported analytical result must preserve sufficient evidence to determine whether the observed group meets the minimum group-size requirement.

Groups below the minimum threshold must not be presented as equally stable comparative findings without an appropriate limitation or qualification.

The current validation process must independently check this rule against the canonical dataset.

---

## Flat Export Requirement

The final `intelligence_results.json` output must be validated as a **flat array of analytical result objects**.

The validator must not assume or require an older grouped structure.

The validator must independently:

1. Load the approved canonical CSV.
2. Recalculate the relevant comparative values.
3. Load the actual exported `intelligence_results.json`.
4. Confirm that the exported file is a valid flat array.
5. Confirm the expected result count.
6. Validate required fields for every exported result.
7. Confirm data and method versions.
8. Confirm result values against independently calculated canonical results.
9. Confirm ranking consistency.
10. Confirm the minimum group-size rule.
11. Report `PASS` only when all required checks succeed.

---

## Validation Status

A result may use:

`"quality_status": "validated"`

only when the exported result has passed the required Track A validation checks.

The overall validation status is:

- `PASS` when all required checks pass.
- `FAIL` when any required validation check fails.

A `PASS` result must be based on validation of the **actual exported JSON file**, not only internal intermediate calculations.

---

## Evidence Requirements

Each finding must contain deterministic evidence derived from the approved canonical dataset.

Evidence may include:

- Comparison dimension
- Group name
- Incident count
- Downtime totals
- Downtime averages
- Failure-frequency totals
- Failure-frequency averages
- Ranking information
- Minimum group-size status

The output must not contain unsupported or LLM-generated numerical findings.

---

## Version Requirements

Every exported result must include:

**Data Version:** `1.1.0`
**Method Version:** `1.0.0`

The validator must confirm that exported results use the approved canonical data version.

Changes to the analytical method, comparison logic, ranking rules, or other material method parameters require a method-version review.

---

## Important Limitations

The intelligence outputs are subject to the following limitations:

- All source incidents are synthetic.
- Results are descriptive demonstration outputs.
- Results are not representative of actual industrial performance.
- Results do not establish causal relationships.
- Results are not predictive evidence.
- Comparative rankings may change when additional observations become available.
- Small groups may have reduced ranking stability.

---

## Unsupported Uses

The intelligence outputs must not be used as:

- Predictive evidence
- Causal evidence
- A probability of future downtime
- A guarantee of future failure outcomes
- Evidence of real-world industrial performance beyond the approved synthetic dataset

---

## Reproducibility Requirement

The analytical output must be reproducible through the reusable analytical scripts.

The required execution flow is:

1. Load the approved canonical CSV.
2. Verify the approved data version.
3. Validate required analytical inputs.
4. Apply approved Track A comparative calculations.
5. Generate the flat standardized intelligence-results export.
6. Independently validate the actual exported results against canonical calculations.
7. Generate validation metrics.
8. Generate weak-case review evidence.
9. Export the final intelligence summary.

No hidden manual calculation or alternate dataset may be required.


