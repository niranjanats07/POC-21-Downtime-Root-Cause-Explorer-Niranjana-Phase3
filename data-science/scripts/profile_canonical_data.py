
import csv
import json
import math
import statistics
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "data" / "canonical" / "intelligence_data.csv"
OUTPUT_PATH = ROOT / "data-science" / "outputs" / "canonical_profile.json"

FIELD_ROLES = {
    "record_id": "Unique canonical measurement-row identifier",
    "record_type": "Canonical record classification",
    "observed_at": "Observation timestamp",
    "entity_id": "Machine or entity identifier",
    "related_entity_id": "Optional related-entity relationship",
    "entity_name": "Human-readable entity name",
    "category": "Incident root-cause category",
    "subcategory": "Incident root-cause subcategory",
    "status": "Incident status",
    "stage": "Optional incident lifecycle stage",
    "metric_name": "Measurement name",
    "metric_value": "Recorded numeric measurement",
    "metric_unit": "Measurement unit",
    "text_value": "Incident descriptive text",
    "latitude": "Optional geographic latitude",
    "longitude": "Optional geographic longitude",
    "source_name": "Source dataset identifier",
    "source_record_id": "Identifier linking measurements to source incident",
    "is_synthetic": "Synthetic-data provenance indicator",
    "data_version": "Canonical dataset version",
    "shift": "Operational shift classification",
    "severity": "Recorded incident severity"
}


def parse_number(value):
    try:
        number = float(value)
        return number if math.isfinite(number) else None
    except (TypeError, ValueError):
        return None


def parse_timestamp(value):
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        return parsed
    except (ValueError, AttributeError):
        return None


def parse_coordinate(value):
    return parse_number(value)


