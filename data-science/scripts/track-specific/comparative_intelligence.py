"""
POC-21 - Track A Comparative Intelligence

Reusable deterministic comparative aggregation logic for the approved
canonical synthetic downtime investigation dataset.

This module:
- Loads the approved canonical CSV
- Reconstructs source incidents using source_record_id
- Pairs downtime_minutes and failure_frequency measurements
- Groups complete incidents by category, machine and shift
- Calculates deterministic comparative metrics
- Applies deterministic ranking
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from typing import Any


PROJECT_ID = "POC-21"
METHOD_VERSION = "1.0.0"
APPROVED_DATA_VERSION = "1.1.0"

REQUIRED_METRICS = {
    "downtime_minutes",
    "failure_frequency",
}

GROUPING_DIMENSIONS = {
    "root_cause_category": "category",
    "machine": "entity_id",
    "shift": "shift",
}


def load_canonical_records(csv_path: str | Path) -> list[dict[str, str]]:
    """
    Load records from the approved canonical CSV.
    """

    path = Path(csv_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Approved canonical dataset was not found: {path}"
        )

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        records = list(reader)

    if not records:
        raise ValueError("The approved canonical dataset is empty.")

    return records


def validate_required_fields(records: list[dict[str, str]]) -> None:
    """
    Verify that the required analytical fields are available.
    """

    if not records:
        raise ValueError("No canonical records are available for validation.")

    required_fields = {
        "source_record_id",
        "category",
        "entity_id",
        "shift",
        "metric_name",
        "metric_value",
        "data_version",
        "is_synthetic",
    }

    available_fields = set(records[0].keys())
    missing_fields = required_fields - available_fields

    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise ValueError(
            f"Canonical dataset is missing required analytical fields: {missing}"
        )


def reconstruct_incidents(
    records: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """
    Reconstruct incident-level records from repeated metric measurements.

    A complete incident requires:
    - downtime_minutes
    - failure_frequency
    """

    incidents: dict[str, dict[str, Any]] = {}

    for row in records:
        source_record_id = (row.get("source_record_id") or "").strip()

        if not source_record_id:
            continue

        if source_record_id not in incidents:
            incidents[source_record_id] = {
                "source_record_id": source_record_id,
                "category": row.get("category") or "",
                "entity_id": row.get("entity_id") or "",
                "shift": row.get("shift") or "",
                "data_version": row.get("data_version") or "",
                "is_synthetic": row.get("is_synthetic") or "",
                "metrics": {},
            }

        metric_name = (row.get("metric_name") or "").strip()
        metric_value = row.get("metric_value")

        if metric_name not in REQUIRED_METRICS:
            continue

        try:
            numeric_value = float(metric_value)
        except (TypeError, ValueError):
            continue

        incidents[source_record_id]["metrics"][metric_name] = numeric_value

    complete_incidents: list[dict[str, Any]] = []

    for incident in incidents.values():
        metrics = incident["metrics"]

        if not REQUIRED_METRICS.issubset(metrics.keys()):
            continue

        complete_incidents.append(
            {
                "source_record_id": incident["source_record_id"],
                "category": incident["category"],
                "entity_id": incident["entity_id"],
                "shift": incident["shift"],
                "data_version": incident["data_version"],
                "is_synthetic": incident["is_synthetic"],
                "downtime_minutes": metrics["downtime_minutes"],
                "failure_frequency": metrics["failure_frequency"],
            }
        )

    return complete_incidents


def normalise_group_name(value: Any) -> str:
    """
    Convert blank grouping values into a deterministic reviewable label.
    """

    if value is None:
        return "(blank)"

    value = str(value).strip()

    return value if value else "(blank)"


def calculate_group_comparison(
    incidents: list[dict[str, Any]],
    grouping_field: str,
    minimum_group_size: int = 3,
) -> list[dict[str, Any]]:
    """
    Calculate deterministic comparative metrics for one grouping dimension.
    """

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for incident in incidents:
        group_name = normalise_group_name(incident.get(grouping_field))
        grouped[group_name].append(incident)

    results: list[dict[str, Any]] = []

    for group_name, group_incidents in grouped.items():
        incident_count = len(group_incidents)

        total_downtime = sum(
            float(item["downtime_minutes"])
            for item in group_incidents
        )

        total_failure_frequency = sum(
            float(item["failure_frequency"])
            for item in group_incidents
        )

        average_downtime = (
            total_downtime / incident_count
            if incident_count
            else 0.0
        )

        average_failure_frequency = (
            total_failure_frequency / incident_count
            if incident_count
            else 0.0
        )

        results.append(
            {
                "group": group_name,
                "incident_count": incident_count,
                "downtime_measurement_count": incident_count,
                "failure_frequency_measurement_count": incident_count,
                "total_downtime_minutes": total_downtime,
                "average_downtime_minutes": average_downtime,
                "total_failure_frequency": total_failure_frequency,
                "average_failure_frequency": average_failure_frequency,
                "meets_minimum_group_size": (
                    incident_count >= minimum_group_size
                ),
            }
        )

    # Deterministic ranking:
    # 1. Descending total downtime
    # 2. Descending incident count
    # 3. Ascending group name
    results.sort(
        key=lambda item: (
            -item["total_downtime_minutes"],
            -item["incident_count"],
            item["group"],
        )
    )

    for rank, result in enumerate(results, start=1):
        result["rank_by_total_downtime"] = rank

    return results


def calculate_comparisons(
    incidents: list[dict[str, Any]],
    minimum_group_size: int = 3,
) -> dict[str, list[dict[str, Any]]]:
    """
    Calculate comparative intelligence across all approved grouping dimensions.
    """

    comparisons: dict[str, list[dict[str, Any]]] = {}

    for comparison_name, grouping_field in GROUPING_DIMENSIONS.items():
        comparisons[comparison_name] = calculate_group_comparison(
            incidents=incidents,
            grouping_field=grouping_field,
            minimum_group_size=minimum_group_size,
        )

    return comparisons


def calculate_overall_metrics(
    incidents: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Calculate overall descriptive metrics for complete incidents.
    """

    incident_count = len(incidents)

    total_downtime = sum(
        float(item["downtime_minutes"])
        for item in incidents
    )

    total_failure_frequency = sum(
        float(item["failure_frequency"])
        for item in incidents
    )

    return {
        "incident_count": incident_count,
        "total_downtime_minutes": total_downtime,
        "average_downtime_minutes": (
            total_downtime / incident_count
            if incident_count
            else 0.0
        ),
        "total_failure_frequency": total_failure_frequency,
        "average_failure_frequency": (
            total_failure_frequency / incident_count
            if incident_count
            else 0.0
        ),
    }


