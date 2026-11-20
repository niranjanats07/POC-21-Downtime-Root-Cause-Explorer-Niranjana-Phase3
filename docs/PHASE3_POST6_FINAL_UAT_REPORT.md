# Phase 3 Post #6 â€” Final User Acceptance Testing Report

## 1. Document Control

| Attribute | Value |
|---|---|
| Project | POC-21 â€” Downtime Root Cause Explorer |
| Certification | Phase 3 â€” Post #6 |
| Report date | 2026-11-17 |
| Environment | Production Render deployment and local certification environment |
| Frontend | https://downtime-frontend-phase3.onrender.com |
| Data Intelligence | https://downtime-frontend-phase3.onrender.com/data-intelligence |
| Backend | https://downtime-backend-phase3.onrender.com |
| Data version | 1.1.0 |
| Method version | 1.0.0 |
| Approved analytical track | Track A â€” Comparative Intelligence |

## 2. Purpose and Scope

This report records the Post #6 final UAT checks performed against the Operational Dashboard, Data Intelligence page and Grounded Data Assistant.

The purpose is to verify that approved intelligence outputs are displayed consistently, that the existing operational experience remains available, and that important loading, error, retry and empty-result states behave as expected.

This report supplements, and does not overwrite, the historical Post #4 and Post #5 UAT records.

## 3. Test Environment and Approved Data

| Item | Observed value |
|---|---|
| Production frontend | Render |
| Production backend | Render |
| Data version | 1.1.0 |
| Method version | 1.0.0 |
| Analytical validation | PASS |
| Intelligence results | 11 |
| Validated results | 11 |
| Source incidents | 30 |
| Total observed downtime | 2,795 minutes |
| Total failure frequency | 65 |
| Source data classification | Synthetic |

The approved output was not regenerated during these UAT checks.

## 4. Operational Dashboard Acceptance

The Operational Dashboard regression was completed separately under Step 9.

Observed production values included:

- 30 incidents.
- 2,795 total downtime minutes.
- MCH-02 ranked highest at 850 minutes.
- Machine and shift filters returned the expected results.
- Operational navigation and existing dashboard functionality remained available.

Detailed evidence: `docs/FINAL_OPERATIONAL_REGRESSION_REPORT.md`.

**Result: PASS â€” Step 9 evidence.**

## 5. Data Intelligence Acceptance

| Test | Expected result | Observed result | Status |
|---|---|---|---|
| Page loading | Approved intelligence page renders | Data Intelligence page rendered | PASS |
| Data version | Version 1.1.0 | 1.1.0 | PASS |
| Method version | Version 1.0.0 | 1.0.0 | PASS |
| Analytical validation | PASS | PASS | PASS |
| Result count | 11 approved results | 11 | PASS |
| Validated result count | 11 | 11 | PASS |
| Source incidents | 30 | 30 | PASS |
| Comparative findings | Approved findings displayed | Mechanical 1,265 min; MCH-02 850 min; Morning 1,060 min | PASS |
| Ranking table | All approved groups displayed | 11 ranked results displayed | PASS |
| Synthetic-data limitation | Responsible-use warning displayed | Displayed throughout comparison and evidence sections | PASS |
| Freshness | Stale approved output identified | Stale warning displayed for 2026-11-07 generation | PASS |

The stale-data warning is an expected freshness observation. It was not suppressed by regenerating approved outputs.

**Result: PASS.**

## 6. Responsive and Keyboard Checks

| Test | Procedure | Observed result | Status |
|---|---|---|---|
| Mobile viewport | Chrome viewport set to 375 Ã— 667 | Heading, description, metadata cards and navigation remained visible; results table could scroll horizontally without page overflow | PASS |
| Keyboard focus visibility | Tab and Shift+Tab navigation | Visible keyboard focus outline observed | PASS |

These are targeted manual checks. They do not constitute a complete WCAG accessibility audit, screen-reader audit or exhaustive device/browser compatibility test.

**Result: PASS â€” limited manual scope.**

## 7. API Error and Retry Acceptance

The production Data Intelligence results request was temporarily blocked using Chrome DevTools Network request blocking.

| Test | Expected result | Observed result | Status |
|---|---|---|---|
| Normal API loading | Summary, results and metadata load | Normal requests returned HTTP 200 | PASS |
| Results API failure | Clear error state displayed | Data Intelligence unavailable panel and diagnostic reference displayed | PASS |
| Retry while blocked | Failed request attempted again | Retry re-attempted the blocked results request; error remained visible | PASS |
| Restore API access | Normal page loads after unblocking | Normal requests returned HTTP 200 and page recovered | PASS |

