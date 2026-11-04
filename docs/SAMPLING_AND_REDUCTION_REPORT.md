# Sampling and Reduction Report

## 1. Purpose

This report documents the source-data review, sampling decision, reduction approach, and reproducibility of the POC-21 canonical data package.

The objective is to retain a controlled, traceable dataset for the Phase 3 Canonical Data Foundation while preserving the supplied source records.

## 2. Source Dataset

| Item | Result |
|---|---|
| Source file | `data/synthetic/downtime_incidents.csv` |
| Source records | 10 |
| Source columns | 11 |
| Source size | 1,212 bytes |
| Source classification | Synthetic |
| Personal data observed | No personal data observed in the supplied synthetic source |
| Restricted data observed | No restricted data observed in the supplied synthetic source |

Manual reviewer confirmation of the data classification remains required.

## 3. Sampling Decision

The complete source dataset was retained. No source records were removed.

| Item | Result |
|---|---|
| Original source records | 10 |
| Records retained | 10 |
| Records removed | 0 |
| Sampling applied | No |
| Sampling seed | 42 (documented; not used because no sampling was required) |

The source dataset is small enough to retain in full. Retaining all records preserves traceability and avoids losing potentially useful examples.

## 4. Reduction and Standardization

The canonical dataset standardizes the source incidents into measurement records.

Each source incident produces two canonical measurement records:

- `downtime_minutes`
- `failure_frequency`

The resulting canonical dataset contains 20 records and 22 columns.

The first 20 columns follow the required canonical column order. The additional domain-specific columns are `shift` and `severity`.

The canonical CSV remains the source of truth. The published JSON file is generated from the canonical CSV by the pipeline.

## 5. Coverage and Limitations

All 10 supplied source incidents were retained.

The source data provides examples across the categories represented in the supplied dataset. However, the dataset is synthetic and small.

Known limitations:

- The dataset contains only 10 source incidents.
- All supplied incidents have a Closed status.
- The observations cover only the dates present in the synthetic source.
- Geographic coordinates are not available in the source data.
- The dataset does not establish real-world operational coverage or representativeness.

These limitations must be considered during reviewer assessment.

## 6. Data Classification Review

No personal or restricted data was observed in the supplied synthetic source dataset.

This is an initial technical review, not a substitute for formal reviewer confirmation. The reviewer must confirm that the dataset is suitable for the intended project use before subsequent analysis work proceeds.

## 7. Reproduction Commands

Run these commands from the repository root in the documented pipeline order:

```powershell
py scripts/data_pipeline/extract_data.py
py scripts/data_pipeline/sample_data.py
py scripts/data_pipeline/standardize_data.py
py scripts/data_pipeline/validate_data.py
py scripts/data_pipeline/publish_data.py
```

After publishing, run validation again:

```powershell
py scripts/data_pipeline/validate_data.py
```

## 8. Outcome

The complete supplied synthetic source dataset has been retained and standardized into the canonical data structure.

The canonical CSV is the source of truth, and the published JSON is generated from it.

The package has passed the automated validation checks. Manual reviewer confirmation of the data classification and formal approval of the canonical data package are still required.

No Phase 3 Post #2 analysis or Data Intelligence functionality should proceed until the reviewer approves the canonical data foundation.