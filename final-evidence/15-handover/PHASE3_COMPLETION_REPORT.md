# POC-21 — Phase 3 Completion Report

**Project:** Downtime Root Cause Explorer  
**Certification:** Phase 3 — Post #6 Final Certification  
**Repository:** `niranjanats07/POC-21-Downtime-Root-Cause-Explorer-Niranjana-Phase3`  
**Branch:** `main`  
**Baseline commit:** `cab343e58762b5800ed07b12060fc6558e70dd90`  
**Planned release tag:** `phase3-v1.0.0`  
**Application version:** `0.1.0`  
**Canonical data version:** `1.1.0`  
**Analytical method version:** `1.0.0`  
**Approved analytical track:** Track A  
**Report status:** Draft — final certification pending  
**Prepared:** 18 November 2026

---

## 1. Executive Summary

This report consolidates the technical validation and evidence gathered for POC-21 Phase 3 Post #6 final certification.

Phase 3 extends the existing Downtime Root Cause Explorer with a separately accessible Data Intelligence page and a grounded data assistant. The existing Phase 2 Operational Dashboard remains the landing page and is preserved.

The certification work covers the canonical synthetic data foundation, analytical readiness, approved Track A output reproducibility, intelligence API contract, frontend and backend build validation, operational regression, Data Intelligence behavior, assistant grounding and safety, automated tests, Selenium, UAT, deployment, container execution, architecture, and evidence-pack preparation.

The technical validation completed so far is positive. However, the evidence pack and handover documentation still require finalization. The release manifest and final release identity must be reconciled with the certified commit. Final Repomix generation, release tagging, GitHub submission, and reviewer signoff have not yet been completed.

**Current certification status: NOT YET CERTIFIED.**

## 2. Original Phase 2 Product

The original product is the Downtime Root Cause Explorer, a production-style demonstration dashboard for investigating equipment downtime.

The Phase 2 Operational Dashboard remains at `/` and retains its existing operational purpose, including:

- Incident and downtime KPIs.
- Root-cause Pareto analysis.
- Machine downtime comparison.
- Frequency-versus-duration analysis.
- Machine and shift heatmap.
- Root-cause investigation and incident details.

The Phase 2 operational page was not replaced by the Phase 3 Data Intelligence page.

## 3. Phase 3 Objective

Phase 3 adds a separate Data Intelligence experience at:

`/data-intelligence`

The page consumes approved Track A intelligence outputs through validated backend APIs. It presents aggregated findings by root-cause category, machine, and shift, together with rankings, comparisons, evidence references, methodology, data quality, freshness, and limitations.

The Post #5 Grounded Data Assistant provides bounded, evidence-linked answers. Deterministic results remain authoritative; optional Gemini explanations do not create or modify analytical findings.

## 4. Post #1 — Canonical Data Foundation

The canonical dataset is:

`data/canonical/intelligence_data.csv`

The validated data foundation contains:

- 60 canonical measurement records.
- 22 columns.
- 30 distinct incidents.
- 4 machines.
- Synthetic-data flags on all 60 records.
- Canonical data version `1.1.0`.

Manifest, schema, quality, identifier, and version checks passed in the clean-clone validation.

Supporting evidence:
- `final-evidence/03-data-foundation/`
- `docs/PHASE3_CANONICAL_DATA_VALIDATION_REPORT.md`

## 5. Post #2 — Data Readiness

The readiness revalidation confirmed 60 measurement rows representing 30 incidents. All 30 incidents have the required downtime and failure-frequency measurements.

The approved analytical readiness assessment supports Track A. Other analytical tracks remain unsupported or conditional according to the readiness assessment.

Independent reconstruction confirmed:

- Incidents: 30.
- Total downtime: 2,795 minutes.
- Total failure frequency: 65.
- Four machines.
- Category, machine, and shift groupings each cover all 30 incidents exactly once.
- Minimum group-size rule: 3; no published groups fall below the threshold.

Supporting evidence:
- `final-evidence/04-data-readiness/`
- `docs/PHASE3_DATA_READINESS_REVALIDATION_REPORT.md`

## 6. Post #3 — Analytical Track

The approved Track A regeneration path is:

`data-science/scripts/export_intelligence_results.py`

The approved validation script is:

`data-science/scripts/validate_analytical_track.py`

The certification clone was used to regenerate the approved outputs. After excluding the generation timestamp, all 11 result records matched the approved baseline. Summary differences were limited to the generation timestamp. Original approved output hashes were rechecked and remained unchanged.

The contract and independent-baseline validation passed.

