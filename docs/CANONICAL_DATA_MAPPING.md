# Canonical Data Mapping

## Mapping Strategy

Each source incident is represented by two canonical `measurement` rows:
one row for `downtime_minutes` and one row for `failure_frequency`. This
retains both numeric source measures while keeping the universal 20-column
contract intact. The source incident identifier is repeated in
`source_record_id`; deterministic metric-specific `record_id` values keep
canonical rows unique.

Two documented domain-specific columns, `shift` and `severity`, are appended
after the 20 mandatory columns because neither has a semantically correct
universal canonical field. They are required for this downtime case study
and do not duplicate a mandatory field.

## Field Mapping

| Source Field | Canonical Field | Transformation | Required | Example | Notes |
|---|---|---|---|---|---|
| `incident_id` | `source_record_id` | Preserve source ID | No | `INC001` | Original incident key |
| `incident_id` | `record_id` | `POC21-{incident_id}-DOWNTIME` or `POC21-{incident_id}-FREQUENCY` | Yes | `POC21-INC001-DOWNTIME` | Stable unique ID per metric row |
| Fixed value | `record_type` | Set to `measurement` | Yes | `measurement` | One row per numeric measurement |
| `incident_date` | `observed_at` | Convert date-only value to ISO 8601 midnight UTC | No | `2026-01-05T00:00:00Z` | Midnight is normalization, not source event time |
| `machine_id` | `entity_id` | Preserve machine identifier | No | `MCH-01` | Machine associated with incident |
| Derived from `machine_id` | `entity_name` | Prefix with `Machine ` | No | `Machine MCH-01` | Readable label |
| `root_cause` | `category` | Trim, lowercase, replace spaces with underscores | No | `mechanical` | Standardized category |
| `sub_cause` | `subcategory` | Trim, lowercase, replace spaces with underscores | No | `bearing_failure` | Standardized subcategory |
| `status` | `status` | Trim and lowercase | No | `closed` | Source status |
| `downtime_minutes` | `metric_name` / `metric_value` / `metric_unit` | Emit one measurement row; numeric value; unit `minutes` | No | `downtime_minutes`, `120`, `minutes` | First metric row per incident |
| `failure_frequency` | `metric_name` / `metric_value` / `metric_unit` | Emit second measurement row; numeric value; unit `count` | No | `failure_frequency`, `3`, `count` | Second metric row per incident |
| `description` | `text_value` | Trim and cap at 500 characters | No | `Bearing wear caused machine stoppage` | Retained as short context |
| `shift` | `shift` (domain-specific) | Trim and lowercase | No | `morning` | No universal field has equivalent meaning |
| `severity` | `severity` (domain-specific) | Trim and lowercase | No | `high` | No universal field has equivalent meaning |
| Fixed value | `source_name` | `synthetic_downtime_incidents_csv` | Yes | `synthetic_downtime_incidents_csv` | Source provenance |
| Fixed value | `is_synthetic` | Boolean `true` | Yes | `true` | All supplied records are synthetic |
| Fixed value | `data_version` | `1.0.0` | Yes | `1.0.0` | Package version |

## Unused Universal Fields

- `related_entity_id`: blank; the source has no linked-entity relationship.
- `stage`: blank; `shift` is not a process lifecycle stage.
- `latitude`, `longitude`: blank; the source has no geographic data.

## Removed Fields

No source fields are removed from the source sample. All 11 original source
fields are either mapped to canonical fields or retained as the documented
`shift` and `severity` extensions.

## Derived Values and Formulas

- `record_id`: deterministic concatenation of project, source incident ID
  and metric identifier.
- `entity_name`: `Machine {machine_id}`.
- `observed_at`: source date plus `T00:00:00Z`.
- Two canonical rows are emitted per source incident, one per numeric metric.

## Category Normalization

`root_cause`, `sub_cause`, `status`, `shift` and `severity` are trimmed and
converted to lowercase; spaces in category fields are replaced with
underscores. Original source spelling remains unchanged in
`source_sample.csv`.

## Unit Normalization

`downtime_minutes` uses `minutes`; `failure_frequency` uses `count`.
Numeric fields contain numbers only.

## Null Handling

Unavailable universal fields are written as blank CSV values and become
JSON `null`. No source metric is silently converted to zero by the canonical
standardization pipeline.

## Text Cleaning

Descriptions are trimmed and limited to 500 characters.

## Synthetic-Data Identification

`is_synthetic=true` for every canonical row because the source is explicitly
stored under `data/synthetic/` and contains synthetic demonstration incidents.