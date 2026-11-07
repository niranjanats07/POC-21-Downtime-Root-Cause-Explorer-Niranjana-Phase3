import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

CSV_PATH = ROOT / "data" / "canonical" / "intelligence_data.csv"

RESULTS_PATH = (
    ROOT / "data-science" / "outputs" / "intelligence_results.json"
)

SUMMARY_PATH = (
    ROOT / "data-science" / "outputs" / "intelligence_summary.json"
)

MINIMUM_GROUP_SIZE = 3


def load_incidents():
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Canonical CSV not found: {CSV_PATH}"
        )

    with CSV_PATH.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        rows = list(csv.DictReader(file))

    if not rows:
        raise ValueError("Canonical CSV is empty.")

    incidents = defaultdict(dict)
    metadata = {}
    data_versions = set()

    for row in rows:
        source_id = row.get("source_record_id", "").strip()

        if not source_id:
            continue

        metric_name = row.get("metric_name", "").strip()
        metric_value = row.get("metric_value", "").strip()

        if metric_name and metric_value:
            try:
                incidents[source_id][metric_name] = float(metric_value)
            except ValueError:
                continue

        metadata.setdefault(source_id, row)

        data_version = row.get("data_version", "").strip()

        if data_version:
            data_versions.add(data_version)

    if len(data_versions) == 1:
        data_version = next(iter(data_versions))
    else:
        data_version = "MULTIPLE_OR_UNSPECIFIED"

    complete_incidents = {}

    for source_id, metrics in incidents.items():
        if (
            "downtime_minutes" in metrics
            and "failure_frequency" in metrics
        ):
            complete_incidents[source_id] = {
                "metadata": metadata[source_id],
                "downtime_minutes": metrics["downtime_minutes"],
                "failure_frequency": metrics["failure_frequency"],
            }

    return rows, complete_incidents, data_version


def build_group_results(complete_incidents, field_name):
    groups = defaultdict(list)

    for incident in complete_incidents.values():
        metadata = incident["metadata"]

        group_name = (
            metadata.get(field_name, "").strip()
            or "(blank)"
        )

        groups[group_name].append(incident)

    results = []

    for group_name, incidents in groups.items():
        incident_count = len(incidents)

        total_downtime = sum(
            incident["downtime_minutes"]
            for incident in incidents
        )

        total_failure_frequency = sum(
            incident["failure_frequency"]
            for incident in incidents
        )

        average_downtime = (
            total_downtime / incident_count
            if incident_count
            else 0
        )

        average_failure_frequency = (
            total_failure_frequency / incident_count
            if incident_count
            else 0
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
                    incident_count >= MINIMUM_GROUP_SIZE
                ),
            }
        )

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


def main():
    rows, complete_incidents, data_version = load_incidents()

    if not complete_incidents:
        raise ValueError(
            "No incidents contain both downtime_minutes "
            "and failure_frequency."
        )

    category_results = build_group_results(
        complete_incidents,
        "category"
    )

    machine_results = build_group_results(
        complete_incidents,
        "entity_id"
    )

    shift_results = build_group_results(
        complete_incidents,
        "shift"
    )

    incident_count = len(complete_incidents)

    total_downtime = sum(
        incident["downtime_minutes"]
        for incident in complete_incidents.values()
    )

    total_failure_frequency = sum(
        incident["failure_frequency"]
        for incident in complete_incidents.values()
    )

    average_downtime = total_downtime / incident_count

    average_failure_frequency = (
        total_failure_frequency / incident_count
    )

    results = {
        "project_id": "POC-21",
        "poc_title": "Downtime Root Cause Explorer",
        "analytical_track": (
            "TRACK A - COMPARATIVE INTELLIGENCE"
        ),
        "data_version": data_version,
        "method_version": "1.0.0",
        "source_file": (
            "data/canonical/intelligence_data.csv"
        ),
        "source_measurement_rows": len(rows),
        "distinct_source_incidents": incident_count,
        "complete_incidents_used_for_comparison": (
            incident_count
        ),
        "minimum_group_size": MINIMUM_GROUP_SIZE,
        "ranking_method": (
            "Descending total downtime, then descending "
            "incident count, then ascending group name for "
            "deterministic tie handling."
        ),
        "calculation_scope": (
            "Descriptive comparison of the approved synthetic "
            "canonical incident dataset only."
        ),
        "synthetic_data_limitation": (
            "All source incidents are synthetic. Results are "
            "descriptive demonstration outputs and must not be "
            "generalized as actual industrial performance or "
            "causal evidence."
        ),
        "overall_metrics": {
            "incident_count": incident_count,
            "total_downtime_minutes": total_downtime,
            "average_downtime_minutes": average_downtime,
            "total_failure_frequency": total_failure_frequency,
            "average_failure_frequency": (
                average_failure_frequency
            ),
        },
        "comparisons": {
            "root_cause_category": category_results,
            "machine": machine_results,
            "shift": shift_results,
        },
    }

    summary = {
        "project_id": "POC-21",
        "analytical_track": (
            "TRACK A - COMPARATIVE INTELLIGENCE"
        ),
        "data_version": data_version,
        "method_version": "1.0.0",
        "overall_result": (
            "Comparative Intelligence completed using "
            "deterministic descriptive calculations on the "
            "approved synthetic canonical dataset."
        ),
        "top_observed_root_cause_category": (
            category_results[0]
        ),
        "top_observed_machine": machine_results[0],
        "top_observed_shift": shift_results[0],
        "limitations": [
            (
                "All records are synthetic and results are not "
                "representative of real-world industrial operations."
            ),
            (
                "The analysis is descriptive and does not establish "
                "causality."
            ),
            (
                "The dataset contains only the approved observation "
                "period and represented machines."
            ),
            (
                "Small group sizes may affect ranking stability and "
                "must be interpreted with caution."
            ),
        ],
    }

    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    RESULTS_PATH.write_text(
        json.dumps(
            results,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    SUMMARY_PATH.write_text(
        json.dumps(
            summary,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        f"Comparative intelligence generated: {RESULTS_PATH}"
    )

    print(
        f"Intelligence summary generated: {SUMMARY_PATH}"
    )

    print(f"Data version: {data_version}")
    print(f"Measurement rows: {len(rows)}")
    print(
        f"Distinct incidents: {incident_count}"
    )
    print(
        f"Complete incidents analysed: {incident_count}"
    )
    print(
        f"Total downtime: {total_downtime}"
    )
    print(
        f"Total failure frequency: "
        f"{total_failure_frequency}"
    )
    print(
        "Top category by total downtime: "
        f"{category_results[0]['group']}"
    )
    print(
        "Top machine by total downtime: "
        f"{machine_results[0]['group']}"
    )
    print(
        "Top shift by total downtime: "
        f"{shift_results[0]['group']}"
    )


if __name__ == "__main__":
    main()