The published analytical package contains 11 standardized findings across root-cause category, machine, and shift dimensions. The package includes evidence references, ranks, metrics, version identifiers, quality status, and limitations.

Supporting evidence:
- `final-evidence/05-analytical-validation/`
- `final-evidence/06-intelligence-contract/`
- `docs/PHASE3_ANALYTICAL_REGENERATION_REPORT.md`

## 7. Post #4 — Data Intelligence Page

The Data Intelligence page is implemented separately from the Operational Dashboard.

Validated API endpoints include:

- `GET /api/intelligence/summary`
- `GET /api/intelligence/results`
- `GET /api/intelligence/results/{result_id}`
- `GET /api/intelligence/metadata`
- `GET /api/intelligence/health`

The page presents the approved findings, filters, comparisons, evidence, methodology, limitations, quality status, and freshness information.

The live deployment returned the expected 11 results and matching data and method versions. Machine, category, and shift filters were exercised. The stale-output warning was confirmed to be correct because the approved output generation timestamp is `2026-11-07T09:53:54Z`; the approved package was not regenerated merely to clear the warning.

Supporting evidence:
- `final-evidence/08-data-intelligence/`
- `docs/FINAL_DATA_INTELLIGENCE_VALIDATION.md`

## 8. Post #5 — Assistant or Approved Skip

The Grounded Data Assistant is implemented and validated.

Mode A provides deterministic guided answers. Mode B uses deterministic retrieval and may provide an optional bounded Gemini explanation. The deterministic answer and evidence remain authoritative.

The assistant is restricted to approved Track A package data and bounded query parameters. It does not receive unrestricted access to the canonical CSV, arbitrary SQL, arbitrary code execution, or unrestricted external URLs. It must not invent metrics, rankings, causal explanations, or predictions.

Live Gemini verification confirmed a machine-downtime ranking answer consistent with Track A, with evidence references and synthetic-data limitations retained.

The public deployment uses synthetic demonstration data. Existing incident endpoints and CSV/JSON exports have separately documented public and unpaginated exposure limitations.

Supporting evidence:
- `final-evidence/09-assistant-or-skip/`
- `docs/PHASE3_LIVE_GEMINI_VERIFICATION_REPORT.md`
- `docs/ASSISTANT_ARCHITECTURE.md`
- `docs/ASSISTANT_SAFETY_AND_SCOPE.md`

## 9. Final Architecture

The final architecture document is:

`docs/PHASE3_FINAL_ARCHITECTURE.md`

It contains 18 numbered sections covering the executive overview, architecture principles, system architecture, technology stack, frontend, backend, canonical data, analytical pipeline, intelligence APIs, assistant, findings, security boundaries, deployment, certification verification, limitations, change boundaries, implementation references, and final architecture statement.

The Mermaid system diagram and document structure were reviewed. The document was copied into:

`final-evidence/15-handover/PHASE3_FINAL_ARCHITECTURE.md`

The source and evidence-pack copies were checked using SHA-256 and produced matching hash output.

## 10. Data Version

`1.1.0`

The canonical dataset and approved intelligence outputs use the validated data version.

## 11. Method Version

`1.0.0`

The approved analytical package identifies Track A and method version `1.0.0`.

## 12. Key Validated Findings

The approved synthetic dataset and Track A package report:

| Measure | Validated value |
|---|---:|
| Source incidents | 30 |
| Total downtime | 2,795 minutes |
| Average downtime | 93.1667 minutes |
| Total failure frequency | 65 |
| Average failure frequency | 2.1667 |
| Published intelligence findings | 11 |

Leading group findings:

| Dimension | Leading finding | Observed downtime |
|---|---|---:|
| Root-cause category | Mechanical | 1,265 minutes |
| Machine | MCH-02 | 850 minutes |
| Shift | Morning | 1,060 minutes |

These are descriptive findings from a small synthetic demonstration dataset. They do not establish causality, prediction, or generalizable real-world performance.

## 13. Test Summary

The consolidated Post #6 automated test run collected and passed 64 tests.

| Result | Count |
|---|---:|
| Passed | 64 |
| Failed | 0 |
| Warnings | 1 |

The warning concerns the Starlette test client using `httpx`, which is deprecated in the current test configuration. It was documented rather than changing dependencies during certification.

Frontend lint, TypeScript checking, and production build passed. The clean-clone validation also confirmed frontend route availability and backend health.

Supporting evidence:
- `final-evidence/10-automated-tests/`
- `docs/PHASE3_AUTOMATED_TEST_REPORT.md`

## 14. Regression Summary

