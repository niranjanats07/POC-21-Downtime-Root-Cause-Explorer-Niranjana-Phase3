import csv
import json
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "data" / "canonical" / "intelligence_data.csv"
OUTPUT_PATH = ROOT / "data-science" / "outputs" / "analytical_readiness.json"


def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Canonical CSV not found: {CSV_PATH}")

    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        raise ValueError("Canonical CSV is empty.")

    incidents = defaultdict(dict)
    incident_metadata = {}

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

        incident_metadata.setdefault(source_id, row)

    incident_count = len(incidents)

    complete_metric_incidents = sum(
        "downtime_minutes" in metrics
        and "failure_frequency" in metrics
        for metrics in incidents.values()
    )

    machine_count = len({
        row.get("entity_id", "").strip()
        for row in incident_metadata.values()
        if row.get("entity_id", "").strip()
    })

    synthetic_count = sum(
        row.get("is_synthetic", "").strip().lower() == "true"
        for row in incident_metadata.values()
    )

    all_closed = all(
        row.get("status", "").strip().lower() == "closed"
        for row in incident_metadata.values()
    )

    category_distribution = dict(Counter(
        row.get("category", "").strip() or "(blank)"
        for row in incident_metadata.values()
    ))

    machine_distribution = dict(Counter(
        row.get("entity_id", "").strip() or "(blank)"
        for row in incident_metadata.values()
    ))

    shift_distribution = dict(Counter(
        row.get("shift", "").strip() or "(blank)"
        for row in incident_metadata.values()
    ))

    severity_distribution = dict(Counter(
        row.get("severity", "").strip() or "(blank)"
        for row in incident_metadata.values()
    ))

    text_count = sum(
        bool(row.get("text_value", "").strip())
        for row in incident_metadata.values()
    )

    data_version_values = sorted({
        row.get("data_version", "").strip()
        for row in rows
        if row.get("data_version", "").strip()
    })

    data_version = (
        data_version_values[0]
        if len(data_version_values) == 1
        else "MULTIPLE_OR_UNSPECIFIED"
    )

    track_a_supported = (
        incident_count >= 20
        and complete_metric_incidents >= 20
        and machine_count >= 2
        and len(category_distribution) >= 2
    )

    tracks = [
        {
            "track": "A",
            "name": "Comparative Intelligence",
            "status": (
                "SUPPORTED"
                if track_a_supported
                else "NOT_SUPPORTED"
            ),
            "supporting_evidence": [
                f"{incident_count} distinct synthetic incidents are available.",
                (
                    f"{complete_metric_incidents} incidents contain both "
                    "downtime_minutes and failure_frequency measurements."
                ),
                (
                    f"{machine_count} machines, "
                    f"{len(category_distribution)} root-cause categories "
                    f"and {len(shift_distribution)} shifts are represented."
                ),
                (
                    "The canonical dataset supports deterministic group totals, "
                    "averages, rankings, percentage contributions and "
                    "performance-gap calculations."
                ),
                (
                    "A simple descriptive baseline can be calculated directly "
                    "from the canonical dataset."
                )
            ],
            "missing_requirements": [
                (
                    f"All {synthetic_count} available incidents are synthetic "
                    "and do not establish real-world operational representativeness."
                ),
                (
                    "The dataset does not establish an independently verified "
                    "real operational population."
                ),
                (
                    "Small groups may produce unstable rankings and must be "
                    "reviewed using minimum group-size and sensitivity checks."
                ),
                (
                    "Results must not be generalized as actual operational "
                    "performance without representative real-world data."
                )
            ],
            "recommendation": (
                "Approve Comparative Intelligence only for a clearly labelled "
                "synthetic-data analytical demonstration. Use deterministic "
                "incident-level aggregation, define minimum group sizes, "
                "validate selected calculations independently, review ranking "
                "stability and document all limitations."
            )
        },
        {
            "track": "B",
            "name": "Trend Intelligence",
            "status": "NOT_SUPPORTED",
            "supporting_evidence": [
                (
                    f"{incident_count} incidents are available, but the "
                    "observation window is limited."
                )
            ],
            "missing_requirements": [
                "A sufficiently long and meaningful longitudinal observation period.",
                "Repeated observations across operational cycles.",
                "A validated time-series baseline.",
                "Evidence supporting trend or seasonality interpretation."
            ],
            "recommendation": (
                "Reject trend and seasonality conclusions for the current "
                "dataset. Do not infer long-term trends from the available "
                "synthetic incident period."
            )
        },
        {
            "track": "C",
            "name": "Risk and Priority Intelligence",
            "status": "CONDITIONAL",
            "supporting_evidence": [
                "Severity, shift, machine and root-cause attributes are available.",
                (
                    "Downtime and failure-frequency measurements could support "
                    "a transparent deterministic demonstration score."
                )
            ],
            "missing_requirements": [
                "Approved business priority rules.",
                "Validated operational thresholds.",
                "Documented stakeholder-approved factor weights.",
                "Evidence that the selected factors represent real urgency."
            ],
            "recommendation": (
                "Do not use Risk and Priority Intelligence as the primary "
                "track unless Post #2 explicitly approves a deterministic "
                "priority method with documented factors, thresholds and "
                "weights."
            )
        },
        {
            "track": "D",
            "name": "Anomaly Intelligence",
            "status": "NOT_SUPPORTED",
            "supporting_evidence": [
                "Numerical downtime and failure-frequency values are available."
            ],
            "missing_requirements": [
                "A representative normal-operation baseline.",
                "Adequate historical observations to characterize variation.",
                "Validated anomaly definitions.",
                "Evidence distinguishing genuine anomalies from sample sparsity."
            ],
            "recommendation": (
                "Reject anomaly detection. The available synthetic sample "
                "does not establish a sufficiently defensible normal baseline."
            )
        },
        {
            "track": "E",
            "name": "Segmentation Intelligence",
            "status": "NOT_SUPPORTED",
            "supporting_evidence": [
                f"{incident_count} incidents and {machine_count} machines are represented.",
                "Descriptive grouping fields are available."
            ],
            "missing_requirements": [
                "Sufficient records for stable and meaningful segments.",
                "Evidence supporting segment stability.",
                "A validated segmentation objective.",
                "Business evidence supporting interpretation of generated groups."
            ],
            "recommendation": (
                "Do not create or claim stable operational segments from the "
                "current synthetic dataset."
            )
        },
        {
            "track": "F",
            "name": "Predictive Intelligence",
            "status": "NOT_SUPPORTED",
            "supporting_evidence": [
                "Numerical measurements are available for each source incident."
            ],
            "missing_requirements": [
                "A genuine prediction target.",
                "Sufficient historical examples.",
                "Decision-time feature availability.",
                "A documented leakage assessment.",
                "A defensible train-validation strategy.",
                "Appropriate performance metrics and error analysis."
            ],
            "recommendation": (
                "Reject predictive modelling. The current dataset is not "
                "approved for predictive intelligence."
            )
        },
        {
            "track": "G",
            "name": "Simulation and Scenario Intelligence",
            "status": "NOT_SUPPORTED",
            "supporting_evidence": [
                "Recorded measurements provide descriptive context only."
            ],
            "missing_requirements": [
                "Validated scenario parameters.",
                "Calibrated operational assumptions.",
                "A defined decision model.",
                "Evidence supporting interpretation of simulated outputs."
            ],
            "recommendation": (
                "Reject operational simulation. Do not invent calibrated "
                "scenario parameters from the synthetic sample."
            )
        },
        {
            "track": "H",
            "name": "Text and Theme Intelligence",
            "status": "CONDITIONAL",
            "supporting_evidence": [
                f"{text_count} incident records contain non-empty descriptions.",
                "Text can be manually reviewed with record-level evidence."
            ],
            "missing_requirements": [
                "A larger and more diverse operational text corpus.",
                "Representative real-world incident language.",
                "A validated taxonomy or theme-classification approach."
            ],
            "recommendation": (
                "Allow only controlled exploratory text review as an optional "
                "supporting activity. Do not claim generalized theme prevalence."
            )
        }
    ]

    primary_question = (
        "Which recorded root-cause categories, machines and shifts have "
        "the highest observed downtime totals and failure-frequency values "
        "within the approved synthetic incident dataset?"
    )

    decision_supported = (
        "Identify the highest-observed groups for closer descriptive review "
        "within the synthetic downtime investigation demonstration."
    )

    supported_tracks = [
        track["track"]
        for track in tracks
        if track["status"] == "SUPPORTED"
    ]

    conditional_tracks = [
        track["track"]
        for track in tracks
        if track["status"] == "CONDITIONAL"
    ]

    rejected_tracks = [
        track["track"]
        for track in tracks
        if track["status"] == "NOT_SUPPORTED"
    ]

    readiness = (
        "DATA READY FOR ANALYTICAL TRACK DEVELOPMENT"
        if "A" in supported_tracks
        else "DATA INSUFFICIENT FOR ANALYTICAL TRACK DEVELOPMENT"
    )

    readiness_explanation = (
        "The approved canonical synthetic dataset supports Track A "
        "(Comparative Intelligence) for a limited, reproducible and "
        "clearly labelled synthetic-data demonstration. The approval does "
        "not establish real-world operational representativeness and does "
        "not support predictive, anomaly, trend, segmentation or simulation "
        "claims."
        if "A" in supported_tracks
        else
        "The canonical dataset does not currently meet the defined evidence "
        "requirements for an approved analytical track."
    )

    result = {
        "source_file": "data/canonical/intelligence_data.csv",
        "data_version": data_version,
        "measurement_rows": len(rows),
        "distinct_incidents": incident_count,
        "incidents_with_both_metrics": complete_metric_incidents,
        "distinct_machines": machine_count,
        "synthetic_incidents": synthetic_count,
        "all_incidents_closed": all_closed,
        "incident_distributions": {
            "machine": machine_distribution,
            "category": category_distribution,
            "shift": shift_distribution,
            "severity": severity_distribution
        },
        "confirmed_data_archetype": (
            "Incident-centric structured event records with repeated metric "
            "measurements per source incident. Suitable for limited "
            "descriptive comparative analysis; not an established "
            "representative time-series or predictive dataset."
        ),
        "tracks": tracks,
        "recommended_primary_track": (
            "A - Comparative Intelligence"
            if "A" in supported_tracks
            else None
        ),
        "optional_supporting_track": (
            "H - Text and Theme Intelligence, limited to controlled "
            "exploratory review."
        ),
        "supported_tracks": supported_tracks,
        "conditionally_supported_tracks": conditional_tracks,
        "rejected_tracks": rejected_tracks,
        "predictive_intelligence_status": "REJECTED",
        "primary_analytical_question": primary_question,
        "decision_supported": decision_supported,
        "scope_boundary": (
            "Track A is approved only for reproducible descriptive comparison "
            "of the approved canonical synthetic dataset. Results must be "
            "labelled synthetic demonstration outputs and must not be "
            "presented as representative of real-world operations."
        ),
        "overall_readiness": readiness,
        "readiness_explanation": readiness_explanation,
        "post_3_approval_gate": (
            "Proceed to Post #3 only if the Post #2 reviewer accepts this "
            "limited Track A scope and approves the readiness evidence."
        )
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )

    print(f"Analytical readiness generated: {OUTPUT_PATH}")
    print(f"Data version: {data_version}")
    print(f"Distinct incidents: {incident_count}")
    print(f"Incidents with both metrics: {complete_metric_incidents}")
    print(f"Supported tracks: {result['supported_tracks']}")
    print(f"Conditional tracks: {result['conditionally_supported_tracks']}")
    print(f"Rejected tracks: {result['rejected_tracks']}")
    print(f"Predictive status: {result['predictive_intelligence_status']}")
    print(f"Overall readiness: {result['overall_readiness']}")


if __name__ == "__main__":
    main()