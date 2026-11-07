# ANALYTICAL METHOD REPORT

## Project Identification

**Project ID:** POC-21  
**PoC Title:** Downtime Root Cause Explorer  
**Analytical Track:** Track A — Comparative Intelligence  
**Method Version:** 1.0.0  
**Canonical Data Version:** 1.1.0  

---

## 1. Purpose

This report documents the analytical method used for the approved Phase 3 analytical track.

The purpose of the method is to generate reproducible comparative intelligence from the approved canonical dataset:

`/data/canonical/intelligence_data.csv`

The method supports structured comparison of observed downtime and failure frequency across:

- Root-cause categories
- Machines
- Shifts

The outputs are descriptive comparative intelligence only. They must not be interpreted as predictive probabilities, causal conclusions, or population-wide industrial performance estimates.

---

## 2. Approved Primary Analytical Question

**Which observed root-cause categories, machines and shifts contribute the greatest total downtime in the approved canonical dataset?**

---

## 3. Decision Supported

The analytical method supports prioritisation of observed groups for further operational review.

The resulting rankings can help identify:

- Higher observed downtime groups
- Lower observed downtime groups
- Relative performance differences
- Groups requiring further investigation

The rankings do not independently establish why a group performs differently.

---

## 4. Approved Analytical Track

**Primary Track:** Track A — Comparative Intelligence

The approved method performs:

- Group totals
- Group comparisons
- Ranking
- Performance prioritisation
- Comparison of downtime contribution
- Comparison of failure-frequency totals

No predictive model, clustering model, anomaly model or simulation model is used.

---

## 5. Canonical Source of Truth

All calculations use only:

`/data/canonical/intelligence_data.csv`

The analytical process does not use:

- Raw API responses
- Manually edited spreadsheets
- Notebook-only datasets
- A second cleaned dataset
- A newly generated dataset
- External datasets

The canonical dataset is the single approved source of truth for the analytical calculations.

---

## 6. Data Version

**Expected Data Version:** `1.1.0`

The validation process confirms that the canonical measurement rows contain the expected data version.

Analytical outputs are produced only when the approved canonical dataset is available and the expected data version is detected.

---

## 7. Analytical Inputs

The following fields are used.

| Canonical Field | Analytical Role |
|---|---|
| `source_record_id` | Incident reconstruction identifier |
| `entity_id` | Machine grouping dimension |
| `category` | Root-cause grouping dimension |
| `shift` | Shift grouping dimension |
| `metric_name` | Measurement identification |
| `metric_value` | Analytical measurement value |
| `data_version` | Version control |
| `is_synthetic` | Data-scope validation |

The required measurement metrics are:

- `downtime_minutes`
- `failure_frequency`

---

## 8. Incident Reconstruction Method

The canonical dataset contains measurement-level rows.

Each incident is reconstructed using `source_record_id`.

A valid complete incident requires:

- One valid `downtime_minutes` measurement
- One valid `failure_frequency` measurement
- A root-cause category
- A machine identifier
- A shift
- A data version

The validator rejects incidents affected by:

- Invalid numeric values
- Duplicate required measurements
- Conflicting metadata
- Missing required comparison fields

This prevents ambiguous or incomplete measurement records from entering comparative calculations.

---

## 9. Missing-Value and Data-Quality Handling

The method applies deterministic validation rules.

Records are excluded from complete-incident calculations when they contain:

- Missing required measurements
- Invalid numeric values
- Duplicate required metrics
- Conflicting metadata
- Missing category values
- Missing machine identifiers
- Missing shift values
- Missing data versions

The validated execution reconstructed 30 complete incidents from 60 canonical measurement rows.

No invalid required numeric measurements were identified in the validated execution.

---

## 10. Leakage Assessment

This analytical track does not train a predictive model.

Therefore, the method does not use future outcome information to predict an earlier target.

The grouping fields are used only for descriptive aggregation:

- Root-cause category
- Machine
- Shift

`source_record_id` is used only to reconstruct measurement rows into incidents.

It is not used as:

- A ranking signal
- A predictive feature
- An analytical performance factor

No identifier is used to artificially influence the analytical ranking.

---

## 11. Baseline Method

The simple baseline independently aggregates the validated complete incidents by each comparison dimension.

For every group, the baseline calculates:

- Incident count
- Total downtime minutes
- Total failure frequency
- Rank by total downtime

The baseline ranking rule is:

1. Descending total downtime
2. Descending incident count
3. Ascending group name

