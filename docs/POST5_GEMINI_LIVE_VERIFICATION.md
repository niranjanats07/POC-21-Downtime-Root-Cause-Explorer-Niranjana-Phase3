# Post #5 — Gemini Mode B Live Verification Evidence

## Execution Details

- Date: 2026-11-15
- Integration mode: Mode B — Deterministic Retrieval + LLM Explanation
- Gemini model configured: `gemini-3.5-flash-lite`
- Backend endpoint: `POST /api/assistant/query`
- Execution environment: Local backend (`127.0.0.1:8000`)
- API key handling: Entered securely through a masked PowerShell prompt; not recorded in this document.

## Live API Test

**Question:**

`Why is MCH-02 ranked first for downtime?`

**Result: PASS — Real Gemini response received**

- API response status: `answered`
- Gemini status: `generated`
- Intent: `describe_segment`

### Deterministic Answer

Machine comparison by observed downtime: #1 MCH-02: 850 minutes (RES-0005).

### Gemini Explanation

MCH-02 ranks first for downtime because it accumulated 850.0 downtime minutes across 8 complete incidents, as documented in evidence RES-0005.

The explanation also preserved the approved measurements:

| Measurement | Value |
|---|---:|
| Total downtime | 850 minutes |
| Complete incidents | 8 |
| Average downtime | 106.25 minutes |
| Total failure frequency | 20 |
| Average failure frequency | 2.5 |

### Evidence and Metadata

- Evidence reference: `RES-0005`
- Result type: `comparative_group_ranking`
- Group: `MCH-02`
- Priority rank: `1`
- Data version: `1.1.0`
- Method version: `1.0.0`
- Quality status: `PASS`

### Limitation Preserved

All source incidents are synthetic. These results are descriptive demonstration outputs only; they do not establish causation, prediction or actual industrial performance.

## Frontend Verification

The Data Intelligence page output was inspected separately.

**Result: PASS — Gemini explanation displayed in the UI**

The inspected page showed:

- Deterministic grounded answer.
- Gemini explanation with status `Generated`.
- Four machine evidence references: `RES-0005` through `RES-0008`.
- Supporting downtime and incident measurements.
- Interpretation limitation explaining the synthetic-data boundary.
- Data version `1.1.0`, method version `1.0.0`, and quality `PASS`.

The frontend comparison question was:

`Which machine ranks highest by downtime?`

The displayed deterministic comparison ranked:
1. MCH-02 — 850 minutes across 8 incidents.
2. MCH-04 — 700 minutes across 7 incidents.
3. MCH-01 — 635 minutes across 8 incidents.
4. MCH-03 — 610 minutes across 7 incidents.

The UI also displayed the Gemini explanation and supporting evidence for these four results.

## Data Freshness Note

The approved analytical output metadata reports:

`generated_at: 2026-11-07T09:53:54Z`

The Data Intelligence page displays a stale-data warning because the approved output is older than seven days.

This warning was preserved and recorded. No approved analytical output, canonical dataset, or Track A calculation was regenerated as part of this Gemini verification.

## Security Notes

- The API key was not included in the request body.
- The API key was not printed or saved in this evidence document.
- The key was supplied through the backend environment.
- No frontend API key exposure is asserted by this test alone.

## Scope and Remaining Validation

This evidence establishes one successful real Gemini API execution and a separate frontend display verification.

It does not by itself establish:
- Complete missing-key, quota, timeout and invalid-response fallback verification.
- Full regression test success after the latest Gemini model change.
- Final maintainer approval of Phase 3 Post #5.

Existing deterministic assistant behavior and approved Track A outputs must remain unchanged.

## Approval Status

**Gemini live execution: PASS**

**Frontend Gemini display: PASS**

**Phase 3 Post #5 final closeout: Pending remaining validation and maintainer review.**

## Targeted Regression Test Results

- Date: 2026-11-15
- Command: `py -m pytest .\backend\tests\test_assistant.py .\backend\tests\test_gemini_explainer.py -v`
- Assistant tests: 21 passed
- Gemini explainer tests: 8 passed
- Total: **29 passed, 0 failed**
- Duration: 0.36 seconds

The tests verified deterministic assistant behavior, approved ranking preservation, evidence validation, version and quality checks, safe fallback behavior, Gemini response validation, and preservation of deterministic answers when Gemini fails.

**Targeted regression status: PASS**

## Full Backend Regression Test Results

- Date: 2026-11-15
- Command: `py -m pytest .\backend\tests -v`
- Assistant tests: 21 passed
- Gemini explainer tests: 8 passed
- Data Intelligence API tests: 14 passed
- Total: **43 passed, 0 failed**
- Duration: 2.65 seconds
- Warnings: 1 Starlette deprecation warning from the test-client dependency; no test failures.

**Full backend regression status: PASS**

## Frontend Regression and Production Build

- Date: 2026-11-15
- TypeScript command: `npx tsc --noEmit`
- TypeScript result: **PASS** — no compiler errors.
- Production build command: `npm run build`
- Production build result: **PASS** — Next.js 16.4.3 compiled successfully.
- Static routes generated:
  - `/`
  - `/_not-found`
  - `/data-intelligence`

**Frontend verification status: PASS**

## Live Missing-Key Fallback Verification

- Date: 2026-11-15
- Temporary backend: `http://127.0.0.1:8001` (no Gemini API key configured)
- Question: `Why is MCH-02 ranked first for downtime?`
- API response status: `answered`
- Gemini status: `fallback_missing_key`
- Deterministic answer preserved: MCH-02 ranked #1 with 850 minutes
- Evidence reference preserved: `RES-0005`
- Data version: `1.1.0`; method version: `1.0.0`; quality: `PASS`
- Gemini explanation: `null`

**Result: PASS — Live missing-key fallback preserved the deterministic answer and evidence.**

## Live API-Error Fallback Verification

- Date: 2026-11-15
- Temporary backend: `http://127.0.0.1:8002`
- Test configuration: Deliberately invalid placeholder API key; real key was not used
- Question: `Why is MCH-02 ranked first for downtime?`
- API response status: `answered`
- Gemini status: `fallback_error`
- Deterministic answer preserved: MCH-02 ranked #1 with 850 minutes
- Evidence reference preserved: `RES-0005`
- Data version: `1.1.0`; method version: `1.0.0`; quality: `PASS`
- Gemini explanation: `null`

**Result: PASS — Live API-error fallback preserved the deterministic answer and evidence.**
