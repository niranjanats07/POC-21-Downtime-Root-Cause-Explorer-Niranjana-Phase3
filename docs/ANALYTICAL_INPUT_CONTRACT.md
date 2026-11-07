# Analytical Input Contract

## Project

**Project ID:** POC-21  
**PoC Title:** Downtime Root Cause Explorer

---

## Purpose

This contract defines the approved input data, required fields, reconstruction rules, validation requirements, and rejection conditions for the Post #3 analytical implementation.

The approved implementation is:

**Track A - Comparative Intelligence**

The analysis is limited to deterministic descriptive comparison of the approved synthetic canonical dataset.

---

## Approved Canonical Input

### Canonical Dataset

`data/canonical/intelligence_data.csv`

### Data Version

**1.1.0**

### Canonical Data Package

The approved canonical dataset contains:

- 60 measurement rows
- 30 distinct source incidents
- 2 measurement rows per source incident
- Synthetic records only

The two expected measurements for each complete incident are:

- `downtime_minutes`
- `failure_frequency`

No alternative dataset, manually edited dataset, replacement dataset, or external data source may be used for the approved Track A calculations.

---

## Data Archetype

The approved data archetype is:

**Incident-centric structured event records with repeated metric measurements per source incident.**

Each source incident is represented by separate canonical measurement rows.

Incident-level analytical records must therefore be reconstructed using:

`source_record_id`

---

## Required Input Fields

### Incident Reconstruction

| Field | Purpose |
|---|---|
| `source_record_id` | Reconstructs measurement rows into source incidents |

### Grouping Dimensions

| Field | Purpose |
|---|---|
| `category` | Root-cause category comparison |
| `entity_id` | Machine comparison |
| `shift` | Shift comparison |

### Metric Fields

| Field | Purpose |
|---|---|
| `metric_name` | Identifies the measurement type |
| `metric_value` | Provides the numeric measurement value |

### Evidence and Version Control

| Field | Purpose |
|---|---|
| `data_version` | Identifies the canonical data version |
| `is_synthetic` | Preserves synthetic-data evidence |

---

## Required Metric Names

The analytical implementation recognises the following metric names:

- `downtime_minutes`
- `failure_frequency`

A complete incident must contain both metrics.

---

## Incident Reconstruction Rules

The canonical dataset contains repeated measurement rows.

The analytical workflow must:

1. Read the canonical CSV using the approved source path.
2. Identify rows using `source_record_id`.
3. Group measurement rows belonging to the same source incident.
4. Identify the metric represented by `metric_name`.
5. Convert valid `metric_value` values to numeric form.
6. Construct an incident-level record containing:
   - Metadata
   - `downtime_minutes`
   - `failure_frequency`
7. Retain only complete incidents containing both required metrics.

Each complete source incident must contribute once to each applicable grouping dimension.

---

## Metric Pairing Rules

For each `source_record_id`, the analysis requires:

- One valid `downtime_minutes` value
- One valid `failure_frequency` value

The analytical calculations must not treat the two canonical measurement rows as two separate incidents.

Instead, they must be paired into one reconstructed incident.

The expected relationship is:

- 30 distinct source incidents
- 60 canonical measurement rows
- 2 required measurements per complete incident

---

## Grouping Rules

Complete incidents are grouped independently by:

1. `category`
2. `entity_id`
3. `shift`

For each grouping dimension, the analytical workflow calculates:

- Incident count
- Total downtime
- Average downtime
- Total failure frequency
- Average failure frequency

Groups are retained according to the configured minimum group size.

The current approved minimum group size is:

**1 incident**

This minimum allows all observed groups in the small synthetic demonstration dataset to be reviewed, but does not imply population representativeness.

---

## Blank or Missing Group Values

When a grouping field is blank or unavailable, the analytical implementation may represent the grouping value as:

`(blank)`

Blank grouping values must not be silently removed without evidence.

Their treatment must remain deterministic and reviewable.

---

## Data Version Rules

The implementation must read available `data_version` values from the canonical records.

The approved canonical data version is:

**1.1.0**

If exactly one data version is present, that version must be preserved in the analytical outputs.

If multiple versions or unspecified versions are detected, the implementation must record that condition and the validation process must review it.

---

## Synthetic Data Rules

All approved source incidents are synthetic.

The `is_synthetic` evidence must be preserved in the analytical workflow.

Analytical outputs must clearly state that results:

- Are based on synthetic data
- Are descriptive demonstration results
- Must not be generalized as actual industrial performance
- Must not be interpreted as causal evidence
- Must not be interpreted as predictive evidence

---

## Input Rejection Conditions

The analytical workflow must fail or be flagged for validation review when:

1. The approved canonical CSV cannot be found.
2. The canonical CSV is empty.
3. No valid source incidents can be reconstructed.
4. No incident contains both required metrics.
5. Required numeric metric values cannot be used for the required comparisons.
6. The canonical input structure prevents deterministic incident reconstruction.
7. Data-version evidence is inconsistent with the approved analytical package requirements.
8. The input is replaced with an unapproved alternative data source.

---

## Fields Not Used as Ranking Inputs

The following fields are not used as direct ranking inputs:

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

These fields may remain available for traceability or contextual evidence but are not used as predictive features.

---

## Analytical Input Scope

The approved input scope is limited to:

`data/canonical/intelligence_data.csv`

The implementation must use the approved synthetic canonical package and must not introduce:

- External datasets
- New source architectures
- Predictive training datasets
- Unsupported derived populations
- Unverified real-world operational data

---

## Evidence Preservation Requirements

The analytical workflow must preserve evidence for:

- Canonical input path
- Data version
- Source measurement-row count
- Distinct source-incident count
- Complete incidents used for analysis
- Required metric names
- Incident reconstruction logic
- Grouping dimensions
- Synthetic-data status
- Input validation outcomes

---

## Contract Decision

**APPROVED INPUT CONTRACT FOR POST #3 - TRACK A COMPARATIVE INTELLIGENCE**

The approved analytical input is the synthetic canonical dataset version **1.1.0** located at:

`data/canonical/intelligence_data.csv`

The dataset must be analysed through deterministic incident reconstruction and descriptive comparative aggregation only.
