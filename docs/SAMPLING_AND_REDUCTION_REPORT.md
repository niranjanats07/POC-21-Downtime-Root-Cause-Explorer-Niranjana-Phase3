# Sampling and Reduction Report

## Original Source

`data/synthetic/downtime_incidents.csv` — synthetic local CSV used by the
existing Phase 2 backend loader.

## Original Size

1,202 bytes.

## Original Record Count

10 records.

## Original Column Count

11 columns.

## Selected Sampling Method

Full-source retention with coverage review. The complete source contains only
10 records, so it is already below the program's default 10,000-row limit.
No record reduction is needed or performed.

## Random Seed

42 is the configured program seed. It is not applied because the source is
retained in full and no random selection takes place.

## Stratification Fields

Coverage was reviewed across `root_cause`, `sub_cause`, `severity`, `status`,
`shift`, `machine_id` and `incident_date`. All source records are retained.

## Date-Coverage Method

All 10 consecutive dates from 2026-01-05 through 2026-01-14 are retained.

## Rare-Record Preservation

All records are retained, including the single Maintenance root-cause record,
the single Low-severity/Operational examples where present, and all machine,
shift and sub-cause combinations.

## Removed Fields

No source columns are removed from `source_sample.csv`. In the canonical
representation, source attributes not in the universal schema are retained
as documented domain-specific columns (`shift`, `severity`). The original
source remains available in the source sample.

## Removed Records

0.

## Text Truncation

No description exceeds 500 characters. The standardization script enforces
the 500-character maximum.

## Sensitive-Data Removal

No personal or restricted data was identified in the supplied synthetic
source. No rows or fields were removed for sensitivity.

## Final Source Sample

- **Path:** `data/source-sample/source_sample.csv`
- **Size:** 1,202 bytes
- **Record count:** 10
- **Column count:** 11

## Representativeness Checks

- Root-cause categories retained: Electrical, Maintenance, Mechanical,
  Operational.
- Severity values retained: High, Low, Medium.
- Shift values retained: Evening, Morning, Night.
- Status values retained: Closed.
- Machines retained: MCH-01, MCH-02, MCH-03, MCH-04.
- Full date range retained: 2026-01-05 to 2026-01-14.
- All 10 source incidents retained.

## Known Sampling Limitations

This is a small synthetic demonstration dataset. It does not establish
statistical representativeness of real manufacturing operations. Status is
constant, the time range is short, and no geographic attributes exist.

## Reproduction Command

```powershell
py scripts/data_pipeline/extract_data.py
py scripts/data_pipeline/sample_data.py
```
