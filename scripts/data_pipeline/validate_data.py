"""Validate the complete canonical data package."""

from pathlib import Path
import csv
import json
from datetime import datetime


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"

CANONICAL = DATA / "canonical" / "intelligence_data.csv"
PUBLISHED = DATA / "published" / "intelligence_data.json"
MANIFEST = DATA / "manifest.json"

# IMPORTANT:
# Keep this version the same as standardize_data.py and publish_data.py
PACKAGE_VERSION = "1.1.0"


REQUIRED_COLUMNS = [
    "record_id",
    "record_type",
    "observed_at",
    "entity_id",
    "related_entity_id",
    "entity_name",
    "category",
    "subcategory",
    "status",
    "stage",
    "metric_name",
    "metric_value",
    "metric_unit",
    "text_value",
    "latitude",
    "longitude",
    "source_name",
    "source_record_id",
    "is_synthetic",
    "data_version",
    "shift",
    "severity",
]


def load_csv(path):
    """Load CSV and return field names and rows."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        rows = list(reader)

    return fields, rows


def file_size_mb(path):
    """Return file size in MB."""
    if not path.exists():
        return 0.0

    return round(path.stat().st_size / (1024 * 1024), 6)


def validate_canonical_csv(errors):
    """Validate canonical CSV structure and data."""

    if not CANONICAL.exists():
        errors.append(
            "Canonical CSV is missing: data/canonical/intelligence_data.csv"
        )
        return [], []

    fields, rows = load_csv(CANONICAL)

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in fields
    ]

    if missing_columns:
        errors.append(
            "Canonical CSV missing required columns: "
            + ", ".join(missing_columns)
        )

    if not rows:
        errors.append("Canonical CSV contains no data rows.")
        return fields, rows

    record_ids = set()

    for index, row in enumerate(rows, start=2):

        record_id = (row.get("record_id") or "").strip()

        if not record_id:
            errors.append(
                f"Missing record_id at canonical CSV row {index}."
            )
        elif record_id in record_ids:
            errors.append(
                f"Duplicate record_id '{record_id}' at canonical CSV row {index}."
            )
        else:
            record_ids.add(record_id)

        # Validate observed_at
        observed_at = (row.get("observed_at") or "").strip()

        if not observed_at:
            errors.append(
                f"Missing observed_at at canonical CSV row {index}."
            )
        else:
            try:
                datetime.fromisoformat(
                    observed_at.replace("Z", "+00:00")
                )
            except ValueError:
                errors.append(
                    f"Invalid observed_at at canonical CSV row "
                    f"{index}: {observed_at}"
                )

        # Validate metric value
        metric_value = (row.get("metric_value") or "").strip()

        if metric_value == "":
            errors.append(
                f"Missing metric_value at canonical CSV row {index}."
            )
        else:
            try:
                float(metric_value)
            except ValueError:
                errors.append(
                    f"Non-numeric metric_value at canonical CSV row "
                    f"{index}: {metric_value}"
                )

        # Validate synthetic flag
        synthetic = (
            row.get("is_synthetic") or ""
        ).strip().casefold()

        if synthetic not in ("true", "false"):
            errors.append(
                f"Invalid is_synthetic value at canonical CSV row "
                f"{index}: {synthetic}"
            )

        # Validate data version
        data_version = (
            row.get("data_version") or ""
        ).strip()

        if not data_version:
            errors.append(
                f"Missing data_version at canonical CSV row {index}."
            )
        elif data_version != PACKAGE_VERSION:
            errors.append(
                f"Canonical CSV data_version '{data_version}' at row "
                f"{index} does not match package version "
                f"'{PACKAGE_VERSION}'."
            )

    return fields, rows


def validate_manifest(rows, fields, errors):
    """Validate manifest against actual files."""

    if not MANIFEST.exists():
        errors.append("Manifest is missing: data/manifest.json")
        return

    try:
        manifest = json.loads(
            MANIFEST.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        errors.append(f"Manifest is invalid JSON: {exc}")
        return

    source_sample = DATA / "source-sample" / "source_sample.csv"

    if source_sample.exists():
        _, sample_rows = load_csv(source_sample)

        if (
            manifest.get("sample_record_count")
            != len(sample_rows)
        ):
            errors.append(
                "Manifest sample_record_count does not match "
                "source sample."
            )

        actual_sample_size = file_size_mb(source_sample)

        if (
            manifest.get("source_sample_size_mb")
            != actual_sample_size
        ):
            errors.append(
                "Manifest source_sample_size_mb does not match "
                "data/source-sample/source_sample.csv."
            )

    if manifest.get("canonical_record_count") != len(rows):
        errors.append(
            "Manifest canonical_record_count does not match "
            "canonical CSV."
        )

    if manifest.get("canonical_column_count") != len(fields):
        errors.append(
            "Manifest canonical_column_count does not match "
            "canonical CSV."
        )

    actual_canonical_size = file_size_mb(CANONICAL)

    if (
        manifest.get("canonical_file_size_mb")
        != actual_canonical_size
    ):
        errors.append(
            "Manifest canonical_file_size_mb does not match "
            "data/canonical/intelligence_data.csv."
        )

    if manifest.get("data_version") != PACKAGE_VERSION:
        errors.append(
            f"Manifest data_version must match package version "
            f"{PACKAGE_VERSION}."
        )


def validate_published_json(rows, errors):
    """Validate published JSON against canonical CSV."""

    if not PUBLISHED.exists():
        errors.append(
            "Published JSON is missing: "
            "data/published/intelligence_data.json"
        )
        return

    try:
        published_rows = json.loads(
            PUBLISHED.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        errors.append(
            f"Published JSON is invalid: {exc}"
        )
        return

    if not isinstance(published_rows, list):
        errors.append(
            "Published JSON must contain a list of records."
        )
        return

    if len(published_rows) != len(rows):
        errors.append(
            "Published JSON record count does not match "
            "canonical CSV."
        )
        return

    canonical_ids = {
        row.get("record_id")
        for row in rows
    }

    published_ids = {
        row.get("record_id")
        for row in published_rows
        if isinstance(row, dict)
    }

    if canonical_ids != published_ids:
        errors.append(
            "Published JSON does not match current canonical CSV."
        )


def main():
    """Run all package validation checks."""

    errors = []

    fields, rows = validate_canonical_csv(errors)

    if fields or rows:
        validate_manifest(rows, fields, errors)
        validate_published_json(rows, errors)

    if errors:
        print("Canonical package validation FAILED:")

        for error in errors:
            print(f"- {error}")

        raise SystemExit(1)

    print("Canonical package validation PASSED.")
    print(f"Package version: {PACKAGE_VERSION}")
    print(f"Canonical records: {len(rows)}")
    print(f"Canonical columns: {len(fields)}")


if __name__ == "__main__":
    main()