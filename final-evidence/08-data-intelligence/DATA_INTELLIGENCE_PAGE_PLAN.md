# Data Intelligence Page Plan

## 1. Project Information

| Field | Value |
|---|---|
| Project ID | POC-21 |
| Project | Downtime Root Cause Explorer |
| Phase | Phase 3 |
| Delivery | Post #4 — Data Intelligence Integration |
| Page | Data Intelligence |
| Frontend route | `/data-intelligence` |
| Frontend implementation | `frontend/src/app/data-intelligence/page.tsx` |
| Primary analytical track | Track A — Comparative Intelligence |
| Canonical data version | 1.1.0 |
| Analytical method version | 1.0.0 |
| Plan status | Implementation completed; final verification pending |

## 2. Background and Purpose

The Data Intelligence page extends the Downtime Root Cause Explorer with a dedicated interface for reviewing approved comparative analytical results.

The page presents deterministic descriptive comparisons of downtime and failure-frequency burden across:

- Root-cause categories.
- Machines.
- Shifts.

The purpose is to help users identify and review observed groups with higher comparative downtime burden.

The page consumes the approved analytical output from Post #3. It must not introduce a new analytical method or modify the approved canonical dataset.

## 3. Business Objective

Provide a structured interface that allows users to:

1. Review the approved intelligence package.
2. Confirm data and analytical method versions.
3. Review validation and freshness information.
4. Understand high-priority comparative findings.
5. Compare results across root-cause categories, machines, and shifts.
6. Inspect supporting evidence and result-specific limitations.
7. Understand the methodology and responsible-use boundaries.

The page is intended for descriptive operational review and prioritisation, not automated operational decisions.

## 4. Approved Analytical Scope

The page uses the approved Track A — Comparative Intelligence process.

| Item | Approved specification |
|---|---|
| Analytical track | Track A — Comparative Intelligence |
| Data source | Synthetic canonical downtime incident dataset |
| Canonical file | `data/canonical/intelligence_data.csv` |
| Data version | 1.1.0 |
| Method version | 1.0.0 |
| Primary measurements | Downtime and failure frequency |
| Comparison dimensions | Root cause, machine, shift |
| Analytical approach | Deterministic descriptive grouped comparisons |
| Decision-support purpose | Review and prioritisation of observed groups |

### Approved baseline findings

| Dimension | Highest-ranked group | Total downtime | Incident count |
|---|---|---:|---:|
| Root cause | Mechanical | 1,265 minutes | 10 |
| Machine | MCH-02 | 850 minutes | 8 |
| Shift | Morning | 1,060 minutes | 11 |

These values are approved Post #3 baseline findings and must remain consistent with the analytical output.

## 5. Scope of the Page

### Included

- Intelligence summary integration.
- Ranked intelligence results integration.
- Metadata and freshness integration.
- Version and validation visibility.
- KPI summary cards.
- Highest-priority comparative findings.
- Dimension-based result filtering.
- Supporting evidence display.
- Methodology information.
- Limitations and responsible-use information.
- Loading and error states.
- Navigation to the existing operational dashboard.

### Excluded

- Predictive maintenance.
- Machine-learning predictions.
- Causal inference.
- Automated maintenance recommendations.
- Live industrial equipment monitoring.
- Modification of approved analytical results.
- Replacement of the existing operational dashboard.

## 6. Architecture and Integration Plan

The integration follows the existing frontend/backend architecture.

### Frontend

Primary file:

`frontend/src/app/data-intelligence/page.tsx`

Responsibilities:

- Retrieve intelligence data from the backend.
- Display metadata and summary information.
- Present ranked results and findings.
- Filter results by analytical dimension.
- Display matching supporting evidence.
- Communicate freshness and validation status.
- Handle loading and error states.

### Backend

Implementation files:

- `backend/app/main.py`
- `backend/app/intelligence/service.py`

Responsibilities:

- Expose intelligence API endpoints.
- Load the approved analytical output.
- Validate the intelligence package.
- Return metadata and result information.
- Handle unavailable or invalid analytical data through controlled API errors.

### Analytical outputs

