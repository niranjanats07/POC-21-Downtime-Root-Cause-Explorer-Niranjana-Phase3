# Data Intelligence Ã¢â‚¬â€ User Acceptance Test Report

## 1. Test Information

| Field | Value |
|---|---|
| Project | POC-21 Ã¢â‚¬â€ Downtime Root Cause Explorer |
| Phase | Phase 3 Ã¢â‚¬â€ Post #4 |
| Page | Data Intelligence |
| Test date | 2026-11-09 |
| Environment | Local production build |
| Browser URL | http://localhost:3001/data-intelligence |
| Approved analytical track | Track A Ã¢â‚¬â€ Comparative Intelligence |

## 2. Application Verification

| Test | Expected result | Observed result | Status |
|---|---|---|---|
| Data version | 1.1.0 | 1.1.0 | PASS |
| Method version | 1.0.0 | 1.0.0 | PASS |
| Validation status | PASS | PASS | PASS |
| Approved track | Track A | TRACK A - COMPARATIVE INTELLIGENCE | PASS |
| Data freshness | Fresh | Fresh | PASS |
| Intelligence result count | 11 | 11 | PASS |
| Validated result count | 11 | 11 | PASS |
| Source incident count | 30 | 30 | PASS |
| Data quality | PASS | PASS | PASS |

## 3. Dimension Filter Interaction Tests

The Compare by dropdown filters results using the analytical result category.

| Selection | Expected result count | Browser-observed count | Status |
|---|---:|---:|---|
| Root cause category | 4 | 4 | PASS |
| Machine | 4 | 4 | PASS |
| Shift | 3 | 3 | PASS |
| All dimensions | 11 | 11 | PASS |

### 3.1 Root Cause Category

Observed groups and total downtime:

| Group | Total downtime (minutes) |
|---|---:|
| Mechanical | 1265 |
| Electrical | 950 |
| Maintenance | 360 |
| Operational | 220 |

### 3.2 Machine

Observed groups and total downtime:

| Group | Total downtime (minutes) |
|---|---:|
| MCH-02 | 850 |
| MCH-04 | 700 |
| MCH-01 | 635 |
| MCH-03 | 610 |

### 3.3 Shift

Observed groups and total downtime:

| Group | Total downtime (minutes) |
|---|---:|
| Morning | 1060 |
| Evening | 935 |
| Night | 800 |

## 4. Supporting Evidence Verification

| Test | Observed result | Status |
|---|---|---|
| Evidence updates with root-cause filter | Matching root-cause evidence displayed | PASS |
| Evidence updates with machine filter | Matching machine evidence displayed | PASS |
| Evidence updates with shift filter | Matching shift evidence displayed | PASS |
| Grouping dimension | Matches selected analytical category | PASS |
| Incident counts and comparative metrics | Displayed for filtered results | PASS |
| Synthetic-data limitation | Displayed with evidence | PASS |

## 5. Frontend Quality Checks

| Check | Command | Result |
|---|---|---|
| ESLint | `npm run lint` | PASS Ã¢â‚¬â€ exit code 0 |
| TypeScript | `npx tsc --noEmit` | PASS Ã¢â‚¬â€ exit code 0 |
| Production build | `npm run build` | PASS Ã¢â‚¬â€ exit code 0 |
| Next.js compilation | Production build | PASS |
| Static page generation | `/data-intelligence` | PASS |
| Production server startup | `npm run start -- -p 3001` | PASS |

## 6. Approved Analytical Findings Regression

The displayed key findings match the approved Post #3 analytical baseline:

| Dimension | Highest-ranked group | Total downtime (minutes) | Incident count |
|---|---|---:|---:|
| Root cause category | Mechanical | 1265 | 10 |
| Machine | MCH-02 | 850 | 8 |
| Shift | Morning | 1060 | 11 |

No analytical source values or backend analytical outputs were changed as part of the dimension-filter UI update.

## 7. Responsible Use and Limitations

The application displays synthetic demonstration incidents.

Results are descriptive comparative intelligence only. They must not be interpreted as causal relationships, predictive evidence, or actual industrial performance.

Small group sizes may affect ranking stability.

## 8. Final Verification and Lighthouse Audit