**Result: PASS.**

## 8. Empty-Results Acceptance

A temporary browser-only `window.fetch` interception returned an HTTP 200 response containing an empty JSON array for the intelligence results endpoint.

| Test | Expected result | Observed result | Status |
|---|---|---|---|
| Empty response | Results count becomes zero | Intelligence Results 0; Validated Results 0 | PASS |
| Empty table | No-results state appears | `No intelligence results match this selection.` displayed | PASS |
| Empty comparisons | No-result messages appear | Messages displayed for root-cause categories, machines and shifts | PASS |
| Clear filters control | Control is available in empty state | Clear filters button displayed | PASS |
| Independent clear-filter reset | Active filter resets to All dimensions while interception remains active | Active filter changed from Machine to All dimensions; empty response remained active as expected | PASS |
| Restore normal browser state | Real API results return | Full page reload restored 11 results and 11 validated results | PASS |

The Clear filters control was tested with Machine active and the empty-results interception enabled. Clicking it reset the active filter to All dimensions while the empty response remained active. A subsequent reload restored all 11 approved results.

The temporary interception was removed by a full page reload. The approved production API response was restored.

**Result: PASS.**

## 9. Grounded Data Assistant Acceptance

Supporting report: `docs/PHASE3_LIVE_GEMINI_VERIFICATION_REPORT.md`.

| Test | Observed result | Status |
|---|---|---|
| Live Gemini execution | Generated explanation returned | PASS |
| Deterministic retrieval | MCH-02 identified as highest-downtime machine | PASS |
| Approved comparison | 850 minutes across 8 incidents | PASS |
| Evidence grounding | RES-0005 through RES-0008 returned | PASS |
| Deterministic answer preservation | Deterministic result remained authoritative | PASS |
| Responsible use | Synthetic-data and descriptive-only limitations retained | PASS |
| Metadata | Data 1.1.0, method 1.0.0, validation PASS | PASS |

Historical Post #5 UAT also records missing-key and API-error fallback checks. Post #5 maintainer approval is not asserted by this report.

## 10. Automated Test Evidence

The consolidated automated suite completed under Step 12.

Command:

`python -m pytest .\backend\tests .\tests\test_assistant_selenium.py .\tests\test_data_intelligence.py .\tests\test_phase3_final_journey_selenium.py -v -s`

Observed result:

- 64 passed.
- 0 failed.
- 1 warning.
- Duration: 55.98 seconds.

Warning: Starlette reports a deprecation concerning use of httpx with `starlette.testclient`. It was recorded and not silently suppressed.

Detailed report: `docs/PHASE3_AUTOMATED_TEST_REPORT.md`.

## 11. Selenium and Screenshot Evidence

Final journey report: `docs/PHASE3_FINAL_SELENIUM_REPORT.md`.

Evidence directory: `docs/evidence/13-final-selenium/`

- `post6-01-operational-dashboard.png`
- `post6-02-data-intelligence.png`
- `post6-03-return-operational-dashboard.png`

Additional final UAT screenshot:

`docs/evidence/14-final-uat/post6-14-uat-data-intelligence-restored.png`

The additional screenshot was captured on 2026-11-17 at 21:41:10. PowerShell confirmed that the file exists, is a valid PNG, and has dimensions 1366 Ã— 768. The user visually confirmed that it shows the Data Intelligence page, 11 results and validation PASS.

## 12. Limitations and Outstanding Items

1. The approved analytical output is stale and the application correctly warns users.
2. The source incidents are synthetic and cannot establish actual industrial performance.
3. The results are descriptive, not causal or predictive.
4. Clear filters independently reset Machine to All dimensions while interception remained active â€” PASS.
5. Keyboard focus visibility was checked, but a complete accessibility audit was not performed.
6. The single mobile viewport check does not establish compatibility across all devices.
7. The Starlette/httpx deprecation warning remains recorded for future dependency maintenance.
8. Post #5 maintainer approval is not established by this UAT report.
9. No deployment, release tag, Git commit or GitHub submission is authorized by this report.

## 13. Final UAT Assessment

| Area | Assessment |
|---|---|
| Operational Dashboard | PASS |
| Data Intelligence | PASS |
| Responsive mobile check | PASS â€” limited scope |
| Keyboard focus visibility | PASS â€” limited scope |
| API error handling | PASS |
| API retry handling | PASS |
| Empty-results display | PASS |
| Clear filters independent reset | PASS â€” reset to All dimensions |
| Normal API restoration | PASS |
| Grounded Data Assistant | PASS â€” supporting evidence |
| Automated test suite | PASS â€” 64 passed |

### UAT status

