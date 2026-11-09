# Data Intelligence Integration Mapping

## 1. Project Information

- Project ID: POC-21
- Project: Downtime Root Cause Explorer
- Phase: Phase 3
- Work package: Post #4 - Data Intelligence integration
- Approved analytical track: Track A - Comparative Intelligence
- Canonical data version: 1.1.0
- Analytical method version: 1.0.0

## 2. Integration Overview

The Data Intelligence page is implemented as a Next.js client page at:

`frontend/src/app/data-intelligence/page.tsx`

The page retrieves its analytical summary, comparative results, and metadata from the FastAPI backend.

Backend route definitions are in `backend/app/main.py`. Intelligence package loading and contract validation are implemented in `backend/app/intelligence/service.py`.

## 3. API Base URL

The frontend resolves its API base URL using:

`process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"`

The frontend also reads `NEXT_PUBLIC_INTELLIGENCE_STALE_AFTER_DAYS` to configure the freshness threshold. The default threshold is 7 days when the configured value is absent or invalid.

## 4. Endpoint-to-Frontend Mapping

| Backend endpoint | Purpose | Frontend integration status |
|---|---|---|
| `GET /api/intelligence/summary` | Returns the analytical summary | Consumed during page loading |
| `GET /api/intelligence/results` | Returns comparative analytical findings | Consumed during page loading |
| `GET /api/intelligence/metadata` | Returns project, version, timestamp, and quality metadata | Consumed during page loading |
| `GET /api/intelligence/results/{result_id}` | Returns one finding by result identifier | Backend endpoint implemented; no direct fetch identified in the inspected page |
| `GET /api/intelligence/health` | Returns package health status | Backend endpoint implemented; no direct fetch identified in the inspected page |

## 5. Frontend Data Flow

1. The Data Intelligence page starts its loading process in a React effect.
2. It requests summary, results, and metadata concurrently using `Promise.all`.
3. It checks each response and raises a user-facing loading error if a required request fails.
4. It parses the returned JSON and stores the summary and result records in React state.
5. It obtains the generation timestamp from metadata, with the summary timestamp available as a fallback.
6. It records the time at which freshness was checked.
7. The page renders the summary, result findings, metadata, and freshness information.

## 6. Result Structure and Dimension Filtering

The frontend result type includes:

- `result_id`
- `result_type`
- `group_key`
- `metric_name`
- `result_value`
- `result_category`
- `priority_rank`
- `finding`
- `evidence`
- `method_version`
- `data_version`
- `generated_at`
- `quality_status`
- `limitation`

The dimension selector supports:

- All dimensions
- Root cause category
- Machine
- Shift

Filtering uses `result_category`. The selected dimension is applied to the displayed findings and supporting evidence through the `filteredResults` collection.

## 7. Version and Freshness Integration

The frontend expects data version `1.1.0` and method version `1.0.0`.

The metadata endpoint supplies `generated_at`. The frontend evaluates the timestamp against the recorded freshness-check time.

- Fresh: timestamp is valid and its age is within the configured threshold.
- Stale: timestamp is valid and its age exceeds the configured threshold.
- Unknown: timestamp is missing, invalid, in the future, or freshness cannot be evaluated.

The default stale threshold is 7 days. It can be changed through `NEXT_PUBLIC_INTELLIGENCE_STALE_AFTER_DAYS`.

## 8. Backend Validation and Error Handling

The five intelligence endpoints use `_load_intelligence_or_http_error()` in `backend/app/main.py`.

The helper calls `load_intelligence()` from the intelligence service. The service validates the summary and result package, including project identity, versions, required fields, numeric values, rankings, evidence, timestamps, result identifiers, and validation status.

Observed API error behaviour:

- HTTP 503: intelligence data is unavailable or fails contract validation.
- HTTP 404: a requested result identifier does not exist.

The frontend checks the summary, results, and metadata responses and reports loading errors when a required request is unsuccessful.

## 9. Analytical Integrity

The page presents deterministic descriptive comparative intelligence from the approved Track A analytical process.

The findings support review and prioritisation of observed root-cause categories, machines, and shifts. They do not establish causation, predict future failures, or represent verified real-world industrial performance.

The canonical dataset is synthetic. Results must retain their documented limitations and quality status.

## 10. Implementation References

| Component | File |
|---|---|
| Data Intelligence frontend | `frontend/src/app/data-intelligence/page.tsx` |
| FastAPI routes | `backend/app/main.py` |
| Intelligence package loader and validator | `backend/app/intelligence/service.py` |
| Analytical summary output | `data-science/outputs/intelligence_summary.json` |
| Analytical results output | `data-science/outputs/intelligence_results.json` |
| API contract | `docs/INTELLIGENCE_API_CONTRACT.md` |
| UAT report | `docs/DATA_INTELLIGENCE_UAT.md` |

## 11. Verification Scope

The following integration behaviour has been verified during Post #4 work:

- Summary, results, and metadata endpoints return the expected package information.
- The individual result endpoint returns a matching finding and returns HTTP 404 for an unknown identifier.
- Contract-loading and validation failures are handled as HTTP 503 responses.
- The frontend displays data version 1.1.0, method version 1.0.0, validation PASS, freshness, and generated timestamp.
- The dimension selector displays root-cause, machine, and shift result groups.
- Supporting evidence follows the selected dimension.
- Frontend ESLint, TypeScript checks, and production build passed after the dimension-filter implementation.

## 12. Conclusion

The Data Intelligence frontend is integrated with the approved comparative intelligence package through the summary, results, and metadata APIs. The backend also exposes individual-result and health endpoints. The mapping distinguishes implemented backend routes from endpoints directly consumed by the inspected frontend page.