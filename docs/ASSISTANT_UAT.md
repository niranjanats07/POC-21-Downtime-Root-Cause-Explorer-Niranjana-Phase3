# Assistant User Acceptance Testing — Post #5

## Functional cases
- Ask which category ranks highest.
- Ask which machine ranks highest.
- Ask which shift ranks highest.
- Compare machines, categories and shifts.
- Explain a valid result and show its evidence.
- Ask for methodology, limitations and freshness.
- Verify data version 1.1.0 and method version 1.0.0 when those are the loaded approved package versions.

## Negative cases
- Empty and over-500-character questions.
- Ambiguous and missing parameters.
- Unsupported trends and predictions.
- Unknown result IDs.
- Unsafe requests for secrets, prompts, arbitrary SQL or code.
- Prompt-injection wording in question and evidence.
- Version mismatch and unavailable source package.

## UI checks
- Suggested questions are visible.
- Loading, answered, unsupported, unsafe and unavailable states are clear.
- Evidence references and limitations are displayed.
- Keyboard access and responsive layouts work.
- Operational View and Data Intelligence remain available.
- Existing Post #4 behavior is unchanged.

## Acceptance evidence
Record each test, expected result, actual result, pass/fail, command, timestamp and screenshot path.

## Final status
Use exactly one guide outcome:
- GROUNDED DATA ASSISTANT APPROVED
- GROUNDED DATA ASSISTANT CHANGES REQUIRED
- ASSISTANT NOT SUITABLE — APPROVED SKIP
- ASSISTANT INTEGRATION BLOCKED

Post #5 requires maintainer review; do not claim approval before it is granted.

## Browser regression evidence — 2026-11-13

Test environment:
- Frontend: local Next.js development server at `http://127.0.0.1:3000`.
- Backend: local FastAPI server at `http://127.0.0.1:8000`.
- Test method: manual browser verification; results supplied from the rendered pages.

| Test | Expected result | Observed result | Status |
|---|---|---|---|
| Data Intelligence route | Page renders approved Track A intelligence | Data version 1.1.0, method version 1.0.0, validation PASS, 11 results and 30 source incidents displayed | PASS |
| Machine dimension filter | Only machine comparison rows are displayed | MCH-02 850 min, MCH-04 700 min, MCH-01 635 min, MCH-03 610 min | PASS |
| Track A evidence | Machine results show their approved evidence | Four machine results displayed with ranks, incident counts and evidence measurements | PASS |
| Grounded Assistant visibility | Assistant appears on Data Intelligence page | Mode A deterministic assistant and suggested questions displayed | PASS |
| Assistant browser query | Machine ranking answer is grounded in approved results | MCH-02 ranked first at 850 minutes; four evidence references RES-0005 through RES-0008 displayed | PASS |
| Assistant limitation display | Synthetic-data limitation is visible | Descriptive-only and non-causal/non-predictive limitation displayed | PASS |
| Operational Dashboard navigation | Original Post #4 dashboard remains accessible | Operational Dashboard opened and displayed its KPI cards, filters, charts/analysis sections, heatmap and 30-incident table | PASS |

### Checks not covered by this browser evidence

- Visual correctness and interaction of every individual chart.
- CSV and JSON download behavior.
- Responsive layout at tablet and mobile sizes.
- Browser console error inspection.

These items remain pending unless separately verified and recorded.

### Browser regression outcome

The observed browser checks support that the Post #5 Data Intelligence page and assistant render and that navigation back to the Post #4 Operational Dashboard remains available. This is local browser evidence only; it does not establish live Render deployment verification or maintainer approval.
## Additional manual browser regression evidence — 2026-11-13

The following checks were completed after the earlier browser regression record. Evidence was user-confirmed during local browser testing.

| Test | Observed result | Status |
|---|---|---|
| Pareto chart | Rendered in Operational Dashboard | PASS |
| Downtime by Machine chart | Rendered in Operational Dashboard | PASS |
| Failure Frequency vs Downtime scatter chart | Rendered in Operational Dashboard | PASS |
| Root Cause Tree | Rendered in Operational Dashboard | PASS |
| Machine/Shift heatmap | Rendered in Operational Dashboard | PASS |
| MCH-01 filter | 8 incidents and 635 downtime minutes displayed | PASS |
| CSV download | User confirmed download completed | PASS |
| JSON download | User confirmed download completed; supplied export contained 7 MCH-04 records | PASS |
| Mobile viewport | User confirmed responsive layout checked | PASS |
| Tablet viewport | User confirmed responsive layout checked | PASS |
| Browser console snippet | Supplied output showed HMR/Fast Refresh messages and no visible red errors | PASS — limited snippet only |

### Evidence limitations

- These are manual, user-confirmed local browser checks.
- They are not automated Selenium test results.
- Chart rendering was checked; exhaustive interaction testing for every chart is not claimed.
- Browser-console evidence covers only the supplied snippet, not a complete console audit.
- Live Render assistant verification remains NOT VERIFIED.
- Post #5 maintainer approval remains PENDING.

### Updated UAT interpretation

The earlier pending list is superseded by the additional manual checks above where explicitly marked PASS. These checks do not establish live deployment, production readiness, or maintainer approval.