| Verification item | Status | Evidence / notes |
|---|---|---|
| All dimensions filter | PASS | 11 ranked results and supporting evidence displayed |
| Root cause category filter | PASS | 4 comparison groups; ranked results and supporting evidence synchronized |
| Machine filter | PASS | 4 comparison groups; ranked results and supporting evidence synchronized |
| Shift filter | PASS | 3 comparison groups; ranked results and supporting evidence synchronized |
| Operational-page regression | PASS | See docs/OPERATIONAL_PAGE_REGRESSION_REPORT.md |
| Responsive-layout verification | PASS | Desktop 1440 px, tablet 768 px, and mobile 390 px checked |
| Lighthouse Performance | PASS | Score: 100 |
| Lighthouse Accessibility | PASS | Score: 100; no automated accessibility failures |
| Lighthouse Best Practices | PASS | Score: 100 |
| Lighthouse SEO | PASS | Score: 100 |
| Manual accessibility review | VERIFIED WITH OBSERVATION | All 10 items reviewed; Check 8 screen-reader follow-up completed with observation |

### Lighthouse Audit Details

- Audit URL: `http://localhost:3001/data-intelligence`
- Audit date: 2026-11-09, 11:35 AM (GMT+5:30)
- Lighthouse version: 13.5.0
- Device profile: Desktop
- Automated accessibility failures: 0
- The IndexedDB notice was reported as a performance-audit warning; all four category scores were 100.

### Manual Accessibility Review Results - 2026-11-09

| No. | Lighthouse manual review item | Result | Evidence / notes |
|---:|---|---|---|
| 1 | Interactive controls are keyboard focusable | PASS | Tab reaches the navigation link and dimension selector; visible focus indicator observed |
| 2 | Interactive elements indicate purpose and state | PASS | Selected dimension is visible and results update accordingly |
| 3 | Logical tab order | PASS | Keyboard navigation follows the page from top to bottom |
| 4 | Visual order follows DOM order | PASS | Browser review confirmed the visual and reading order |
| 5 | Focus is not accidentally trapped | PASS | Tab navigation moves freely through interactive elements |
| 6 | Focus remains usable after content updates | PASS | Results update after changing the dimension; focus remains visible and usable |
| 7 | HTML5 landmark elements | PASS | Refreshed production DOM: main=1, navigation=1, footer=1 |
| 8 | Offscreen content and assistive technology | PASS WITH OBSERVATION | Native option elements and Next.js route announcer observed. Windows Narrator confirmed navigation, dropdown labelling, table headings and values, and all four dropdown options. No issue observed in tested interactions |
| 9 | Custom controls have associated labels | PASS | Dimension select has an associated HTML label and id result-dimension |
| 10 | Custom controls expose appropriate roles | PASS | Native anchor and select controls provide implicit semantic roles |

**Check 8 follow-up:** Completed on 2026-11-09 using Windows Narrator. Tested navigation, dropdown labelling, table announcements, and all four dropdown options. No issue was observed in the tested interactions.
## 9. Current UAT Assessment

**Status: VERIFIED WITH OBSERVATION**

All ten Lighthouse manual accessibility review items have been reviewed and recorded. Nine checks passed. Check 8 is PASS WITH OBSERVATION. Windows Narrator confirmed the navigation link, labelled dropdown, results table headings and values, and all four dropdown options. No issue was observed in the tested interactions.

The navigation landmark remediation was verified in the refreshed production browser. The DOM reported main=1, navigation=1, and footer=1. ESLint, TypeScript, and the production build also passed after the change.

The Lighthouse audit recorded scores of 100 for Performance, Accessibility, Best Practices, and SEO, with zero automated accessibility failures.

The Check 8 screen-reader follow-up is complete. Accessibility sign-off is recorded as VERIFIED WITH OBSERVATION; the observation about offscreen native options and the Next.js route announcer is retained.

## 10. Automated Backend API and Contract Tests

**Execution date:** 2026-11-09
**Test command:** `py -m pytest .\backend\tests\test_intelligence_api.py -q`

| Test area | Coverage | Result |
|---|---|---|
| Approved package loader | Approved versions, quality status and 11 results | PASS |
| Missing results file | Loader failure handling | PASS |
| Invalid JSON | Malformed package rejection | PASS |
| Version mismatch | Summary and results version consistency | PASS |
| Invalid result value | Negative result rejection | PASS |
| Duplicate result IDs | Result identity validation | PASS |
| Result count mismatch | Summary and results consistency | PASS |
| Summary API | HTTP 200 and expected result count | PASS |
| Results API | HTTP 200 and 11 results | PASS |
| Metadata API | Data version, method version and quality status | PASS |
| Health API | Healthy status and metadata | PASS |
| Result detail API | RES-0001 lookup | PASS |
| Unknown result | HTTP 404 | PASS |
| Invalid package API handling | HTTP 503 | PASS |

**Execution result:** 14 passed, 0 failed, 1 deprecation warning, in 5.71 seconds.

**Evidence file:** `backend/tests/test_intelligence_api.py`

**Scope note:** These are backend loader, contract and API tests. They do not establish completion of frontend UI tests or the full Selenium journey.
