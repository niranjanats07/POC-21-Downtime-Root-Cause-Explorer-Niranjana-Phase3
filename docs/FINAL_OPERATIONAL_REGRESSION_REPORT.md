# Final Operational Regression Report

## 1. Validation Details

- Project: POC-21 — Downtime Root Cause Explorer
- Validation Environment: Production Render deployment
- Frontend: https://downtime-frontend-phase3.onrender.com/
- Validation Date: 2026-11-16
- Scope: Existing Phase 2 Operational Dashboard regression
- Report Purpose: Post #6 final certification evidence

## 2. Dashboard and KPI Validation

| Check | Observed Result | Status |
|---|---|---|
| Dashboard loading | Operational Dashboard loaded successfully | PASS |
| Unfiltered incident count | 30 of 30 | PASS |
| Total incidents | 30 | PASS |
| Total downtime | 2,795 minutes | PASS |
| Average downtime | 93.2 minutes | PASS |
| Closed incident average | 93.2 minutes | PASS |
| Machine downtime ranking | MCH-02: 850; MCH-04: 700; MCH-01: 635; MCH-03: 610 minutes | PASS |
| Machine/shift heatmap | Four machines and three shifts displayed | PASS |

## 3. Filter Regression

| Test | Observed Result | Status |
|---|---|---|
| MCH-01 filter | 8 incidents; 635 minutes; average 79.4 | PASS |
| MCH-02 filter | 8 incidents; 850 minutes; average 106.3 | PASS |
| MCH-02 + Morning filter | 3 incidents; 310 minutes; average 103.3 | PASS |
| Reset filters | Restored 30 of 30 incidents and overall KPIs | PASS |

## 4. Incident Investigation

Incident INC001 was opened successfully.

| Field | Observed Value |
|---|---|
| Machine | MCH-01 |
| Date | 2026-01-05 |
| Shift | Morning |
| Downtime | 120 minutes |
| Failure frequency | 3 |
| Root cause | Mechanical |
| Sub-cause | Bearing Failure |
| Severity | High |
| Status | Closed |

The investigation panel displayed the incident description, investigation priority and recommendation. The recommendation included a reminder to validate findings against maintenance records and engineering personnel.

Status: PASS

## 5. Export Validation

- CSV: Download completion was confirmed by the user. File contents were not independently inspected.
- JSON: Export content was provided and inspected.
- JSON export contained 30 incident records with the expected incident fields.
- The displayed JSON records were consistent with the overall dashboard totals: 30 incidents and 2,795 downtime minutes.
- All records shown had status Closed.

| Export Check | Result |
|---|---|
| CSV download confirmation | PASS |
| JSON download/content inspection | PASS |

## 6. Scope and Evidence Boundaries

The following checks are not claimed by this report:

- Final Selenium end-to-end journey.
- Mobile/responsive browser validation.
- Independent inspection of downloaded CSV contents.
- Full automated test-suite execution for Post #6.

These remain separate Post #6 certification activities.

## 7. Overall Result

The production Operational Dashboard passed the browser checks documented in this report. Dashboard loading, KPI display, machine filters, combined machine/shift filtering, reset behaviour, incident investigation and the documented export checks were verified.

No claim is made here that the complete Post #6 certification has passed.

**Operational browser regression: PASS for the checks listed in this report.**