**TECHNICAL UAT PASS**

The observed acceptance checks support the technical behaviour documented above. The Clear filters reset behaviour was independently verified. The normal API response was restored with 11 results and 11 validated results.

Formal reviewer/maintainer sign-off remains separate from these technical observations.

## 14. Evidence Traceability

| Evidence | Path |
|---|---|
| Operational regression | `docs/FINAL_OPERATIONAL_REGRESSION_REPORT.md` |
| Data Intelligence validation | `docs/FINAL_DATA_INTELLIGENCE_VALIDATION.md` |
| Live Gemini verification | `docs/PHASE3_LIVE_GEMINI_VERIFICATION_REPORT.md` |
| Automated test report | `docs/PHASE3_AUTOMATED_TEST_REPORT.md` |
| Final Selenium report | `docs/PHASE3_FINAL_SELENIUM_REPORT.md` |
| Selenium screenshots | `docs/evidence/13-final-selenium/` |
| Final UAT screenshot | `docs/evidence/14-final-uat/post6-14-uat-data-intelligence-restored.png` |
| Historical assistant UAT | `docs/ASSISTANT_UAT.md` |
| Historical Data Intelligence UAT | `docs/PHASE3_DATA_INTELLIGENCE_UAT.md` |

---

**Document status: TECHNICAL UAT RECORDED â€” REVIEW SIGN-OFF PENDING**

## 15. Focused Professional UI/UX Enhancement — 2026-11-20

Following maintainer acceptance of the technical Phase 3 implementation, a focused demonstration-experience enhancement was validated.

### Enhancement acceptance observations

| Area | Observed result | Status |
|---|---|---|
| Operational Dashboard | Compact filters and primary operational views retained in the desktop layout | PASS — manual check |
| Data Intelligence | Validated findings, comparisons and visualizations presented | PASS — manual check |
| Investigation workflow | Machine, root-cause and finding selection exposes supporting evidence and incident context | PASS — manual check |
| Grounded explanation | Gemini explanation uses approved analytical evidence; deterministic result remains authoritative | PASS — manual check |
| Responsive experience | Desktop and mobile layouts manually checked | PASS — manual check |
| Technical safeguards | No new analytical model, forecasting, frontend recalculation or unsupported finding introduced | PASS — scope review |

These observations are limited to the stated manual checks and do not constitute a complete accessibility or cross-device certification.

### Fresh automated browser regression — 2026-11-20

The final Selenium journey was rerun against the local frontend after the UI/UX enhancement.

- Target: `http://localhost:3000`
- Browser: Google Chrome 157.0.8103.79
- ChromeDriver: 157.0.8103.78
- Result: 1 passed, 0 failed
- Duration: 67.15 seconds

The journey verified Operational Dashboard access, Data Intelligence navigation, approved metadata visibility, Grounded Data Assistant presence and return navigation.

Fresh screenshots:
- `docs/evidence/13-final-selenium/post6-01-operational-dashboard.png`
- `docs/evidence/13-final-selenium/post6-02-data-intelligence.png`
- `docs/evidence/13-final-selenium/post6-03-return-operational-dashboard.png`

The screenshot files were verified as non-empty and captured on 2026-11-20.

Detailed execution record: `docs/PHASE3_FINAL_SELENIUM_REPORT.md`.

### Scope and release boundary

The approved Track A outputs, data version 1.1.0 and method version 1.0.0 remain the analytical source of truth. The stale-data warning and synthetic-data, descriptive-only limitations remain visible.

This is local UI/UX regression evidence. It does not establish that these latest local changes have been deployed to the production URL, committed, pushed, or approved by the reviewer.

**Focused UI/UX local regression: PASS — reviewer acceptance pending.**

## 16. Verified Mobile-Viewport Browser Evidence — 2026-11-20

A Selenium browser capture used Chrome DevTools viewport emulation at 390 × 844 CSS pixels against the local frontend.

| Check | Result |
|---|---|
| Operational Dashboard route | Captured |
| Data Intelligence route | Captured |
| Viewport width | 390 px |
| Viewport height | 844 px |
| Document width | 390 px |
| Horizontal document overflow | None |
| Screenshot files | Both non-empty |
| Browser capture | PASS |

Evidence:
- `docs/evidence/13-final-selenium/post6-04-operational-dashboard-mobile.png`
- `docs/evidence/13-final-selenium/post6-05-data-intelligence-mobile.png`

This is emulated mobile-viewport browser evidence, not a physical-device test or full cross-device certification. It was captured against the local frontend and does not establish production deployment.

**Mobile-viewport capture: PASS — reviewer acceptance pending.**
