# Sampling Report

The complete source file is retained. It contains 10 records and 11 columns,
so no reduction is required to meet the 10,000-row limit. All 10 records
preserve the observed root-cause, sub-cause, severity, status, shift, machine
and date coverage. The fixed program seed is 42 but is not used because the
sampling decision is full-source retention.

Reproduce with:

```powershell
py scripts/data_pipeline/extract_data.py
py scripts/data_pipeline/sample_data.py
```

Known limitations: the dataset is synthetic, small, has only Closed status,
covers 10 dates, and contains no geographic attributes.
