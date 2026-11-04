
"""Validate the complete Post #1 canonical data package and write evidence."""
from pathlib import Path
import csv
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
CANONICAL = DATA / "canonical" / "intelligence_data.csv"
SAMPLE = DATA / "source-sample" / "source_sample.csv"
PUBLISHED = DATA / "published" / "intelligence_data.json"
MANIFEST = DATA / "manifest.json"
REPORT = DATA / "quality" / "validation_report.json"

MANDATORY = [
    "record_id", "record_type", "observed_at", "entity_id",
    "related_entity_id", "entity_name", "category", "subcategory",
    "status", "stage", "metric_name", "metric_value", "metric_unit",
    "text_value", "latitude", "longitude", "source_name",
    "source_record_id", "is_synthetic", "data_version",
]
EXPECTED_COLUMNS = MANDATORY + ["shift", "severity"]

MAX_DATA_BYTES = 10 * 1024 * 1024
MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_ROWS = 10_000
MAX_COLS = 50


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def main():
    errors = []
    sample_cols, sample_rows = [], []
    columns, rows = [], []

    required_paths = [
        DATA / "README.md",
        MANIFEST,
        DATA / "schema.json",
        SAMPLE,
        CANONICAL,
        PUBLISHED,
        DATA / "quality" / "data_profile.json",
        DATA / "quality" / "sampling_report.md",
        ROOT / "scripts" / "data_pipeline" / "extract_data.py",
        ROOT / "scripts" / "data_pipeline" / "sample_data.py",
        ROOT / "scripts" / "data_pipeline" / "standardize_data.py",
        ROOT / "scripts" / "data_pipeline" / "validate_data.py",
        ROOT / "scripts" / "data_pipeline" / "publish_data.py",
        ROOT / "docs" / "DATA_SOURCE_INVENTORY.md",
        ROOT / "docs" / "SAMPLING_AND_REDUCTION_REPORT.md",
        ROOT / "docs" / "CANONICAL_DATA_MAPPING.md",
        ROOT / "docs" / "CANONICAL_DATA_PACKAGE_VALIDATION.md",
    ]

    for path in required_paths:
        if not path.is_file():
            errors.append(
                f"Missing required file: {path.relative_to(ROOT)}"
            )

    if not errors:
        sample_cols, sample_rows = read_csv(SAMPLE)
        columns, rows = read_csv(CANONICAL)

        if columns[:len(MANDATORY)] != MANDATORY:
            errors.append(
                "Mandatory canonical columns are missing or out of order."
            )

        if columns != EXPECTED_COLUMNS:
            errors.append(
                "Canonical columns differ from documented 20-field "
                "contract plus shift/severity."
            )

        if len(columns) > MAX_COLS:
            errors.append("Canonical column count exceeds 50.")

        if len(rows) > MAX_ROWS:
            errors.append("Canonical row count exceeds 10,000.")

        ids = [row.get("record_id", "") for row in rows]

        if any(not value for value in ids) or len(ids) != len(set(ids)):
            errors.append("record_id must be non-empty and unique.")

        allowed_types = {
            "entity", "event", "transaction", "measurement",
            "process", "scenario", "node", "edge", "document",
        }

        for index, row in enumerate(rows, start=2):
            if row.get("record_type") not in allowed_types:
                errors.append(
                    f"Invalid record_type at canonical CSV row {index}."
                )

            if not row.get("source_name"):
                errors.append(
                    f"Missing source_name at canonical CSV row {index}."
                )

            if row.get("is_synthetic") not in ("true", "false"):
                errors.append(
                    f"Invalid is_synthetic at canonical CSV row {index}."
                )

            if not row.get("data_version"):
                errors.append(
                    f"Missing data_version at canonical CSV row {index}."
                )

            if row.get("metric_value"):
                try:
                    float(row["metric_value"])
                except ValueError:
                    errors.append(
                        f"Non-numeric metric_value at canonical CSV row {index}."
                    )

            for coord in ("latitude", "longitude"):
                if row.get(coord):
                    try:
                        float(row[coord])
                    except ValueError:
                        errors.append(
                            f"Non-numeric {coord} at canonical CSV row {index}."
                        )

            if row.get("observed_at"):
                try:
                    datetime.strptime(
                        row["observed_at"], "%Y-%m-%dT%H:%M:%SZ"
                    )
                except ValueError:
                    errors.append(
                        f"Invalid ISO UTC observed_at at canonical CSV row {index}."
                    )

            if len(row.get("text_value") or "") > 500:
                errors.append(
                    f"text_value exceeds 500 characters at canonical CSV row {index}."
                )

        schema = json.loads(
            (DATA / "schema.json").read_text(encoding="utf-8")
        )

        if list(schema.keys()) != EXPECTED_COLUMNS:
            errors.append(
                "schema.json field order/content does not match canonical CSV columns."
            )

        manifest = json.loads(
            MANIFEST.read_text(encoding="utf-8")
        )

        if manifest.get("canonical_record_count") != len(rows):
            errors.append(
                "Manifest canonical_record_count does not match canonical CSV."
            )

        if manifest.get("canonical_column_count") != len(columns):
            errors.append(
                "Manifest canonical_column_count does not match canonical CSV."
            )

        if manifest.get("sample_record_count") != len(sample_rows):
            errors.append(
                "Manifest sample_record_count does not match source sample."
            )

        expected_sizes = {
            "source_sample_size_mb": SAMPLE,
            "canonical_file_size_mb": CANONICAL,
            "published_file_size_mb": PUBLISHED,
        }

        for manifest_key, file_path in expected_sizes.items():
            if file_path.exists():
                actual_mb = round(
                    file_path.stat().st_size / (1024 * 1024), 6
                )

                if manifest.get(manifest_key) != actual_mb:
                    errors.append(
                        f"Manifest {manifest_key} does not match "
                        f"{file_path.relative_to(ROOT)}."
                    )

        if manifest.get("canonical_file") != (
            "data/canonical/intelligence_data.csv"
        ):
            errors.append("Manifest canonical_file path is incorrect.")

        if manifest.get("published_file") != (
            "data/published/intelligence_data.json"
        ):
            errors.append("Manifest published_file path is incorrect.")

        if manifest.get("data_version") != "1.0.0":
            errors.append(
                "Manifest data_version must match package version 1.0.0."
            )

        if manifest.get("contains_synthetic_data") is not True:
            errors.append(
                "Manifest must identify synthetic data."
            )

        if manifest.get("contains_personal_data") is not False:
            errors.append(
                "Manifest personal-data declaration must be false "
                "for this reviewed source."
            )

        # Reconstruct JSON values from the canonical CSV and compare.
        published = json.loads(
            PUBLISHED.read_text(encoding="utf-8")
        )

        expected = []

        for row in rows:
            item = {}

            for key, value in row.items():
                if value == "":
                    item[key] = None
                elif key in ("metric_value", "latitude", "longitude"):
                    item[key] = (
                        float(value) if "." in value else int(value)
                    )
                elif key == "is_synthetic":
                    item[key] = value == "true"
                else:
                    item[key] = value

            expected.append(item)

        if published != expected:
            errors.append(
                "Published JSON does not match current canonical CSV."
            )

    file_sizes = {}

    for path in (SAMPLE, CANONICAL, PUBLISHED):
        if path.exists():
            file_sizes[str(path.relative_to(ROOT))] = path.stat().st_size

            if path.stat().st_size > MAX_FILE_BYTES:
                errors.append(
                    f"{path.relative_to(ROOT)} exceeds 5 MB."
                )

    if DATA.exists():
        data_bytes = sum(
            path.stat().st_size
            for path in DATA.rglob("*")
            if path.is_file() and path != REPORT
        )
    else:
        data_bytes = 0

    report = {
        "status": "PASS" if not errors else "FAIL",
        "project_id": "POC-21",
        "data_version": "1.0.0",
        "errors": errors,
        "evidence": {
            "data_directory_size_bytes_including_report": 0,
            "data_directory_size_mb_including_report": 0.0,
            "main_file_sizes_bytes": file_sizes,
            "canonical_row_count": (
                len(rows) if CANONICAL.exists() else None
            ),
            "canonical_column_count": (
                len(columns) if CANONICAL.exists() else None
            ),
            "canonical_columns": (
                columns if CANONICAL.exists() else []
            ),
            "source_sample_row_count": (
                len(sample_rows) if SAMPLE.exists() else None
            ),
            "source_sample_column_count": (
                len(sample_cols) if SAMPLE.exists() else None
            ),
            "synthetic_data": True,
            "personal_data_review": (
                "No personal data observed in supplied synthetic source; "
                "manual reviewer confirmation remains required."
            ),
            "phase2_visualization_changes": (
                "No dashboard/API visualization files intentionally "
                "modified by this package build."
            ),
        },
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)

    # Calculate the report's own size without repeatedly rewriting it.
    for _ in range(20):
        serialized = json.dumps(
            report, indent=2, ensure_ascii=False
        ) + "\n"

        total_bytes = data_bytes + len(serialized.encode("utf-8"))
        total_mb = round(total_bytes / (1024 * 1024), 6)

        evidence = report["evidence"]

        if (
            evidence["data_directory_size_bytes_including_report"]
            == total_bytes
            and evidence["data_directory_size_mb_including_report"]
            == total_mb
        ):
            break

        evidence["data_directory_size_bytes_including_report"] = total_bytes
        evidence["data_directory_size_mb_including_report"] = total_mb

    serialized = json.dumps(
        report, indent=2, ensure_ascii=False
    ) + "\n"

    REPORT.write_text(serialized, encoding="utf-8")

    if errors:
        raise SystemExit(
            "Canonical package validation FAILED:\n- "
            + "\n- ".join(errors)
        )

    print("Canonical package validation PASSED.")


if __name__ == "__main__":
    main()
