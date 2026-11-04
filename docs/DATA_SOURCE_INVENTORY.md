# Data Source Inventory

## Project

- **Project:** POC-21 — Downtime Root Cause Explorer
- **Phase:** Phase 3 — Post #1, Canonical Data Foundation
- **Base application:** Existing Phase 2 Downtime Root Cause Explorer
- **Existing Phase 2 repository:** https://github.com/niranjanats07/POC-21-Downtime-Root-Cause-Explorer-Niranjana-Phase2
- **Live frontend:** https://downtime-frontend.onrender.com/
- **Live backend:** https://downtime-backend.onrender.com/

## Existing Application Data Flow

The FastAPI backend imports `load_downtime_data()` from
`backend/app/data/loader.py`. That loader reads
`data/synthetic/downtime_incidents.csv` using a repository-relative path.
The API exposes incident data, KPI and chart endpoints from this loaded
dataset. The Next.js frontend consumes the backend API. Phase 3 Post #1 does
not change this application data flow or its operational visualizations.

## Source Inventory

| Source | Type | Access Method | Current Usage | Raw Size | Record Count | Sensitivity | Phase 3 Decision |
|---|---|---|---|---:|---:|---|---|
| `data/synthetic/downtime_incidents.csv` | Synthetic CSV | Local repository file; loaded by `backend/app/data/loader.py` | Backend incident, KPI, chart, filter and export endpoints | 1,202 bytes | 10 rows × 11 columns | Synthetic demonstration data; no personal data observed | Use as the sole Post #1 source |

## Source Fields

`incident_id`, `machine_id`, `incident_date`, `shift`, `root_cause`,
`sub_cause`, `downtime_minutes`, `failure_frequency`, `severity`, `status`,
`description`.

## Excluded Sources

No additional source file, public API, database, user-uploaded data source or
simulation output was identified in the supplied project snapshot for this
Post #1 package. The live API is not used as a Phase 3 extraction dependency.

## Licensing or Access Notes

The source is labelled and stored as synthetic project demonstration data.
No third-party license or external API dependency is identified for this CSV
in the supplied repository. This inventory is based on the supplied project
snapshot; confirm any later source additions before using them.

## Data Risks

- Data is synthetic and not representative of real plant operations.
- Only 10 incidents are present; distributions and trends are illustrative.
- All records have `status=Closed`, so status variation is absent.
- No location fields are supplied.
- `incident_date` is date-only; no event time or timezone is supplied.
- No personal or restricted fields were observed in the source.

## Selected Phase 3 Source

Use only `data/synthetic/downtime_incidents.csv`, copied without row loss to
`data/source-sample/source_sample.csv`. The canonical file is generated from
that source sample through the documented pipeline.
