# Data Source Inventory

## Project

- **Project:** POC-21 - Downtime Root Cause Explorer
- **Phase:** Phase 3 - Post #1, Canonical Data Foundation
- **Base application:** Existing Phase 2 Downtime Root Cause Explorer
- **Existing Phase 2 repository:** https://github.com/niranjanats07/POC-21-Downtime-Root-Cause-Explorer-Niranjana-Phase2
- **Live frontend:** https://downtime-frontend.onrender.com/
- **Live backend:** https://downtime-backend.onrender.com/

## Existing Application Data Flow

The FastAPI backend imports `load_downtime_data()` from `backend/app/data/loader.py`.

The current loader reads `data/canonical/intelligence_data.csv` using a repository-relative path.

The loader selects measurement records, reconstructs incident-level records from the canonical measurements, and exposes the incident data through the existing API endpoints. The Next.js frontend consumes the backend API.

The backend data-loading implementation now uses the canonical dataset. The existing dashboard and visualization behavior is intended to remain compatible with the Phase 2 application and must be regression-tested.

## Source Inventory

| Source | Type | Access Method | Current App Usage | Raw Size | Record Count / Columns | Update Pattern | Important Fields | Sensitivity | Phase 3 Decision |
|---|---|---|---|---:|---|---|---|---|---|
| `data/synthetic/downtime_incidents.csv` | Synthetic CSV | Local repository file | Input to canonical data pipeline; application now reads the generated canonical dataset | 1,212 bytes | 10 records / 11 columns | Static local file; no automated update pattern identified in the supplied project snapshot | `incident_id`, `machine_id`, `incident_date`, `shift`, `root_cause`, `sub_cause`, `downtime_minutes`, `failure_frequency`, `severity`, `status`, `description` | Synthetic demonstration data; no personal data observed | Sole Post #1 source |

## Source Fields

The source contains these 11 fields:

`incident_id`, `machine_id`, `incident_date`, `shift`, `root_cause`, `sub_cause`, `downtime_minutes`, `failure_frequency`, `severity`, `status`, `description`.

## Canonical Representation

The canonical dataset is stored at:

`data/canonical/intelligence_data.csv`

It contains 20 measurement records representing the 10 source incidents.

The first 20 columns follow the required universal schema. The additional domain-specific columns are `shift` and `severity`.

The published JSON is generated from the canonical CSV at:

`data/published/intelligence_data.json`

## Excluded Sources

No additional source file, public API, database, user-uploaded data source or simulation output was identified in the supplied project snapshot for this Post #1 package.

The live API is not used as a Phase 3 extraction dependency.

## Licensing or Access Notes

The source is labelled and stored as synthetic project demonstration data.

No third-party license or external API dependency is identified for this CSV in the supplied repository. This inventory is based on the supplied project snapshot; confirm any later source additions before using them.

## Data Risks

- Data is synthetic and not representative of real plant operations.
- Only 10 incidents are present; distributions and trends are illustrative.
- All records have `status=Closed`, so status variation is absent.
- No location fields are supplied.
- `incident_date` is date-only; no event time or timezone is supplied.
- No personal or restricted fields were observed in the source.
- Manual reviewer confirmation of the personal-data assessment remains required.

## Selected Phase 3 Source

The selected source is:

`data/synthetic/downtime_incidents.csv`

The complete source is retained in:

`data/source-sample/source_sample.csv`

The canonical file is generated from that source sample through the documented pipeline.