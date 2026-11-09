# Operational Page Regression Report

## 1. Project Information
- Project: POC-21 - Downtime Root Cause Explorer
- Phase: Phase 3 - Post #4 Data Intelligence Integration
- Verification date: 2026-11-09
- Environment: Local Next.js production server and FastAPI backend
- Operational page: http://localhost:3001/

## 2. Regression Objective
Verify that the existing operational dashboard remains functional after integrating the separate Data Intelligence page.

## 3. Application Availability
| Check | Observed result | Status |
|---|---|---|
| Operational page HTTP response | 200 | PASS |
| Dashboard title present | True | PASS |
| Dashboard response length | 8088 characters | PASS |
| Operational dashboard rendered | Confirmed by browser inspection | PASS |
| Data Intelligence navigation | Visible | PASS |

## 4. Initial Dashboard State
| Metric | Observed result | Status |
|---|---:|---|
| Total incidents | 30 | PASS |
| Total downtime | 2795 minutes | PASS |
| Average downtime | 93.2 minutes | PASS |
| Closed incident average | 93.2 minutes | PASS |
| Incident list | 30 of 30 | PASS |

## 5. Machine Filter Verification
Filter: MCH-02
| Check | Observed result | Status |
|---|---:|---|
| Incidents | 8 | PASS |
| Total downtime | 850 minutes | PASS |
| Average downtime | 106.3 minutes | PASS |
| Machine chart | MCH-02 only | PASS |
| Heatmap | MCH-02 only | PASS |
| Incident list | 8 matching incidents | PASS |

## 6. Shift Filter Verification
Filter: Morning, with Machine set to All.
| Check | Observed result | Status |
|---|---:|---|
| Incidents | 11 | PASS |
| Total downtime | 1060 minutes | PASS |
| Average downtime | 96.4 minutes | PASS |
| Machines represented | 4 | PASS |
| Incident list | 11 matching incidents | PASS |

## 7. Root Cause Filter Verification
Filter: Mechanical, with Machine and Shift set to All.
| Check | Observed result | Status |
|---|---:|---|
| Incidents | 10 | PASS |
| Total downtime | 1265 minutes | PASS |
| Average downtime | 126.5 minutes | PASS |
| Machines represented | 4 | PASS |
| Incident list | 10 matching incidents | PASS |

## 8. Reset Filter Verification
| Check | Observed result | Status |
|---|---:|---|
| Total incidents after reset | 30 | PASS |
| Total downtime after reset | 2795 minutes | PASS |
| Average downtime after reset | 93.2 minutes | PASS |
| Machine, shift, severity, root cause and status | All | PASS |

## 9. Dashboard Content Observed
- Downtime Pareto Analysis section present.
- Downtime by Machine values displayed.
- Failure Frequency vs Downtime Duration section present.
- Root Cause Tree section present.
- Machine / Shift Downtime Heatmap values displayed.
- Incident Investigation table displayed.
- CSV and JSON download controls visible; download behavior not tested.

## 10. Data Intelligence Integration Regression
- Separate Data Intelligence navigation is visible.
- Data Intelligence page is accessible at /data-intelligence.
- Approved data version: 1.1.0.
- Approved method version: 1.0.0.
- Validation status: PASS.
- Intelligence result count: 11.
- Source incident count: 30.
- Approved Track A findings were displayed.
- No analytical output changes were made during operational regression testing.

## 11. Verification Limitations
- Severity-only filtering was not separately tested.
- Status-only filtering was not separately tested.
- CSV and JSON downloads were not tested.
- Individual incident investigation actions were not separately tested.
- Pareto, scatter and root-cause-tree visual interactions were not separately tested.
- Browser responsive and accessibility checks remain separate verification items.

## 12. Regression Assessment
RESULT: OPERATIONAL PAGE REGRESSION CHECKS PASSED FOR THE TESTED FLOWS.

The existing operational dashboard loaded successfully and its tested machine, shift, root-cause and reset filter flows returned the observed expected values. The separate Data Intelligence page remained accessible.

This assessment is limited to the checks recorded in this report. It is not a claim that every dashboard control or interaction has been tested.

## 13. Evidence Location
- Operational implementation: frontend/src/app/page.tsx
- Data Intelligence implementation: frontend/src/app/data-intelligence/page.tsx
- Backend implementation: backend/app/main.py
- Approved analytical outputs: data-science/outputs/
- This report: docs/OPERATIONAL_PAGE_REGRESSION_REPORT.md
