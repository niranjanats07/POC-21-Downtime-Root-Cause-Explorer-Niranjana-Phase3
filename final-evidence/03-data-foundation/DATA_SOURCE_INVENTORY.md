# Data Source Inventory

## 1. Purpose

This report inventories the data sources used by the Phase 3 data pipeline for **PoC-21 — Downtime Root Cause Explorer**.

The purpose of this inventory is to document the supplied source, canonical representation, provenance and important limitations of the dataset used for analytical development.

## 2. Primary Source

The project uses a synthetic downtime incident dataset.

**Primary source file:**

`data/synthetic/downtime_incidents.csv`

The source contains:

- **30 synthetic downtime incidents**
- Incident-level operational attributes
- Recorded downtime duration values
- Recorded failure-frequency values
- Machine, root-cause category, shift and severity attributes

The source data is synthetic and must not be represented as verified real industrial operational data.

## 3. Source Dataset Characteristics

The supplied synthetic source dataset contains **30 incident records**.

Each incident represents a downtime event with descriptive attributes including:

- Incident identifier
- Observation date and timestamp
- Machine identifier
- Root-cause category
- Subcategory
- Shift
- Severity
- Status
- Downtime duration
- Recorded failure-frequency value

The dataset is intended for controlled data-pipeline validation and descriptive analytical demonstration.

## 4. Canonical Data Source

The canonical analytical source is:

`data/canonical/intelligence_data.csv`

It contains **60 canonical measurement records representing 30 synthetic source incidents**.

Each source incident is represented by two canonical measurement records:

1. `downtime_minutes`
2. `failure_frequency`

Therefore, the 60 canonical rows must **not** be interpreted as 60 independent incidents.

The incident-level analytical population is **30 synthetic incidents**.

## 5. Published Data Representation

The published representation is:

`data/published/intelligence_data.json`

This published file is generated from the approved canonical data package.

Analytical calculations must preserve the relationship between canonical measurement records and their corresponding source incident identifiers.

## 6. Data Version

The current canonical data package version is:

`1.1.0`

The version must remain consistent across:

- Canonical data
- Published data
- Data manifest
- Validation evidence
- Analytical outputs that identify the package version

## 7. Dataset Expansion History

The synthetic source dataset was previously expanded from **10 incidents to 30 incidents** to provide broader descriptive coverage for the Phase 3 analytical workflow.

The current approved dataset therefore contains:

- **30 synthetic source incidents**
- **60 canonical measurement records**
- **22 canonical columns**

The earlier 10-incident dataset should not be used as the current analytical basis.

## 8. Data Provenance

The canonical records preserve provenance information including:

- Source name
- Source record identifier
- Canonical record identifier
- Synthetic-data indicator
- Data version

These fields support traceability between the canonical measurements and the supplied synthetic source records.

Provenance metadata supports record-level traceability but does not independently establish the accuracy of synthetic values as real operational observations.

## 9. Synthetic Data Status

All incidents in the current dataset are synthetic.

Accordingly:

- The data supports descriptive demonstration and