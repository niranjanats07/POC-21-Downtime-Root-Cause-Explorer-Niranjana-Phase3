# POC-21 Canonical Data Package

This directory contains the controlled Phase 3 Post #1 data package for the
Downtime Root Cause Explorer.

## Source of truth

`data/canonical/intelligence_data.csv` is the canonical source of truth.
All later Phase 3 analysis must use this file or outputs generated directly
from it after the package is reviewed and approved.

## Included files

- `source-sample/source_sample.csv` — exact local snapshot of the existing
  synthetic source file.
- `canonical/intelligence_data.csv` — standardized measurement-level records.
- `published/intelligence_data.json` — generated JSON representation of the
  canonical CSV.
- `manifest.json` and `schema.json` — package metadata and field contract.
- `quality/` — reproducible profile, sampling note and validation evidence.

## Source and sampling decision

The Phase 2 application uses `data/synthetic/downtime_incidents.csv`.
The supplied source contains 10 records and 11 columns (1,202 bytes).
It is already far below the 10,000-row and 5 MB limits, so all records are
retained; no rows are dropped and no random sample is necessary. Seed 42 is
recorded for reproducibility policy, but is not applied because no random
sampling occurs.

## Canonical representation

Each source incident becomes two canonical measurement records:
one for `downtime_minutes` and one for `failure_frequency`. This preserves
both numeric measures without adding non-standard metric columns. The
case-specific `shift` and `severity` attributes are retained as two documented
additional columns after the 20 mandatory fields.

All records are synthetic. Date-only source values are normalized to
midnight UTC (`YYYY-MM-DDT00:00:00Z`); this is a date normalization, not a
claim that the incident occurred at exactly midnight.

## Rebuild

From the repository root:

```powershell
py scripts/data_pipeline/extract_data.py
py scripts/data_pipeline/sample_data.py
py scripts/data_pipeline/standardize_data.py
py scripts/data_pipeline/publish_data.py
py scripts/data_pipeline/validate_data.py
```

The pipeline uses the source file already committed in this repository and
does not require a live API or an external service.