def get_data_versions(records: list[dict[str, str]]) -> list[str]:
    """
    Return deterministic sorted data versions detected in canonical records.
    """

    versions = {
        (row.get("data_version") or "").strip()
        for row in records
        if (row.get("data_version") or "").strip()
    }

    return sorted(versions)


def all_records_synthetic(records: list[dict[str, str]]) -> bool:
    """
    Check whether all canonical records are explicitly marked synthetic.
    """

    if not records:
        return False

    true_values = {
        "true",
        "1",
        "yes",
        "y",
    }

    return all(
        str(row.get("is_synthetic") or "").strip().lower()
        in true_values
        for row in records
    )


def run_comparative_intelligence(
    csv_path: str | Path,
    minimum_group_size: int = 3,
) -> dict[str, Any]:
    """
    Execute the reusable Track A comparative intelligence workflow.

    Returns all reconstructed incidents, comparisons and summary metadata
    required by runner, validation and export scripts.
    """

    records = load_canonical_records(csv_path)

    validate_required_fields(records)

    incidents = reconstruct_incidents(records)

    if not incidents:
        raise ValueError(
            "No complete incidents containing both required metrics "
            "could be reconstructed."
        )

    comparisons = calculate_comparisons(
        incidents=incidents,
        minimum_group_size=minimum_group_size,
    )

    return {
        "project_id": PROJECT_ID,
        "method_version": METHOD_VERSION,
        "source_measurement_rows": len(records),
        "distinct_source_incidents": len(
            {
                (row.get("source_record_id") or "").strip()
                for row in records
                if (row.get("source_record_id") or "").strip()
            }
        ),
        "complete_incidents": len(incidents),
        "data_versions_detected": get_data_versions(records),
        "all_records_synthetic": all_records_synthetic(records),
        "minimum_group_size": minimum_group_size,
        "overall_metrics": calculate_overall_metrics(incidents),
        "comparisons": comparisons,
        "incidents": incidents,
    }
