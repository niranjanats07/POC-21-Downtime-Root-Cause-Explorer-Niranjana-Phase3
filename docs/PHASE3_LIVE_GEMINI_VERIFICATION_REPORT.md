# Phase 3 Live Gemini Deployment Verification

## Project
- Project: POC-21 — Downtime Root Cause Explorer
- Certification: Phase 3 — Post #6
- Verification Date: 2026-11-16
- Environment: Production deployment on Render
- Backend: https://downtime-backend-phase3.onrender.com
- Frontend: https://downtime-frontend-phase3.onrender.com/data-intelligence

## Deployment Verification
- Render deployment status: LIVE
- Backend startup: PASS
- Application startup complete: PASS
- Health endpoint: HTTP 200 OK
- Deployment became live: 2026-11-16 14:04:29 UTC

## Live Assistant Test
- Assistant mode: Mode B — Grounded Gemini explanation
- Test question: Which machine ranks highest by downtime?
- Deterministic retrieval: PASS
- Gemini explanation status: Generated
- Live Gemini explanation: PASS

## Verified Answer
The assistant identified MCH-02 as the highest-ranked machine by total downtime.

| Rank | Machine | Downtime | Incidents | Evidence |
|---|---|---:|---:|---|
| 1 | MCH-02 | 850 minutes | 8 | RES-0005 |
| 2 | MCH-04 | 700 minutes | 7 | RES-0006 |
| 3 | MCH-01 | 635 minutes | 8 | RES-0007 |
| 4 | MCH-03 | 610 minutes | 7 | RES-0008 |

## Grounding and Responsible Use
- Four evidence references were returned.
- Evidence measurements matched the approved Track A comparison results.
- The explanation did not replace the deterministic answer.
- The response retained the synthetic-data limitation.
- No causal or predictive claim was made.
- The deterministic result and evidence remain authoritative.

## Data and Method Metadata
- Data version: 1.1.0
- Method version: 1.0.0
- Analytical validation: PASS
- Intelligence result count: 11
- Validated result count: 11
- Source incidents: 30
- Approved track: TRACK A - COMPARATIVE INTELLIGENCE

## Freshness Observation
The approved analytical output was generated at 2026-11-07T09:53:54Z. The live page correctly displays a stale-data warning because the output is older than seven days.

The approved analytical outputs were not regenerated as part of this live assistant test.

## Result
**Live Gemini explanation: PASS**

**Deterministic retrieval and evidence grounding: PASS**

**Freshness: OBSERVATION — approved output is stale**

This verification records the live behavior observed in the production page on 2026-11-16. It does not expose or record secret environment-variable values.
