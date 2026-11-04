# Canonical Data Package Validation

## Required Contract

The canonical CSV begins with the 20 mandatory universal fields in the exact
required order. The two documented case-specific columns, `shift` and
`severity`, follow those fields. Total columns: 22 (within the 50-column cap).

## Automated Validation

Run from the repository root:

```powershell
py scripts/data_pipeline/validate_data.py
```

The validator checks:

- Required package files and directories.
- Total `/data` size (maximum 10 MB).
- Source sample, canonical CSV and published JSON size (maximum 5 MB each).
- Canonical row and column limits.
- Exact mandatory column order and documented extension columns.
- Non-empty, unique `record_id`.
- Allowed `record_type` values.
- ISO 8601 timestamps.
- Numeric metric values and latitude/longitude values where present.
- `true`/`false` synthetic flags.
- Required `source_name` and `data_version`.
- Text values no longer than 500 characters.
- Manifest counts, column count, data version and file sizes.
- Published JSON equivalence to the canonical CSV.

The machine validator cannot certify legal ownership or detect every possible
sensitive-data issue. The source inventory therefore records a separate
human review of the supplied synthetic CSV.

## Preservation

No Phase 2 dashboard, API, backend loader, frontend page, chart, test or
deployment configuration is intentionally redesigned by this Post #1 change.
The existing Phase 2 source file remains in place and remains the backend
loader's source.

## Build and Deployment Readiness

The data package is local and does not require a live API for Phase 3 data
preparation. A fresh Repomix, clean-clone validation, Docker build and target
platform build still need to be executed in the actual Phase 3 Git repository
before deployment readiness can be claimed.