def profile():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Canonical CSV not found: {CSV_PATH}")

    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        columns = reader.fieldnames or []

    if not rows:
        raise ValueError("Canonical CSV contains no data rows.")

    total = len(rows)
    fields = {}
    whitespace_profile = {}

    for column in columns:
        values = [row.get(column, "") or "" for row in rows]
        non_empty = [value for value in values if value.strip()]
        counts = Counter(non_empty)

        fields[column] = {
            "expected_role": FIELD_ROLES.get(
                column, "Role not explicitly documented"
            ),
            "non_null_count": len(non_empty),
            "null_count": total - len(non_empty),
            "completeness_percent": round(len(non_empty) / total * 100, 2),
            "unique_count": len(counts),
            "top_values": [
                {"value": value, "count": count}
                for value, count in counts.most_common(10)
            ],
            "examples": list(dict.fromkeys(non_empty))[:5],
        }

        whitespace_profile[column] = {
            "leading_or_trailing_whitespace_count": sum(
                1 for value in non_empty if value != value.strip()
            ),
            "empty_string_count": sum(1 for value in values if value == ""),
        }

    # Numeric metric summaries
    metric_summary = {}

    metric_names = sorted({
        row.get("metric_name", "")
        for row in rows
        if row.get("metric_name", "").strip()
    })

    for metric in metric_names:
        selected = [
            parse_number(row.get("metric_value"))
            for row in rows
            if row.get("metric_name") == metric
        ]
        values = [value for value in selected if value is not None]

        metric_summary[metric] = {
            "valid_numeric_count": len(values),
            "invalid_numeric_count": len(selected) - len(values),
            "minimum": min(values) if values else None,
            "maximum": max(values) if values else None,
            "mean": round(statistics.mean(values), 4) if values else None,
            "median": round(statistics.median(values), 4) if values else None,
            "standard_deviation_sample": (
                round(statistics.stdev(values), 4)
                if len(values) > 1 else None
            ),
            "standard_deviation_population": (
                round(statistics.pstdev(values), 4)
                if values else None
            ),
            "units": dict(Counter(
                row.get("metric_unit", "")
                for row in rows
                if row.get("metric_name") == metric
            )),
        }

    # Temporal coverage and timezone consistency
    parsed_dates = []
    invalid_dates = []
    timezone_values = []

    for row in rows:
        value = row.get("observed_at", "")
        parsed = parse_timestamp(value)

        if parsed is None:
            invalid_dates.append(value)
        else:
            parsed_dates.append(parsed)
            timezone_values.append(
                "timezone-aware" if parsed.tzinfo is not None
                else "timezone-naive"
            )

    observation_dates = sorted({
        value.date() for value in parsed_dates
    })

    date_gaps = []
    for previous, current in zip(
        observation_dates, observation_dates[1:]
    ):
        gap_days = (current - previous).days
        if gap_days > 1:
            date_gaps.append({
                "from": previous.isoformat(),
                "to": current.isoformat(),
                "missing_days": gap_days - 1,
            })

    date_counts = Counter(
        value.date().isoformat() for value in parsed_dates
    )

    date_profile = {
        "valid_date_count": len(parsed_dates),
        "invalid_date_count": len(invalid_dates),
        "minimum_observed_at": (
            min(parsed_dates).isoformat() if parsed_dates else None
        ),
        "maximum_observed_at": (
            max(parsed_dates).isoformat() if parsed_dates else None
        ),
        "distinct_observation_dates": len(observation_dates),
        "observation_date_distribution": dict(sorted(date_counts.items())),
        "gaps_between_observation_dates": date_gaps,
        "timezone_type_distribution": dict(Counter(timezone_values)),
        "timezone_consistent": len(set(timezone_values)) <= 1,
    }

    # Record and relationship uniqueness
    record_ids = [
        row.get("record_id", "")
        for row in rows if row.get("record_id", "")
    ]
    source_incident_ids = [
        row.get("source_record_id", "")
        for row in rows if row.get("source_record_id", "")
    ]

    entity_incident_pairs = {
        (
            row.get("entity_id", ""),
            row.get("source_record_id", "")
        )
        for row in rows
        if row.get("entity_id") and row.get("source_record_id")
    }

    record_profile = {
        "unique_record_id_count": len(set(record_ids)),
        "duplicate_record_id_count": len(record_ids) - len(set(record_ids)),
        "distinct_source_incident_count": len(set(source_incident_ids)),
        "record_type_distribution": dict(Counter(
            row.get("record_type", "") for row in rows
        )),
        "repeated_source_incident_measurement_rows": (
            len(source_incident_ids) - len(set(source_incident_ids))
        ),
        "distinct_entity_incident_relationship_count": len(
            entity_incident_pairs
        ),
    }

    # Categorical coverage, rare values and near-constant fields
    categorical_distributions = {}
    categorical_flags = {}

    categorical_columns = [
        "record_type", "entity_id", "category", "subcategory",
        "status", "stage", "shift", "severity", "metric_name",
        "metric_unit"
    ]

    for column in categorical_columns:
        if column not in columns:
            continue

        values = [
            row.get(column, "").strip()
            for row in rows
            if row.get(column, "").strip()
        ]
        counts = Counter(values)

        categorical_distributions[column] = dict(counts)

        rare_values = [
            {"value": value, "count": count}
            for value, count in counts.items()
            if count / total < 0.10
        ]

        dominant_value = counts.most_common(1)[0] if counts else None
        near_constant = bool(
            dominant_value and dominant_value[1] / total >= 0.95
        )

        categorical_flags[column] = {
            "rare_values_below_10_percent": rare_values,
            "near_constant_field_at_95_percent": near_constant,
            "dominant_value": (
                {
                    "value": dominant_value[0],
                    "count": dominant_value[1],
                    "percent_of_all_rows": round(
                        dominant_value[1] / total * 100, 2
                    ),
                }
                if dominant_value else None
            ),
        }

    # Geographic coverage and validity
    latitude_values = [
        parse_coordinate(row.get("latitude"))
        for row in rows
    ]
    longitude_values = [
        parse_coordinate(row.get("longitude"))
        for row in rows
    ]

    valid_coordinate_pairs = [
        (lat, lon)
        for lat, lon in zip(latitude_values, longitude_values)
        if lat is not None and lon is not None
        and -90 <= lat <= 90
        and -180 <= lon <= 180
    ]

    invalid_coordinate_rows = sum(
        1 for lat, lon in zip(latitude_values, longitude_values)
        if (lat is not None or lon is not None)
        and not (
            lat is not None and lon is not None
            and -90 <= lat <= 90
            and -180 <= lon <= 180
        )
    )

    geography_profile = {
        "rows_with_valid_coordinate_pairs": len(valid_coordinate_pairs),
        "rows_without_complete_coordinate_pairs": (
            total - len(valid_coordinate_pairs)
        ),
        "invalid_coordinate_rows": invalid_coordinate_rows,
        "latitude_minimum": (
            min(pair[0] for pair in valid_coordinate_pairs)
            if valid_coordinate_pairs else None
        ),
        "latitude_maximum": (
            max(pair[0] for pair in valid_coordinate_pairs)
            if valid_coordinate_pairs else None
        ),
        "longitude_minimum": (
            min(pair[1] for pair in valid_coordinate_pairs)
            if valid_coordinate_pairs else None
        ),
        "longitude_maximum": (
            max(pair[1] for pair in valid_coordinate_pairs)
            if valid_coordinate_pairs else None
        ),
        "unique_coordinate_pair_count": len(set(valid_coordinate_pairs)),
    }

    # Text length, truncation indicators and whitespace
    text_values = [
        row.get("text_value", "")
        for row in rows
        if row.get("text_value", "").strip()
    ]

    text_lengths = [len(value.strip()) for value in text_values]

    text_profile = {
        "non_null_text_count": len(text_values),
        "average_text_length": (
            round(statistics.mean(text_lengths), 2)
            if text_lengths else 0
        ),
        "maximum_text_length": max(text_lengths) if text_lengths else 0,
        "minimum_text_length": min(text_lengths) if text_lengths else 0,
        "possible_truncation_review_required": any(
            length >= 250 for length in text_lengths
        ),
        "leading_or_trailing_whitespace_count": sum(
            1 for value in text_values if value != value.strip()
        ),
    }

    # Provenance distributions
    provenance_profile = {
        "source_name_distribution": dict(Counter(
            row.get("source_name", "") for row in rows
        )),
        "source_record_id_count": len(set(source_incident_ids)),
        "synthetic_value_distribution": dict(Counter(
            row.get("is_synthetic", "") for row in rows
        )),
        "data_version_distribution": dict(Counter(
            row.get("data_version", "") for row in rows
        )),
    }

    profile_data = {
        "source_file": "data/canonical/intelligence_data.csv",
        "file_size_bytes": CSV_PATH.stat().st_size,
        "row_count": total,
        "column_count": len(columns),
        "columns": columns,
        "field_profiles": fields,
        "whitespace_profile": whitespace_profile,
        "metric_summary": metric_summary,
        "date_profile": date_profile,
        "record_profile": record_profile,
        "categorical_distributions": categorical_distributions,
        "categorical_quality_flags": categorical_flags,
        "geography_profile": geography_profile,
        "text_profile": text_profile,
        "provenance_profile": provenance_profile,
        "limitations": [
            "Profile describes the canonical CSV only.",
            "Canonical rows are not necessarily independent incidents.",
            "Two metric rows may belong to the same source incident.",
            "Observed associations do not establish root-cause causality.",
            "Synthetic data must not be interpreted as real operational evidence.",
            "Missing optional source fields are reported, not fabricated.",
            "Text truncation indicators require source-level confirmation.",
        ],
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(profile_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Profile generated: {OUTPUT_PATH}")
    print(f"Rows: {total}")
    print(f"Columns: {len(columns)}")
    print(f"Distinct source incidents: {len(set(source_incident_ids))}")
    print(f"Metric summaries: {len(metric_summary)}")
    print(f"Valid coordinate pairs: {len(valid_coordinate_pairs)}")
    print(f"Valid timestamps: {len(parsed_dates)}")
    print("Canonical profile generation completed.")


if __name__ == "__main__":
    profile()