- `data-science/outputs/intelligence_summary.json`
- `data-science/outputs/intelligence_results.json`

The frontend must consume these outputs through the backend API rather than independently recomputing the approved analytical results.

## 7. API Integration Plan

The frontend uses the configured API base URL:

`NEXT_PUBLIC_API_URL`

Default:

`http://localhost:8000`

The page integrates the following endpoints:

| Endpoint | Purpose |
|---|---|
| `/api/intelligence/summary` | Summary metrics and validation information |
| `/api/intelligence/results` | Comparative intelligence results |
| `/api/intelligence/metadata` | Project, version, freshness, and approval metadata |
| `/api/intelligence/results/{result_id}` | Individual result detail |
| `/api/intelligence/health` | Intelligence package health |

The page directly consumes summary, results, and metadata for its primary display.

The result-detail and health endpoints support the wider backend API contract and verification scope.

## 8. Metadata and Freshness Plan

The interface must display:

- Data version.
- Method version.
- Validation result.
- Approved analytical track.
- Data freshness.
- Generation timestamp.

Expected versions:

- Data version: 1.1.0.
- Method version: 1.0.0.

Freshness behavior:

| Condition | Display |
|---|---|
| Valid timestamp within threshold | Fresh |
| Valid timestamp beyond threshold | Stale |
| Missing or invalid timestamp | Unknown |
| Future timestamp | Unknown |

The default stale threshold is seven days and can be configured using `NEXT_PUBLIC_INTELLIGENCE_STALE_AFTER_DAYS`.

## 9. KPI and Findings Plan

The page provides four summary KPIs:

1. Intelligence Results.
2. Validated Results.
3. Source Incidents.
4. Data Quality.

The Key Comparative Findings section presents up to three results ordered by priority rank.

Each finding includes its group, priority, quality status, finding description, metric name, and result value.

The displayed findings must remain consistent with the approved analytical output.

## 10. Comparative Results and Filtering Plan

The ranked comparative results table displays:

- Rank.
- Type.
- Group.
- Metric.
- Value.
- Category.
- Quality.

The dimension selector provides:

- All dimensions.
- Root cause category.
- Machine.
- Shift.

Filtering is based on the analytical `result_category` field.

The filtered result collection must be shared by the ranked table and Supporting Evidence section.

An appropriate empty state must be displayed when a selection produces no results.

## 11. Supporting Evidence Plan

Each result's evidence must remain associated with its corresponding analytical result.

The evidence display includes:

- Result type.
- Group key.
- Priority rank.
- Evidence factors.
- Evidence values.
- Optional contribution.
- Result-specific limitation.

Filtering must update the evidence section consistently with the selected comparison dimension.

## 12. Methodology and Responsible Use

The interface must identify the analytical approach as Track A — Comparative Intelligence.

It must communicate that the results support deterministic descriptive review and prioritisation.

The page must explicitly preserve these limitations:

- Source incidents are synthetic and intended for demonstration.
- Results are descriptive, not causal.
- Results are not predictive evidence.
- Results must not be presented as actual industrial performance.
- Small group sizes may affect ranking stability.

## 13. Loading, Error, and Navigation Plan

### Loading

Display a clear loading message while the intelligence package is being retrieved.

### Error

Display a controlled error state when intelligence data cannot be loaded.

Provide a navigation link back to the operational dashboard.

### Navigation

The Data Intelligence page must remain separate from the existing operational dashboard.

The operational dashboard route remains `/`.

## 14. Implementation Milestones and Current Status