The baseline provides an independent deterministic comparison against the exported analytical results.

---

## 12. Selected Analytical Method

The approved Track A method aggregates complete incidents independently for three grouping dimensions.

### Root-Cause Category

Incidents are grouped using:

`category`

### Machine

Incidents are grouped using:

`entity_id`

### Shift

Incidents are grouped using:

`shift`

For every group, the method calculates:

- Incident count
- Total downtime minutes
- Total failure frequency
- Priority rank based on total downtime

---

## 13. Ranking Method

Groups are ranked using the following deterministic ordering:

1. **Total downtime minutes — descending**
2. **Incident count — descending**
3. **Group name — ascending**

This rule ensures that ties are handled consistently and reproducibly.

Ranks must be sequential:

`1, 2, 3, ..., N`

---

## 14. Minimum Group Size

The configured minimum group size is:

**3 observed incidents**

This threshold is used for small-group sensitivity review.

Groups containing fewer than 3 complete observed incidents are explicitly identified in the weak-case review because rankings based on very small numbers of observations can be more sensitive to individual incidents.

The minimum group-size threshold does not establish:

- Statistical significance
- Population representativeness
- Causal validity
- Long-term ranking stability

For the validated execution, all observed comparison groups met or exceeded the configured minimum group size of 3 incidents.

The smallest observed group sizes were:

- Root-cause category: 5 incidents
- Machine: 7 incidents
- Shift: 9 incidents

Therefore, no observed comparison group was identified as below the configured minimum group-size threshold.

The threshold supports sensitivity review and interpretation. It does not change the deterministic calculation rules used to calculate group totals and rankings.

---

## 15. Why This Method Fits Track A

The approved analytical question requires comparison and prioritisation of observed groups.

Track A is appropriate because the required outputs are:

- Group comparisons
- Aggregate totals
- Rankings
- Relative priority signals

The method does not require:

- Forecasting
- Classification
- Probability estimation
- Causal modelling
- Clustering
- Anomaly detection

A deterministic comparative method therefore provides the required decision support without introducing unnecessary model complexity.

---

## 16. Reproducible Execution Sequence

The analytical process follows this sequence:

1. Load the canonical CSV.
2. Verify the canonical structure and data version.
3. Reconstruct incidents from measurement rows.
4. Validate required measurements.
5. Exclude invalid or incomplete incidents.
6. Build the simple independent baseline.
7. Execute comparative grouping logic.
8. Calculate group totals.
9. Apply deterministic ranking rules.
10. Export intelligence results.
11. Validate calculation accuracy.
12. Compare exported results with the independent baseline.
13. Review weak cases and limitations.
14. Generate structured intelligence outputs.

Core logic is maintained in reusable scripts.

---

## 17. Analytical Outputs

The method produces comparative intelligence for:

- Root-cause categories
- Machines
- Shifts

The structured output includes:

- Group identity
- Incident count
- Total downtime minutes
- Total failure frequency
- Ranking information
- Data version
- Method version
- Validation status
- Limitation information

---

## 18. Unsupported Uses

The analytical outputs must not be used as:

- Predictive forecasts
- Failure probabilities
- Causal conclusions
- Population-wide industrial performance estimates
- Statistical significance evidence
- Guaranteed future rankings
- Evidence that a shift or machine directly causes downtime

The rankings describe the approved observed dataset only.

---

## 19. Known Limitations

The principal limitations are:

- All source incidents are synthetic.
- The dataset represents a limited observation scope.
- Machine coverage is limited.
- The observation period is limited.
- Sampling methodology and population inclusion probabilities are not established.
- Geographic coordinates are unavailable.
- Lifecycle-stage information is unavailable.
- Rankings may change when additional incidents are introduced.
- Comparative results do not establish causal relationships.
- Results are descriptive and not predictive.

Even though all observed groups meet the configured minimum size of 3 incidents, the outputs remain limited to the approved synthetic dataset.

---

## 20. Method Conclusion

The implemented method is a deterministic and reproducible Track A — Comparative Intelligence method.

It uses only the approved canonical dataset, applies explicit data-quality rules, reconstructs complete incidents deterministically, uses an independent simple baseline and produces explainable group rankings.

The method applies a configured minimum group-size threshold of 3 incidents for small-group sensitivity review.

In the validated execution, all observed comparison groups met or exceeded this threshold.

The method is suitable for the approved analytical purpose within the documented limitations.

**Method Version:** 1.0.0  
**Canonical Data Version:** 1.1.0