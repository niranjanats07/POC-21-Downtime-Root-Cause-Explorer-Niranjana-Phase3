# Intelligence API Contract

## 1. Project Information

| Field | Value |
|---|---|
| Project ID | POC-21 |
| Project | Downtime Root Cause Explorer |
| Phase | Phase 3 - Post #4 |
| Analytical Track | Track A - Comparative Intelligence |
| Data Version | 1.1.0 |
| Method Version | 1.0.0 |
| API Framework | FastAPI |
| Default Backend URL | http://localhost:8000 |

## 2. Purpose

This document defines the implemented backend API contract used by the Data Intelligence page.

The API exposes the approved analytical summary, standardized findings, individual finding details, package metadata and health status.

All analytical values originate from the approved canonical dataset:

`data/canonical/intelligence_data.csv`

The API preserves the approved Track A analytical outputs and their documented limitations.

## 3. API Base URL

The frontend reads the backend URL from:

`NEXT_PUBLIC_API_URL`

When the environment variable is not configured, the frontend defaults to:

`http://localhost:8000`

All endpoints use the `/api/intelligence` prefix.

## 4. Implemented Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/intelligence/summary` | Returns the analytical summary |
| GET | `/api/intelligence/results` | Returns the flat array of analytical findings |
| GET | `/api/intelligence/results/{result_id}` | Returns one finding identified by its result ID |
| GET | `/api/intelligence/metadata` | Returns project and analytical version metadata |
| GET | `/api/intelligence/health` | Returns the intelligence package health status |

All five routes use the shared intelligence package loader and contract validation.
## 5. Summary Response

`GET /api/intelligence/summary`

Returns a JSON object containing the analytical summary.

The verified response includes:

| Field | Description |
|---|---|
| `project_id` | Project identifier |
| `poc_title` | Project title |
| `data_version` | Canonical data version |
| `method_version` | Analytical method version |
| `approved_track` | Approved analytical track |
| `primary_analytical_question` | Approved analytical question |
| `decision_to_be_supported` | Intended decision support |
| `total_result_count` | Number of exported findings |
| `key_findings` | Human-readable leading findings |
| `priority_items` | Highest-ranked group for each comparison dimension |
| `validation_result` | Overall analytical validation status |
| `important_limitations` | Important interpretation limitations |
| `generation_timestamp` | Summary generation timestamp |
| `overall_metrics` | Aggregate incident and measurement metrics |
| `top_observed_root_cause_category` | Leading root-cause group and metrics |
| `top_observed_machine` | Leading machine group and metrics |
| `top_observed_shift` | Leading shift group and metrics |

The live verified response reported:

- Total findings: 11
- Validation result: PASS
- Complete source incidents: 30
- Total downtime: 2,795.0 minutes
- Total failure frequency: 65.0

The leading observed groups were:

- Mechanical: 1,265.0 downtime minutes
- MCH-02: 850.0 downtime minutes
- Morning shift: 1,060.0 downtime minutes

These values describe the approved synthetic dataset only.

## 6. Results Response

`GET /api/intelligence/results`

Returns the complete flat JSON array of standardized analytical findings.

The approved export contains 11 findings.

Each finding follows the field structure defined in:

`docs/INTELLIGENCE_OUTPUT_CONTRACT.md`

Important fields include:

- `result_id`
- `result_type`
- `group_key`
- `metric_name`
- `result_value`
- `result_unit`
- `result_category`
- `priority_rank`
- `finding`
- `evidence`
- `method_version`
- `data_version`
- `generated_at`
- `quality_status`
- `limitation`

The frontend uses `result_category` to filter findings by comparison dimension.

Supported categories:

- `root_cause_category`
- `machine`
- `shift`

The API returns the complete result collection. The dimension filter is applied in the frontend and is not a backend query parameter.

## 7. Individual Result Response

`GET /api/intelligence/results/{result_id}`

Returns the complete analytical finding matching the supplied `result_id`.

The response uses the same standardized finding structure as the results endpoint.

### Not-found behaviour

If the supplied result ID does not exist, the endpoint returns:

**HTTP 404**

```json
{
  "detail": "Intelligence result not found."
}
```

## 8. Metadata Response

`GET /api/intelligence/metadata`

