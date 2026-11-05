# Sampling and Reduction Report

## 1. Source dataset
- Source file: `data/synthetic/downtime_incidents.csv`
- Source type: Synthetic downtime incident dataset
- Original size: 1,212 bytes
- Original record count: 10
- Original column count: 11

## 2. Sampling decision
- Selected method: Full-source retention; no sampling or reduction
- Reason: The complete source contains only 10 records and is within the 10,000-row limit.
- Random seed: 42 (documented but not used)
- Stratification fields: None; stratified sampling was not required.
- Date coverage: All 10 source dates retained.
- Rare-record preservation: All source records retained, including any uncommon category or severity values present in the source.

## 3. Removed fields and records
- Source records removed: None
- Source fields removed during sampling: None
- Reduction decision: No source-level reduction performed.

## 4. Text and sensitive-data handling
- Source sample retains the original source records.
- Canonical text fields are subject to the 500-character package limit.
- No additional text truncation was required during source sampling.
- The supplied dataset is synthetic.
- No personal data was observed in the supplied source; manual reviewer confirmation is still required.

## 5. Final source sample
- Output path: `data/source-sample/source_sample.csv`
- File size: 1,212 bytes
- Record count: 10
- Column count: 11

## 6. Canonical output
- Canonical path: `data/canonical/intelligence_data.csv`
- Canonical record count: 20
- Canonical column count: 22
- Canonical file size: 4,982 bytes
- Published JSON path: `data/published/intelligence_data.json`
- Published JSON record count: 20
- Published JSON file size: 11,520 bytes

The canonical dataset contains two measurement records per source incident. This is a standardization transformation, not additional source sampling.

## 7. Representativeness checks
- All 10 source records were retained.
- All source dates and observed source categories were retained.
- No records were excluded to improve or alter the distribution.
- The dataset is synthetic and small; it should not be treated as representative of all operational downtime.

## 8. Known limitations
- Synthetic dataset with only 10 source incidents.
- All source incidents have Closed status.
- Coverage is limited to 10 dates.
- No geographic attributes are present.
- Manual sensitive-data and source-rights review remains required.

## 9. Analytical Readiness and Interpretation Limits
- The dataset contains only 10 synthetic source incidents. It is suitable for demonstrating data validation, standardization, dashboard functionality, and basic descriptive analysis, but it is not sufficient for strong statistical conclusions.
- Root-cause groups contain very small numbers of incidents. Comparisons between categories should be treated as illustrative observations rather than statistically reliable findings.
- The dataset does not establish a basis for predictive modelling, reliable anomaly detection, or generalizable causal analysis.
- Observed downtime and failure-frequency values describe this synthetic sample only and should not be interpreted as representative operational performance.
- Additional real-world data, broader time coverage, and sufficient observations across categories would be required for stronger analytical conclusions.

## 10. Reproduction commands

Run from the repository root:

```powershell
py scripts/data_pipeline/extract_data.py
py scripts/data_pipeline/sample_data.py
```

The sampling decision is full-source retention. The fixed seed is documented for reproducibility but is not used by this no-reduction workflow.