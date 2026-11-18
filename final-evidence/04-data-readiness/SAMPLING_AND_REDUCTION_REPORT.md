# Sampling and Reduction Report

## 1. Original Source

| Item | Details |
|---|---|
| Source name | Synthetic Downtime Incident Dataset |
| Source type | Synthetic CSV |
| Source path | `data/synthetic/downtime_incidents.csv` |
| Original record count | 30 |
| Original column count | 11 |
| Original file size | 4,246 bytes |
| Data classification | Synthetic |
| Personal data observed | No personal data observed in the supplied synthetic source |
| Restricted data observed | No restricted data observed in the supplied synthetic source |

Manual reviewer confirmation of data classification remains required.

## 2. Original Size

The original source CSV is 4,246 bytes.

The complete source dataset was small enough to retain without reducing its record count.

## 3. Original Record Count

- Original records: 30
- Records retained: 30
- Records removed: 0

The complete source dataset was retained.

## 4. Original Column Count

The original source contains 11 columns.

The source sample retains all 11 source columns.

## 5. Selected Sampling Method

**Full-source retention (no sampling required).**

The supplied source contains only 30 records. All records were retained to preserve the available operational examples and avoid unnecessary information loss.

No random or stratified record selection was performed.

## 6. Random Seed

- Documented seed: 42
- Seed usage: Not applicable
- Reason: The complete source dataset was retained without random sampling.

## 7. Stratification Fields

No stratified sampling was performed.

The retained source records preserve the categories and examples available in the original synthetic dataset.

## 8. Date-Coverage Method

All source records were retained.

The source contains observations across the dates represented in the original dataset. No date-based filtering or record reduction was applied.

## 9. Rare-Record Preservation

All 30 source records were retained.

This preserves the available examples, including less frequent examples in the supplied source.

No rare-record exclusion was performed.

## 10. Removed Fields

No source columns were removed from `source_sample.csv`.

The canonical standardization process maps source information into the approved canonical fields and documented domain-specific fields.

See `docs/CANONICAL_DATA_MAPPING.md` for the field-level transformations.

## 11. Removed Records

- Records removed during sampling: 0
- Records retained: 30
- Sampling reduction: None

## 12. Text Truncation

The source sample retains the original source records.

Canonical free-text values are subject to the Phase 3 maximum of 500 characters per value.

Any transformation applied during canonical standardization is documented in the canonical mapping.

## 13. Sensitive-Data Removal

No personal or restricted data was observed in the supplied synthetic source dataset.

No separate sensitive-record removal was required based on the initial technical review.

Manual reviewer confirmation remains required before formal approval.

## 14. Final Source Sample

| Item | Result |
|---|---|
| Path | `data/source-sample/source_sample.csv` |
| Size | 4,217 bytes |
| Record count | 30 |
| Column count | 11 |
| Encoding | UTF-8 |
| Sampling | Full-source retention |

## 15. Representativeness Checks

The following checks were performed:

- All 30 original records are retained.
- The source sample preserves all 11 original columns.
- Available source categories are retained.
- The available date coverage is preserved.
- Rare examples present in the original source are retained.
- No records were removed through sampling.

The dataset is synthetic and contains only 30 source incidents. It should not be interpreted as representative of real-world operational activity.

## 16. Canonical Standardization Result

Each source incident produces two canonical measurement records:

1. `downtime_minutes`
2. `failure_frequency`

The resulting canonical dataset contains:

| Item | Result |
|---|---:|
| Canonical records | 60 |
| Canonical columns | 22 |
| Canonical CSV size | 16,182 bytes |
| Published JSON records | 60 |
| Published JSON size | 36,280 bytes |

The first 20 columns follow the mandatory Phase 3 canonical column order.

The additional domain-specific columns are `shift` and `severity`.

The canonical CSV is the source of truth. The published JSON is generated from the canonical CSV.

## 17. Known Sampling Limitations

The following limitations apply:

- The source dataset contains only 30 synthetic incidents.
- The observations cover only the dates represented in the supplied source.
- Geographic coordinates are not available in the source data.
- The dataset does not establish real-world operational representativeness.
- No random sampling was necessary because the complete source was retained.

These limitations must be considered during reviewer assessment.

## 18. Reproduction Command

Run the following commands from the repository root in the documented pipeline order:

```powershell
py scripts/data_pipeline/extract_data.py
py scripts/data_pipeline/sample_data.py
py scripts/data_pipeline/standardize_data.py
py scripts/data_pipeline/validate_data.py
py scripts/data_pipeline/publish_data.py
```

After publishing, validate the package again:

```powershell
py scripts/data_pipeline/validate_data.py
```

## 19. Final Result

The complete supplied synthetic source dataset has been retained and standardized into the canonical data structure.

The canonical CSV contains 60 measurement records and 22 columns.

The published JSON contains 60 records and is generated from the canonical CSV.

Automated canonical package validation has passed.

Manual reviewer confirmation of data classification and formal approval of the Canonical Data Foundation remain outstanding.

