# Canonical Data Package Validation

## Required Contract

The canonical CSV begins with the 20 mandatory universal fields in the exact
required order. The two documented case-specific columns, `shift` and
`severity`, follow those fields. Total columns: 22 (within the 50-column cap).

The package limits are:

- Total `/data` directory size: maximum 10 MB.
- Source sample CSV: maximum 5 MB.
- Canonical CSV: maximum 5 MB.
- Published JSON: maximum 5 MB.
- Canonical rows: maximum 10,000.
- Canonical columns: maximum 50.
- Text values: maximum 500 characters.

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
human review of the supplied synthetic CSV. Manual reviewer confirmation
remains necessary.

## Preservation and Backend Compatibility

The existing Phase 2 dashboard, API, frontend pages, charts, tests and
deployment configuration are intended to retain their existing behavior.
No visualization redesign is part of this Post #1 change.

The backend data-loading implementation now reads the Phase 3 canonical CSV
and reconstructs legacy-compatible incident rows for the existing API and
dashboard. The original Phase 2 source file remains in the repository as
historical project data; it is not the active backend loader source.

Local regression checks previously covered the dashboard's KPI, Pareto,
machine downtime, heatmap and root-cause views, along with filtering and
CSV/JSON exports. These checks support compatibility but do not replace
clean-clone or deployment verification.

## Build and Deployment Readiness

The data package is prepared and validated locally. A passing canonical
package validation does not by itself establish deployment readiness.

Before deployment readiness can be claimed, complete and record:

- Fresh Repomix generation after the final documentation changes.
- Clean-clone validation in the Phase 3 Git repository.
- Backend tests and frontend production build.
- Docker build, if Docker is part of the target deployment process.
- Target-platform build and deployment verification.
- Live frontend and backend endpoint checks.

Do not begin Phase 3 Post #2 until the Post #1 canonical data package has
received formal reviewer approval.