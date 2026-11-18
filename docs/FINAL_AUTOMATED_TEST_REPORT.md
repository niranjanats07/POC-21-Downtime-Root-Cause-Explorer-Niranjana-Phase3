# Final Automated Test Report

## 1. Execution Details

| Field | Value |
|---|---|
| Project | POC-21 — Downtime Root Cause Explorer |
| Certification Stage | Phase 3 — Post #6 |
| Execution Date | 2026-11-17 |
| Environment | Windows |
| Python Version | 3.13.15 |
| Pytest Version | 8.4.2 |
| Browser | Google Chrome, headless |
| Automation Framework | Selenium |
| Frontend URL | https://downtime-frontend-phase3.onrender.com |
| Overall Test Result | PASS |

## 2. Consolidated Test Execution

### Command executed

```powershell
$env:DATA_INTELLIGENCE_URL = "https://downtime-frontend-phase3.onrender.com"; python -m pytest .\backend\tests .\tests\test_assistant_selenium.py .\tests\test_data_intelligence.py .\tests\test_phase3_final_journey_selenium.py -v -s
```

### Actual execution result

| Metric | Result |
|---|---:|
| Tests collected | 64 |
| Passed | 64 |
| Failed | 0 |
| Warnings | 1 |
| Execution duration | 55.98 seconds |

**Overall: 64 passed, 0 failed, 1 warning.**

## 3. Test Suite Breakdown

| Test suite | Passed |
|---|---:|
| Backend assistant tests | 21 |
| Gemini explainer tests | 18 |
| Intelligence API tests | 14 |
| Grounded assistant Selenium tests | 5 |
| Data Intelligence UI Selenium tests | 5 |
| Final user journey Selenium test | 1 |
| **Total** | **64** |

## 4. Backend Assistant Validation

The following areas were covered:

- Rejection of unsafe and unsupported requests.
- Enforcement of assistant scope restrictions.
- Preservation of approved machine rankings.
- Rejection of ranking manipulation requests.
- Data-version and method-version mismatch handling.
- Quality failure handling.
- Question length validation.
- Evidence identifier validation.
- Evidence filtering and reference limits.
- Preservation of approved deterministic responses.

**Result: 21 passed.**

## 5. Gemini Explainer Validation

The following areas were covered:

- Missing API key fallback.
- Gemini API error fallback.
- Quota exhaustion handling.
- Successful response acceptance.
- Invalid numerical claim rejection.
- Contradictory machine ranking rejection.
- Machine ranking validation.
- Unsupported causal claim rejection.
- Grounded explanation acceptance.
- Preservation of deterministic responses when Gemini fails.

**Result: 18 passed.**

## 6. Intelligence API Validation

The following areas were covered:

- Approved intelligence package loading.
- Missing results file rejection.
- Invalid JSON rejection.
- Data-version mismatch rejection.
- Negative result value rejection.
- Duplicate result identifier rejection.
- Summary and results count consistency.
- Summary endpoint.
- Results endpoint.
- Metadata endpoint.
- Health endpoint.
- Result detail endpoint.
- Unknown result handling.
- Invalid package handling.

**Result: 14 passed.**

## 7. Browser and UI Validation

### 7.1 Grounded Assistant Selenium

Verified:

- Assistant loading.
- Evidence and version metadata visibility.
- Highest downtime machine response.
- Grounded overall summary.
- Unsupported question handling.

**Result: 5 passed.**

### 7.2 Data Intelligence UI Selenium

Verified:

- Data Intelligence page loading.
- Operational Dashboard navigation.
- Results table visibility.
- Quality status visibility.
- Machine filter interaction.
- Supporting evidence section.
- Methodology section.
- Limitations and responsible-use section.

**Result: 5 passed.**

### 7.3 Final Selenium User Journey

Verified:

1. Operational Dashboard loads.
2. Data Intelligence navigation is available.
3. Data Intelligence page opens.
4. Expected version and quality information is visible.
5. Operational Dashboard navigation works.
6. User returns to the Operational Dashboard.

**Result: 1 passed.**

## 8. Selenium Screenshot Evidence

The final journey generated the following screenshots:

| Screenshot | Evidence path |
|---|---|
| Operational Dashboard | `docs/evidence/13-final-selenium/post6-01-operational-dashboard.png` |
| Data Intelligence | `docs/evidence/13-final-selenium/post6-02-data-intelligence.png` |
| Return to Operational Dashboard | `docs/evidence/13-final-selenium/post6-03-return-operational-dashboard.png` |

These files are retained as Post #6 browser evidence.

## 9. Warning and Maintenance Observation

One warning was reported during test execution:

```text
StarletteDeprecationWarning:
Using httpx with starlette.testclient is deprecated;
install httpx2 instead.
```

Assessment:

- The warning did not cause a test failure.
- All 64 tests passed.
- The warning is recorded for future dependency maintenance.
- No dependency upgrade or unrelated code change was introduced during this certification test run.

## 10. Legacy Test Exclusion

The file below was inspected:

`tests/test_poc.py`

It was excluded from the current consolidated Post #6 test command.

Reason:

- It targets the earlier application deployment URLs.
- It expects the historical 10-incident dataset.
- The current approved Phase 3 application uses the 30-incident operational dataset and a separate Data Intelligence page.

The legacy file was preserved without modification.

Its exclusion is documented and is not represented as a passing test.

## 11. Evidence and Reproducibility

Test source files:

- `backend/tests/test_assistant.py`
- `backend/tests/test_gemini_explainer.py`
- `backend/tests/test_intelligence_api.py`
- `tests/test_assistant_selenium.py`
- `tests/test_data_intelligence.py`
- `tests/test_phase3_final_journey_selenium.py`

Browser screenshots:

- `docs/evidence/13-final-selenium/post6-01-operational-dashboard.png`
- `docs/evidence/13-final-selenium/post6-02-data-intelligence.png`
- `docs/evidence/13-final-selenium/post6-03-return-operational-dashboard.png`

Execution evidence:

- Consolidated pytest terminal output recorded in the Post #6 certification session.
- Actual pytest summary: 64 passed, 0 failed, 1 warning.

## 12. Acceptance Assessment

| Acceptance criterion | Result |
|---|---|
| Backend assistant tests | PASS |
| Gemini explainer tests | PASS |
| Intelligence API tests | PASS |
| Grounded assistant Selenium tests | PASS |
| Data Intelligence UI Selenium tests | PASS |
| Final Selenium navigation journey | PASS |
| Consolidated test execution | PASS |
| Test failures | None in this execution |
| Deprecation warning | Documented |
| Legacy test exclusion | Documented |

## 13. Certification Status

**Step 12 — Full Automated Test Suite: PASS**

The consolidated Post #6 execution completed with 64 passing tests and no failures.

One dependency deprecation warning remains documented.

This report certifies only the test execution described above. It does not independently certify final UAT, deployment configuration, container requirements, the complete evidence pack, handover documentation, release tagging or GitHub submission.

**Overall Phase 3 certification remains PENDING until all 24 mandatory steps are completed and reviewed.**