| Milestone | Work item | Current status |
|---|---|---|
| 1 | Confirm approved Track A analytical baseline | Completed |
| 2 | Implement individual intelligence result endpoint | Completed |
| 3 | Implement backend intelligence contract validation | Completed |
| 4 | Implement controlled API failure handling | Completed |
| 5 | Expose metadata and freshness information | Completed |
| 6 | Integrate summary, results, and metadata in frontend | Completed |
| 7 | Implement Data Intelligence page | Completed |
| 8 | Implement dimension-based filtering | Completed |
| 9 | Synchronize supporting evidence with filtering | Completed |
| 10 | Create API contract documentation | Completed |
| 11 | Create integration mapping documentation | Created; structural verification substantially complete |
| 12 | Create UI specification | Completed; 18 sections verified |
| 13 | Record UAT evidence | Updated; VERIFIED WITH OBSERVATION |
| 14 | Complete All dimensions browser verification | Completed; 11 results verified |
| 15 | Complete responsive-layout verification | Completed; desktop, tablet and mobile reviewed |
| 16 | Complete accessibility review | Completed; VERIFIED WITH OBSERVATION |
| 17 | Complete operational-page regression | Completed; documented filter and reset tests |
| 18 | Complete final submission evidence | Pending |

## 15. Acceptance Criteria

The page is considered ready for final acceptance when the following criteria are verified:

### Data and API

- Correct project and analytical versions are displayed.
- Backend contract validation passes.
- Summary and result endpoints return the approved output.
- Metadata and freshness are displayed correctly.
- Invalid or unavailable data is handled through a controlled error state.

### Interface

- KPI values match the approved summary.
- Key findings match the approved analytical baseline.
- Ranked results display the expected fields.
- All four dimension selector options work.
- Supporting evidence follows the selected dimension.
- Loading and error states work as intended.
- Methodology and limitations are visible.

### Quality and regression

- ESLint passes.
- TypeScript validation passes.
- Production build passes.
- Responsive layout is reviewed.
- Accessibility checks are completed.
- Existing operational dashboard behavior is preserved.
- Final UAT evidence is recorded.

## 16. Documentation and Evidence

The following documents support the Post #4 integration:

- `docs/INTELLIGENCE_API_CONTRACT.md`
- `docs/INTELLIGENCE_INTEGRATION_MAPPING.md`
- `docs/DATA_INTELLIGENCE_UI_SPEC.md`
- `docs/DATA_INTELLIGENCE_UAT.md`
- `docs/OPERATIONAL_PAGE_REGRESSION_REPORT.md`

The following existing Post #3 analytical documents remain authoritative for the approved analytical basis:

- `docs/ANALYTICAL_TRACK_EXECUTION_PLAN.md`
- `docs/ANALYTICAL_INPUT_CONTRACT.md`
- `docs/ANALYTICAL_METHOD_REPORT.md`
- `docs/ANALYTICAL_VALIDATION_REPORT.md`
- `docs/WEAK_CASE_AND_LIMITATION_REVIEW.md`

Implementation changes and verification evidence must be recorded in the relevant project documentation.

Existing Post #3 files and backups must be preserved.

## 17. Outstanding Work

The following Post #4 implementation and verification activities have been completed:

1. Verified the All dimensions selection displays all 11 intelligence results.
2. Completed responsive-layout checks at desktop, tablet, and mobile widths.
3. Completed the manual accessibility review. Overall status: VERIFIED WITH OBSERVATION. Check 8 includes completed Windows Narrator testing and retains its documented observation.
4. Completed operational dashboard regression testing for the documented filter and reset flows.
5. Recorded observed regression results in docs/OPERATIONAL_PAGE_REGRESSION_REPORT.md.
6. Updated the UAT report with implementation, verification, Lighthouse, and accessibility evidence.
7. Created and verified the operational-page regression report.
8. Created or verified the Data Intelligence page plan, integration mapping, API contract, UI specification, UAT report, and operational regression report.

Remaining final acceptance activities:

1. Perform a final inventory and consistency review of all required Post #4 documentation and supporting analytical reference documents.
2. Assemble the final submission evidence, including relevant test results, verification records, and document paths.
3. Review the complete Post #4 acceptance criteria and determine the final submission status.

Only activities supported by observed evidence may be marked PASS. The final Post #4 acceptance decision remains pending until the remaining activities are completed.
## 18. Conclusion

The Data Intelligence page integrates the approved Track A comparative intelligence output into the Downtime Root Cause Explorer.

The implementation includes metadata, freshness, KPI summaries, ranked findings, dimension filtering, supporting evidence, methodology, and responsible-use information.

The remaining work is focused on final verification, regression testing, documentation completeness, and Post #4 acceptance.