Returns project and analytical version metadata, including project identity, data version, method version, approved analytical track, generation timestamp, and quality status.

## 9. Health Response

`GET /api/intelligence/health`

Returns the current intelligence package health status, including its data version, method version, and quality status.

## 10. Validation and Error Handling

All five endpoints call:

`_load_intelligence_or_http_error()`

The shared helper calls the intelligence package loader.

The backend service validates the analytical package, including:

- Project identity
- Data and method versions
- Summary validation status
- Result count
- Required result fields
- Allowed result types, categories, metrics and units
- Numeric result validity
- Ranking validity
- Evidence structure
- Duplicate result identifiers
- Timestamp validity

The shared helper converts handled loading and validation exceptions into a controlled service-unavailable response.

### HTTP status behaviour

| HTTP status | Meaning |
|---|---|
| 200 | Requested resource returned successfully |
| 404 | Requested result ID does not exist |
| 503 | Intelligence data is unavailable or failed contract validation |

The documented 503 response message is:

`Data Intelligence data is unavailable or failed contract validation.`

Other unexpected server or transport failures are not claimed to be covered by this specific exception mapping.

## 11. Frontend Integration Contract

The Data Intelligence page currently fetches these three endpoints concurrently:

- `/api/intelligence/summary`
- `/api/intelligence/results`
- `/api/intelligence/metadata`

The frontend:

1. Starts in a loading state.
2. Checks the HTTP status of all three responses.
3. Parses the JSON responses.
4. Checks summary and metadata data versions.
5. Checks every returned finding's data and method versions.
6. Stores the summary, findings and generation timestamp.
7. Calculates freshness using the stored generation timestamp.
8. Displays a controlled error message when loading or version validation fails.
9. Ends the loading state in a `finally` block.

The page currently applies dimension filtering locally using `result_category`.

The individual result-detail endpoint is implemented by the backend. The current page's identified fetch calls do not include that endpoint.

## 12. Version and Freshness Requirements

The approved versions are:

| Version field | Required value |
|---|---|
| `data_version` | `1.1.0` |
| `method_version` | `1.0.0` |

The frontend rejects version mismatches.

The page displays the generation timestamp and a freshness classification.

The configured stale threshold is seven days by default.

Missing, invalid or future generation timestamps must not be presented as confirmed fresh data.

## 13. Data and Analytical Integrity

The API must not:

- Modify approved analytical values.
- Invent findings or evidence.
- Replace the canonical dataset with an unapproved source.
- Treat frontend filtering as a new analytical calculation.
- Present synthetic findings as actual industrial performance.
- Interpret comparative rankings as causal or predictive conclusions.

The API exposes deterministic descriptive outputs from the approved Track A analytical process.

## 14. Verification Evidence

The following checks were observed during Post #4 integration:

| Check | Observed result |
|---|---|
| Health endpoint | HTTP 200; healthy |
| Summary endpoint | Returned approved summary |
| Results endpoint | 11 findings verified |
| Result detail | RES-0001 returned successfully |
| Unknown result ID | HTTP 404 |
| Metadata endpoint | Versions and generation timestamp verified |
| Contract failure handling | Controlled HTTP 503 verified |
| Backend Python compilation | PASS |

These records describe the verification evidence available during document preparation. They do not imply that every possible API failure or edge case has been tested.

## 15. Limitations and Responsible Use

All source incidents are synthetic.

The API results are descriptive demonstration outputs only. They:

- Do not represent actual industrial performance.
- Do not establish causal relationships.
- Are not predictive evidence.
- Do not provide probabilities of future downtime.
- Do not guarantee future failure outcomes.
- May change when additional observations are introduced.

The API must preserve the limitations supplied with each analytical finding and in the analytical summary.

## 16. Contract Conclusion

The Data Intelligence backend exposes five implemented GET endpoints for summary, results, result detail, metadata and health.

The backend applies shared package loading and contract validation before serving these resources.

The frontend consumes the summary, results and metadata endpoints, validates approved versions and applies local dimension filtering.

The API contract preserves the approved POC-21 Track A analytical outputs, version requirements and responsible-use limitations.

**Data Version:** 1.1.0
**Method Version:** 1.0.0
**Project:** POC-21
