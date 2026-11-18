# Final Analytical Revalidation Report

## 1. Document Control

- Project: POC-21 — Downtime Root Cause Explorer
- Certification phase: Phase 3 — Post #6
- Validation date: 2026-11-16
- Validation environment: Independent clean Git clone
- Branch: main
- Baseline commit: `cab343e58762b5800ed07b12060fc6558e70dd90`
- Source report: `docs/PHASE3_ANALYTICAL_REGENERATION_REPORT.md`
- Validation status: PASS

## 2. Purpose

This document provides the final certification-facing record of the approved Track A analytical regeneration and independent validation.

The detailed original report is retained unchanged. This document consolidates its results and preserves the recorded evidence, scope and limitations.

## 3. Approved Analytical Configuration

| Item | Validated value |
|---|---|
| Analytical track | TRACK A — COMPARATIVE INTELLIGENCE |
| Data version | 1.1.0 |
| Method version | 1.0.0 |
| Canonical measurement rows | 60 |
| Expected incidents | 30 |
| Expected intelligence results | 11 |

## 4. Regeneration and Reproducibility

The approved exporter was executed in the independent clean clone:

`data-science/scripts/export_intelligence_results.py`

Recorded outcomes:

- Intelligence results export: SUCCESS
- Intelligence summary export: SUCCESS
- Original project outputs modified: NO
- Original result records: 11
- Regenerated result records: 11
- Analytical record content match, excluding generated timestamp metadata: PASS
- Summary comparison: only the generation timestamp differed; all other fields matched.

The generic `run_analytical_track.py` wrapper was not used for final export because its underlying runner produces an intermediate dictionary structure rather than the approved flat output contract.

## 5. Independent Validation Results

The approved-format outputs were validated using:

`data-science/scripts/validate_analytical_track.py`

| Validation item | Result |
|---|---|
| Overall validation | PASS |
| Measurement rows | 60 / 60 |
| Reconstructed incidents | 30 / 30 |
| Complete incidents | 30 / 30 |
| Invalid numeric rows | 0 |
| All source records synthetic | TRUE |
| Data version | 1.1.0 |
| Method version | 1.0.0 |
| Flat export records | 11 / 11 |
| Required fields | PASS |
| Unique result IDs | PASS |
| Version consistency | PASS |
| Quality status | PASS |
| Ranking validation | PASS |
| Independent baseline validation | PASS |

## 6. Group Coverage and Validation

All 30 complete incidents were included exactly once in each comparison dimension.

### Root-cause categories

| Category | Incidents |
|---|---:|
| Electrical | 9 |
| Maintenance | 5 |
| Mechanical | 10 |
| Operational | 6 |
| Total | 30 |

Group validation: PASS.

### Machines

| Machine | Incidents |
|---|---:|
| MCH-01 | 8 |
| MCH-02 | 8 |
| MCH-03 | 7 |
| MCH-04 | 7 |
| Total | 30 |

Group validation: PASS.

### Shifts

| Shift | Incidents |
|---|---:|
| Evening | 10 |
| Morning | 11 |
| Night | 9 |
| Total | 30 |

Group validation: PASS.

All groups met the minimum group-size threshold of 3. Independent baseline checks passed for incident counts, downtime totals, failure-frequency totals and ranks.

## 7. Original Output Integrity

SHA256 hashes were captured before clean-clone regeneration and compared with the original project files after validation.

| Original output | Integrity |
|---|---|
| `intelligence_results.json` | PASS — unchanged |
| `intelligence_summary.json` | PASS — unchanged |
| `validation_metrics.json` | PASS — unchanged |
| `weak_case_review.json` | PASS — unchanged |

All four original files matched their baseline SHA256 hashes.

## 8. Interpretation and Limitations

- All source incidents are synthetic.
- Track A provides descriptive comparative findings only.
- Rankings do not establish causation.
- Results are not predictive evidence.
- Findings must not be generalized as actual industrial performance.

These limitations are part of the approved interpretation boundary and must remain visible in downstream reporting.

## 9. Evidence and Traceability

- Detailed source report: `docs/PHASE3_ANALYTICAL_REGENERATION_REPORT.md`
- Baseline SHA256 evidence: `docs/evidence/06-analytical-regeneration-baseline.csv`
- Approved exporter: `data-science/scripts/export_intelligence_results.py`
- Clean-clone validator: `data-science/scripts/validate_analytical_track.py`
- Clean-clone validation output: `data-science/outputs/validation_metrics.json`
- Clean-clone weak-case output: `data-science/outputs/weak_case_review.json`
- Original output integrity: verified against the baseline SHA256 CSV on 2026-11-16.

## 10. Final Assessment

The approved Track A analytical regeneration and independent validation passed in the clean clone.

The regenerated analytical records matched the original records after excluding generated timestamp metadata. The summary differed only in its generation timestamp. All four original analytical output files remained byte-for-byte unchanged according to the recorded baseline SHA256 comparison.

**Analytical regeneration: PASS.**

**Intelligence output validation: PASS.**

**Final analytical revalidation: PASS.**

This report certifies the recorded analytical checks only. It does not constitute formal Post #6 reviewer certification or release authorization.