The existing Operational Dashboard was checked against the live deployment. Incident totals, downtime metrics, machine ranking, shift heatmap, filters, incident details, and JSON export were checked.

The final Selenium journey verified navigation from the Operational Dashboard to Data Intelligence and back to the Operational Dashboard. Three screenshots were captured.

Supporting evidence:
- `final-evidence/07-operational-regression/`
- `final-evidence/11-selenium/`
- `final-evidence/14-screenshots/`
- `docs/FINAL_OPERATIONAL_REGRESSION_REPORT.md`
- `docs/PHASE3_FINAL_SELENIUM_REPORT.md`

## 15. Deployment Summary

The deployed frontend and backend were checked using their public Render endpoints.

The backend health endpoint, frontend root, and Data Intelligence route returned HTTP 200. Intelligence metadata, results, and summary values were checked for version and metric consistency.

The deployed source commit or Render build identity was not independently verified during these checks.

Supporting evidence:
- `final-evidence/13-deployment/`
- `docs/PHASE3_POST6_DEPLOYMENT_VALIDATION_REPORT.md`

## 16. Evidence Summary

The prescribed 15-folder evidence-pack structure was created.

The evidence inventory contains validation reports, supporting documents, analytical baseline evidence, screenshots, deployment and container logs, and the pre-certification Repomix artifact.

Structural checks confirmed:

- All 15 prescribed folder names are present.
- All evidence folders except the intentionally reserved handover folder contained files before architecture was added.
- Screenshot files were checked for valid PNG structure and non-zero size.
- No zero-byte files were found in the checked inventory.
- Required central reports were present.
- The evidence-pack README was saved and checked.
- The architecture document was copied into the handover folder and its hash matched the source.

The evidence pack is undergoing finalization. The completion report, architecture document, handover guide, and root README update have been prepared. Final evidence reconciliation and review remain in progress. The final Repomix, release identity reconciliation, release tag, GitHub submission, and reviewer signoff remain pending.

## 17. Known Limitations

1. The dataset is synthetic and small; it must not be represented as validated real-world railway operational evidence.
2. Track A is descriptive. The results do not establish causality or predictive capability.
3. The generated intelligence output timestamp is `2026-11-07T09:53:54Z`, so the freshness warning is expected.
4. The automated test run reports one Starlette/httpx deprecation warning.
5. Docker initially encountered transient TLS errors. Subsequent image pull and full Compose build succeeded.
6. Local container validation confirmed backend health and frontend HTTP routes, but did not include a complete local browser interaction journey.
7. A full security scan and production orchestration assessment were not completed as part of the documented validation.
8. Existing public incident endpoints and CSV/JSON exports are unpaginated and have a separately documented exposure risk.
9. Deployed source commit identity was not independently verified.
10. Final reviewer signoff and GitHub certification submission remain pending.

## 18. Unsupported Uses

The application and its current evidence do not support:

- Treating synthetic findings as actual railway incident statistics.
- Generalizing results to other operators, fleets, machines, or time periods.
- Causal claims about why equipment failed.
- Predictive maintenance or failure forecasts.
- Safety-critical or automated maintenance decisions.
- Unapproved analytical tracks or unsupported metrics.
- Treating optional Gemini explanations as independent analytical evidence.
- Using the public demonstration configuration with restricted or real operational data without a separate security and privacy review.

## 19. Future Options

Potential future work, subject to separate approval and real data governance, includes:

- Evaluation using approved, representative operational data.
- A separate security review before introducing restricted data.
- Further accessibility and responsive testing.
- Dependency maintenance to address the documented deprecation and audit warnings.
- Additional analytical tracks only after their readiness requirements and validation contracts are met.

These are future options, not claims of current certification scope.

## 20. Final Result and Current Status

The technical validation activities documented above have produced positive results, including the consolidated automated test run, final Selenium journey, technical UAT, deployment validation, container validation, and architecture review.

However, the full 24-step final certification process is not yet complete. The remaining evidence-pack and handover activities, final Repomix, release identity reconciliation, release tag, GitHub submission, and reviewer signoff must be completed and verified before a final certification result is assigned.

**Current status: IN PROGRESS — NOT YET CERTIFIED.**

**Final certification result: NOT YET ASSIGNED.**

The final result must be selected only after all mandatory steps and reviewer signoff:

- `PHASE 3 COMPLETE — CERTIFIED`
- `PHASE 3 FINAL CHANGES REQUIRED`
- `PHASE 3 CERTIFICATION BLOCKED`

No release tag, GitHub submission, or certification approval is claimed by this draft report.
