
"""Publish JSON and update data profile and manifest from the canonical CSV."""

from pathlib import Path
import csv
import json
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"

SOURCE_SAMPLE = DATA / "source-sample" / "source_sample.csv"
CANONICAL = DATA / "canonical" / "intelligence_data.csv"
PUBLISHED = DATA / "published" / "intelligence_data.json"
MANIFEST = DATA / "manifest.json"
PROFILE = DATA / "quality" / "data_profile.json"

VERSION = "1.0.0"


def mb(path):
    return round(path.stat().st_size / (1024 * 1024), 6) if path.exists() else 0.0


def main():
    if not CANONICAL.is_file():
        raise SystemExit(
            "Canonical CSV missing; run standardize_data.py first."
        )

    if not SOURCE_SAMPLE.is_file():
        raise SystemExit("Source sample CSV is missing.")

    with CANONICAL.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        rows = list(reader)

    records = []

    for row in rows:
        item = {}

        for key, value in row.items():
            if value == "":
                item[key] = None
            elif key in ("metric_value", "latitude", "longitude"):
                item[key] = float(value) if "." in value else int(value)
            elif key == "is_synthetic":
                item[key] = value.casefold() == "true"
            else:
                item[key] = value

        records.append(item)

    PUBLISHED.parent.mkdir(parents=True, exist_ok=True)

    PUBLISHED.write_text(
        json.dumps(records, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    with SOURCE_SAMPLE.open("r", encoding="utf-8-sig", newline="") as f:
        sample_rows = list(csv.DictReader(f))

    original_source = DATA / "synthetic" / "downtime_incidents.csv"

    if original_source.exists():
        with original_source.open("r", encoding="utf-8-sig", newline="") as f:
            original_rows = list(csv.DictReader(f))
    else:
        original_rows = sample_rows

    root_causes = Counter(r["root_cause"] for r in sample_rows)
    severities = Counter(r["severity"] for r in sample_rows)
    shifts = Counter(r["shift"] for r in sample_rows)
    statuses = Counter(r["status"] for r in sample_rows)
    dates = sorted(r["incident_date"] for r in sample_rows)

    profile = {
        "project_id": "POC-21",
        "data_version": VERSION,
        "source_sample": {
            "record_count": len(sample_rows),
            "column_count": len(sample_rows[0]) if sample_rows else 0,
            "date_min": dates[0] if dates else None,
            "date_max": dates[-1] if dates else None,
            "root_cause_counts": dict(sorted(root_causes.items())),
            "severity_counts": dict(sorted(severities.items())),
            "shift_counts": dict(sorted(shifts.items())),
            "status_counts": dict(sorted(statuses.items())),
        },
        "canonical": {
            "record_count": len(rows),
            "column_count": len(columns),
            "metric_name_counts": dict(
                sorted(Counter(r["metric_name"] for r in rows).items())
            ),
            "is_synthetic_values": sorted(
                set(r["is_synthetic"] for r in rows)
            ),
        },
        "limitations": [
            "Synthetic demonstration data only.",
            "Only 10 source incidents are available.",
            "All source incidents have Closed status.",
            "The date range covers 10 consecutive days.",
            "No geographic coordinates or event times are supplied.",
        ],
    }

    PROFILE.parent.mkdir(parents=True, exist_ok=True)

    PROFILE.write_text(
        json.dumps(profile, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    original = DATA / "synthetic" / "downtime_incidents.csv"

    manifest = {
        "project_id": "POC-21",
        "project_title": "Downtime Root Cause Explorer",
        "data_version": VERSION,
        "canonical_file": "data/canonical/intelligence_data.csv",
        "published_file": "data/published/intelligence_data.json",
        "source_type": "synthetic_csv",
        "source_names": ["data/synthetic/downtime_incidents.csv"],
        "is_sampled": len(sample_rows) < len(original_rows),
        "sampling_method": (
            "full_source_retained_no_reduction_required"
            if len(sample_rows) == len(original_rows)
            else "stratified_by_root_cause_severity_status_and_shift_seed_42"
        ),
        "random_seed": 42,
        "original_record_count": len(original_rows),
        "sample_record_count": len(sample_rows),
        "canonical_record_count": len(rows),
        "canonical_column_count": len(columns),
        "source_sample_size_mb": mb(SOURCE_SAMPLE),
        "canonical_file_size_mb": mb(CANONICAL),
        "published_file_size_mb": mb(PUBLISHED),
        "original_source_size_bytes": (
            original.stat().st_size if original.exists() else None
        ),
        "contains_synthetic_data": True,
        "contains_personal_data": False,
        "contains_restricted_data": False,
        "domain_specific_columns": ["shift", "severity"],
    }

    MANIFEST.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(
        f"Published {len(records)} canonical records to "
        f"{PUBLISHED.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
