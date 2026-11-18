# Phase 3 User Acceptance Testing (UAT)
## PoC 21 â€” Downtime Root Cause Explorer

**Project:** Infocreon Internship â€” Downtime Root Cause Explorer
**PoC ID:** 21
**Developer:** Niranjana T Suresh
**GitHub:** @niranjanats07
**Batch:** Batch 8 / MA College
**Phase:** Phase 3 â€” Data Intelligence Page Integration
**Approved Track:** Track A â€” Comparative Intelligence
**Data Version:** 1.1.0
**Method Version:** 1.0.0

---

## 1. Purpose

This report records the User Acceptance Testing performed for the separate Phase 3 Data Intelligence page.

The existing Phase 2 Operational Dashboard is preserved. The Data Intelligence page consumes the approved Track A outputs and does not independently recalculate analytical results in the frontend.

## 2. Test Environment

- Frontend: Next.js, React, TypeScript, Tailwind CSS
- Backend: FastAPI, Python
- Frontend URL: http://localhost:3001
- Backend URL: http://localhost:8000
- Data: Approved Track A synthetic demonstration outputs
- Browser automation: Selenium with pytest
- Container build: Not verified

## 3. Approved Data and Integration Files

The integration uses these approved analytical outputs:

- `data-science/outputs/intelligence_results.json`
- `data-science/outputs/intelligence_summary.json`
- `data-science/outputs/validation_metrics.json`

Supporting source and contract files:

- `data/canonical/intelligence_data.csv`
- `data/manifest.json`
- `data/schema.json`
- `docs/INTELLIGENCE_OUTPUT_CONTRACT.md`
- `docs/ANALYTICAL_METHOD_REPORT.md`
- `docs/ANALYTICAL_VALIDATION_REPORT.md`
- `docs/WEAK_CASE_AND_LIMITATION_REVIEW.md`

## 4. UAT Test Results

| ID | Test scenario | Expected result | Actual result / evidence | Status |
|---|---|---|---|---|
| DI-UAT-01 | Open Data Intelligence page | Page loads successfully | Browser page verified | PASS |
| DI-UAT-02 | Navigation | Operational View and Data Intelligence navigation available | Navigation verified | PASS |
| DI-UAT-03 | Approved metadata | Data and method versions displayed | Versions 1.1.0 and 1.0.0 verified | PASS |
| DI-UAT-04 | Validation status | Approved validation status displayed | PASS status verified | PASS |
| DI-UAT-05 | Summary cards | Approved summary values displayed | Summary values verified | PASS |
| DI-UAT-06 | Track A results | Ranking results displayed | Results table verified | PASS |
| DI-UAT-07 | Machine filter | Results respond to machine selection | Filter interaction verified | PASS |
| DI-UAT-08 | Evidence interaction | Supporting evidence opens | Manually verified | PASS |
| DI-UAT-09 | Methodology | Methodology information displayed | Section verified | PASS |
| DI-UAT-10 | Limitations | Synthetic-data limitations displayed | Section verified | PASS |
| DI-UAT-11 | Loading state | Loading indicator displayed while fetching | Browser behavior confirmed by developer | PASS |
| DI-UAT-12 | API error and retry | Error is handled and retry works | Browser behavior confirmed by developer | PASS |
| DI-UAT-13 | Empty state | No-match message and Clear filters work | Browser behavior confirmed by developer | PASS |
| DI-UAT-14 | Stale-data detection | Old or invalid timestamp produces warning | Detection logic verified in source; browser scenario confirmed by developer | PASS |
| DI-UAT-15 | Version mismatch | Unexpected versions are rejected | Detection logic verified in source | PASS |
| DI-UAT-16 | Mobile layout | Page remains usable at mobile viewport | Confirmed by developer | PASS |
| DI-UAT-17 | Accessibility | Keyboard navigation and accessible controls checked | Confirmed by developer | PASS |
| DI-UAT-18 | Operational dashboard regression | Existing dashboard remains functional | Confirmed by developer | PASS |

**Note:** Manual checks marked as developer-confirmed are based on the developer's reported verification. They are not represented as separate automated test cases.

## 5. Automated Test Evidence

### Backend API tests

File: `backend/tests/test_intelligence_api.py`

Result: **14 passed**

### Selenium UI tests

File: `tests/test_data_intelligence.py`

Result: **5 passed**

### Combined test execution

Command:

```powershell
py -m pytest .\backend\tests\test_intelligence_api.py .\tests\test_data_intelligence.py -q
```

Result:

```text
19 passed, 1 warning
0 failures
```

The warning was a Starlette/httpx deprecation warning.

A separate Jest/Vitest frontend unit-test suite was not confirmed. Selenium browser tests were used for UI smoke testing.

## 6. Freshness and Version Validation

The Data Intelligence page implements:

- Expected data version validation.
- Expected method version validation.
- Result-level version validation.
- Generation timestamp validation.
- Configurable stale-data threshold.
- Fresh, Stale, and Unknown freshness states.
- A warning when freshness cannot be verified.

The implementation was inspected in:

`frontend/src/app/data-intelligence/page.tsx`

## 7. Required Supporting Documentation

The following project documentation supports the integration:

- `docs/DATA_INTELLIGENCE_PAGE_PLAN.md`
- `docs/INTELLIGENCE_INTEGRATION_MAPPING.md`
- `docs/INTELLIGENCE_API_CONTRACT.md`
- `docs/DATA_INTELLIGENCE_UI_SPEC.md`
- `docs/DATA_INTELLIGENCE_UAT.md`
- `docs/OPERATIONAL_PAGE_REGRESSION_REPORT.md`
- `docs/PHASE3_DATA_INTELLIGENCE_SELENIUM_EVIDENCE.md`

The Post #4 integration guide used:

`04_INFOCREON_PHASE3_DATA_INTELLIGENCE_PAGE_INTEGRATION_GUIDE.docx`

## 8. Approval and Build Status

| Requirement | Status | Evidence |
|---|---|---|
| Post #3 analytical approval | Confirmed | Maintainer approval reported by developer |
| Post #4 Word guide | Confirmed | Guide requirements used during integration |
| Frontend production build | PASS | Previously completed successfully |
| Frontend lint | PASS | Previously completed successfully |
| Backend and Selenium tests | PASS | 19 combined tests passed |
| Docker container build | NOT VERIFIED | Docker Desktop was closed before successful completion could be confirmed |

## 9. Known Limitations

- The dataset is synthetic demonstration data.
- Findings are descriptive and should not be interpreted as causal or predictive evidence.
- No separate Jest/Vitest frontend test suite was confirmed.
- Docker container build completion has not been verified.
- Manual browser checks are recorded based on developer confirmation.

## 10. Final UAT Assessment

**Phase 3 UAT Status: PASS â€” WITHIN THE VERIFIED SCOPE**

The Data Intelligence page has been integrated as a separate page while preserving the existing Operational Dashboard.

The combined backend and Selenium test execution passed all 19 tests. The developer also confirmed the additional browser checks documented above.

Docker container build completion remains unverified and is not claimed as a successful test.

**Final Post #4 maintainer approval remains subject to review.**

---

**Developed by:** Niranjana T Suresh
**PoC ID:** 21
**GitHub:** @niranjanats07
**Batch:** Batch 8 / MA College
**Infocreon Internship**
