# Phase 3 Analytical Regeneration and Validation Report

## 1. Project Details
- Project: POC-21 — Downtime Root Cause Explorer
- Certification Phase: Phase 3 — Post #6
- Validation Date: 2026-11-16
- Validation Environment: Independent clean Git clone
- Branch: main
- Baseline Commit: cab343e58762b5800ed07b12060fc6558e70dd90

## 2. Approved Analytical Configuration
- Analytical Track: TRACK A - COMPARATIVE INTELLIGENCE
- Data Version: 1.1.0
- Method Version: 1.0.0
- Canonical Measurement Rows: 60
- Expected Incidents: 30
- Expected Intelligence Results: 11

## 3. Regeneration Procedure
The approved exporter `data-science/scripts/export_intelligence_results.py` was executed in the independent clean clone.

- Intelligence results export: SUCCESS
- Intelligence summary export: SUCCESS
- Original project outputs: Not modified

The generic `run_analytical_track.py` wrapper was not used for final export because its underlying runner produces an intermediate dictionary structure rather than the approved flat output contract.

## 4. Reproducibility Results
The original and regenerated intelligence results were compared after excluding generated timestamp metadata.

- Original result records: 11
- Regenerated result records: 11
- Analytical record content match: PASS

The summary comparison identified only a generation timestamp difference. All other summary fields matched.

## 5. Independent Analytical Validation
The approved-format output was validated using `data-science/scripts/validate_analytical_track.py` in the clean clone.

- Overall validation: PASS
- Measurement rows: 60 / 60
- Reconstructed incidents: 30 / 30
- Complete incidents: 30 / 30
- Invalid numeric rows: 0
- All source records synthetic: TRUE
- Data version: 1.1.0
- Method version: 1.0.0
- Flat export records: 11 / 11
- Required fields: PASS
- Unique result IDs: PASS
- Version consistency: PASS
- Quality status: PASS
- Ranking validation: PASS
- Independent baseline validation: PASS

## 6. Group Validation
All 30 complete incidents were included exactly once in each comparison dimension.

### Root-Cause Categories
- Electrical: 9 incidents
- Maintenance: 5 incidents
- Mechanical: 10 incidents
- Operational: 6 incidents
- Group validation: PASS

### Machines
- MCH-01: 8 incidents
- MCH-02: 8 incidents
- MCH-03: 7 incidents
- MCH-04: 7 incidents
- Group validation: PASS

### Shifts
- Evening: 10 incidents
- Morning: 11 incidents
- Night: 9 incidents
- Group validation: PASS

All groups met the minimum group-size threshold of 3. Independent baseline checks passed for incident counts, downtime totals, failure-frequency totals, and ranks.

## 7. Original Output Integrity
SHA256 hashes were captured before clean-clone regeneration and compared with the original project files after validation.

| File | Integrity |
|---|---|
| intelligence_results.json | PASS — unchanged |
| intelligence_summary.json | PASS — unchanged |
| validation_metrics.json | PASS — unchanged |
| weak_case_review.json | PASS — unchanged |

All four original files matched their baseline SHA256 hashes.

## 8. Limitations and Interpretation
- All source incidents are synthetic.
- Track A provides descriptive comparative findings only.
- Rankings do not establish causation.
- Results are not predictive evidence.
- Findings must not be generalized as actual industrial performance.

## 9. Conclusion
Analytical regeneration and independent validation passed in the clean clone. The regenerated analytical records matched the original records apart from generation timestamp metadata in the summary. All four approved analytical output files in the original project remained byte-for-byte unchanged.

**Step 6 — Analytical Regeneration: PASS**  
**Step 7 — Intelligence Output Validation: PASS**

## 10. Evidence Locations
- Baseline SHA256 evidence: `docs/evidence/06-analytical-regeneration-baseline.csv`
- Clean-clone validator: `data-science/scripts/validate_analytical_track.py`
- Clean-clone validation output: `data-science/outputs/validation_metrics.json`
- Clean-clone weak-case output: `data-science/outputs/weak_case_review.json`
- Original output integrity: verified against the baseline SHA256 CSV on 2026-11-16.