# Post #5 — Grounded Data Assistant Suitability Assessment

## Project Information

- Project: POC-21 — Downtime Root Cause Explorer
- Phase: Phase 3 Post #5
- Assessment date: 2026-11-12
- Approved analytical track: Track A — Comparative Intelligence
- Data version: 1.1.0
- Method version: 1.0.0
- Governing guide: 05_INFOCREON_PHASE3_GROUNDED_DATA_ASSISTANT_GUIDE.docx

## 1. Target User

Maintenance and operations supervisors who need to retrieve and understand approved comparative downtime findings.

## 2. Existing Operational and Intelligence Experience

The project has two existing experiences:

- Operational Dashboard: displays operational downtime KPIs, charts and incident information.
- Data Intelligence: displays approved Track A comparative findings, rankings, filters, evidence, methodology and limitations.

The assistant must complement these pages and must not replace either page.

## 3. User Questions Not Solved Conveniently Today

The existing Data Intelligence page provides tables and filters. Users must locate the relevant dimension, identify the desired result and inspect its evidence.

A guided assistant can provide a more direct question-to-result workflow, including retrieval of a specific approved finding and its recorded limitations.

It must not claim to provide new analytical insights.

## 4. Proposed Supported Questions

1. Which root-cause category ranks highest by observed downtime?
2. Which machine has the highest observed downtime?
3. Which shift ranks highest by observed downtime?
4. How do the machines compare?
5. How do root-cause categories compare?
6. What evidence supports the MCH-02 ranking?
7. What limitations apply to these findings?
8. Which data and method versions were used?

## 5. Deterministic Retrieval Mapping

| Question | Approved source | Deterministic operation |
|---|---|---|
| Highest root-cause category | intelligence_results.json | Select category result with rank 1 |
| Highest machine | intelligence_results.json | Select machine result with rank 1 |
| Highest shift | intelligence_results.json | Select shift result with rank 1 |
| Compare machines | intelligence_results.json | Retrieve machine results in rank order |
| Compare root-cause categories | intelligence_results.json | Retrieve category results in rank order |
| Evidence for MCH-02 | intelligence_results.json | Retrieve RES-0005 evidence |
| Finding limitations | intelligence_summary.json and result records | Retrieve recorded limitations |
| Data and method versions | Approved metadata and summary | Return recorded version fields |

All numerical answers must be taken directly from approved, validated output records. No frontend or assistant-side recalculation is permitted.

## 6. Evidence Availability

The existing validated loader returns:

- metadata
- summary
- results

Each result includes structured evidence factors, values, versions, quality status and a limitation.

Verified sample results:

- RES-0001: Mechanical, 1,265 minutes, 10 incidents.
- RES-0005: MCH-02, 850 minutes, 8 incidents.
- RES-0009: Morning, 1,060 minutes, 11 incidents.

Evidence is aggregate-level. Individual incident-level evidence must not be invented or implied.

## 7. Security and Privacy

The inspected data manifest identifies the dataset as synthetic and indicates that it contains no personal or restricted data.

The inspected FastAPI application files did not reveal application-level authentication or route-level authorization dependencies.

CORS is not authentication.

The assistant must:

- Reuse the existing validated intelligence package.
- Avoid unrestricted raw-data access.
- Avoid arbitrary SQL, shell commands, filesystem paths and dynamic code execution.
- Validate user input and supported intent parameters.
- Limit returned results and evidence references.
- Reject unsafe and out-of-scope requests.
- Avoid exposing secrets or internal configuration.
- Preserve existing application access boundaries.

Public or production deployment requires a separate authentication and authorization review.

## 8. Deployment Feasibility

The existing FastAPI backend and Next.js frontend provide a feasible integration foundation.

The existing intelligence loader validates the approved results and summary before returning the package.

A separate assistant service and API route can reuse this package without modifying the existing Post #4 service or endpoints.

Public deployment and Docker verification remain separate outstanding checks.

## 9. Value Beyond Filters and Tables

The proposed assistant adds:

- Guided natural-language question selection.
- Direct retrieval of approved findings.
- Clear explanations of recorded metrics.
- Direct references to approved evidence.
- Explicit limitations and version information.
- Controlled responses to unsupported questions.

It does not introduce a second analytical pipeline or independent calculation engine.

## 10. Deterministic Versus LLM Decision

Decision: deterministic guided mode.

An LLM is not required because the supported questions map to a small, fixed catalogue of approved result records and metadata.

Templates and deterministic response composition are sufficient.

No generic chatbot, unrestricted RAG, direct LLM-to-data access or LLM-generated numerical findings will be implemented.

## 11. Approved Assistant Mode

Mode A — Deterministic Guided.

The assistant will use:

- Approved Track A results.
- Approved summary and metadata.
- Fixed supported intents.
- Validated parameters.
- Deterministic query functions.
- Structured evidence references.
- Grounded response validation.
- Explicit limitations and unsupported-question handling.

## 12. Skip Rationale

Not applicable. The assessment identifies a bounded deterministic use case.

## 13. Result

DETERMINISTIC ASSISTANT SUITABLE — LLM NOT REQUIRED

Implementation is permitted to proceed under Mode A, subject to the security boundaries and evidence restrictions documented above.

This is a suitability decision, not final Post #5 maintainer approval.

## 14. Inspection Evidence

- Backend service function inspection: completed.
- Existing intelligence API route inspection: completed.
- Approved package loader inspection: completed.
- RES-0001, RES-0005 and RES-0009 evidence inspection: completed.
- Authentication and authorization search: completed; no application-level mechanism found in inspected files.
- Route dependency search: completed; no route-level dependencies found.
- Existing Data Intelligence frontend review: completed.
- Approved analytical output and limitation review: completed.

## 15. Implementation and Verification Status

The Mode A implementation has been completed locally.

Implemented:
- Deterministic intent classification and scope checks.
- Parameter validation and approved Track A query routing.
- Validated intelligence-package retrieval.
- Structured evidence construction and response validation.
- FastAPI assistant query endpoint.
- Data Intelligence page assistant components.
- Fixed supported-question catalogue and explicit limitations.

Verification evidence is documented in:
- `docs/ASSISTANT_IMPLEMENTATION_LOG.md`
- `docs/ASSISTANT_GROUNDING_VALIDATION.md`
- `docs/ASSISTANT_UAT.md`
- `docs/ASSISTANT_QUERY_CONTRACT.md`
- `docs/GROUNDED_RESPONSE_CONTRACT.md`

Local backend regression: 35 passed, 0 failed.
Assistant-specific tests: 21 passed, 0 failed.
Frontend TypeScript and production build: passed.
Manual browser regression: documented in the UAT and implementation log.

These results establish local implementation and test evidence only. Selenium execution has not been confirmed. The new Phase 3 Render deployment has not yet been verified with the Post #5 source, and maintainer approval is pending.

Proceed to final Post #5 requirement-to-evidence review and submission preparation. Do not claim final approval or deployment certification until those gates are completed.
