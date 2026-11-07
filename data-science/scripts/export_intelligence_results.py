"""
POC-21 - Intelligence Results Exporter

Exports Track A Comparative Intelligence results into the standard
Post #3 intelligence_results.json and intelligence_summary.json packages.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ID = "POC-21"
POC_TITLE = "Downtime Root Cause Explorer"
ANALYTICAL_TRACK = "TRACK A - COMPARATIVE INTELLIGENCE"
METHOD_VERSION = "1.0.0"

PRIMARY_ANALYTICAL_QUESTION = (
    "Which observed root-cause categories, machines and shifts contribute "
    "the greatest downtime and failure-frequency burden in the approved "
    "synthetic canonical dataset?"
)

DECISION_TO_BE_SUPPORTED = (
    "Support deterministic review and prioritisation of observed groups "
    "for further investigation based on comparative downtime and "
    "failure-frequency results."
)

LIMITATION = (
    "All source incidents are synthetic. Results are descriptive "
    "demonstration outputs only and must not be generalized as actual "
    "industrial performance, causal evidence or predictive evidence."
)


def ensure_import_path() -> None:
    """Allow imports from scripts/track-specific when run as a script."""

    scripts_dir = Path(__file__).resolve().parent
    track_specific_dir = scripts_dir / "track-specific"

    if str(track_specific_dir) not in sys.path:
        sys.path.insert(0, str(track_specific_dir))


ensure_import_path()

from comparative_intelligence import run_comparative_intelligence  # noqa: E402


def get_project_root() -> Path:
    """Return the repository root."""

    return Path(__file__).resolve().parents[2]


def utc_timestamp() -> str:
    """Return a UTC ISO-8601 generation timestamp."""

    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def build_result_records(
    comparisons: dict[str, list[dict[str, Any]]],
    data_version: str,
    generated_at: str,
    quality_status: str = "validated",
) -> list[dict[str, Any]]:
    """
    Convert comparative group results into the standard intelligence
    result-record contract.
    """

    results: list[dict[str, Any]] = []
    result_number = 1

    comparison_labels = {
        "root_cause_category": "root-cause category",
        "machine": "machine",
        "shift": "shift",
    }

    for comparison_type, groups in comparisons.items():
        label = comparison_labels.get(
            comparison_type,
            comparison_type.replace("_", " "),
        )

        for group in groups:
            result_id = f"RES-{result_number:04d}"

            total_downtime = float(group["total_downtime_minutes"])
            average_downtime = float(group["average_downtime_minutes"])
            total_failure_frequency = float(
                group["total_failure_frequency"]
            )
            average_failure_frequency = float(
                group["average_failure_frequency"]
            )
            incident_count = int(group["incident_count"])
            rank = int(group["rank_by_total_downtime"])

            finding = (
                f"{group['group']} ranks #{rank} among observed "
                f"{label} groups by total downtime, with "
                f"{total_downtime:.1f} downtime minutes across "
                f"{incident_count} complete incidents."
            )

            results.append(
                {
                    "result_id": result_id,
                    "result_type": "comparative_group_ranking",
                    "record_id": None,
                    "entity_id": (
                        group["group"]
                        if comparison_type == "machine"
                        else None
                    ),
                    "group_key": group["group"],
                    "period_start": None,
                    "period_end": None,
                    "metric_name": "total_downtime_minutes",
                    "result_value": total_downtime,
                    "result_unit": "minutes",
                    "result_category": comparison_type,
                    "priority_rank": rank,
                    "finding": finding,
                    "evidence": [
                        {
                            "factor": "grouping_dimension",
                            "value": comparison_type,
                            "contribution": None,
                        },
                        {
                            "factor": "incident_count",
                            "value": incident_count,
                            "contribution": incident_count,
                        },
                        {
                            "factor": "average_downtime_minutes",
                            "value": average_downtime,
                            "contribution": average_downtime,
                        },
                        {
                            "factor": "total_failure_frequency",
                            "value": total_failure_frequency,
                            "contribution": total_failure_frequency,
                        },
                        {
                            "factor": "average_failure_frequency",
                            "value": average_failure_frequency,
                            "contribution": average_failure_frequency,
                        },
                    ],
                    "method_version": METHOD_VERSION,
                    "data_version": data_version,
                    "generated_at": generated_at,
                    "quality_status": quality_status,
                    "limitation": LIMITATION,
                }
            )

            result_number += 1

    return results


def get_top_group(
    comparisons: dict[str, list[dict[str, Any]]],
    comparison_name: str,
) -> dict[str, Any] | None:
    """Return the highest-ranked group for a comparison."""

    groups = comparisons.get(comparison_name, [])

    return groups[0] if groups else None


def build_summary(
    analysis: dict[str, Any],
    result_records: list[dict[str, Any]],
    data_version: str,
    generated_at: str,
    validation_result: str = "PASS",
) -> dict[str, Any]:
    """Build the required intelligence summary."""

    comparisons = analysis["comparisons"]

    top_category = get_top_group(
        comparisons,
        "root_cause_category",
    )

    top_machine = get_top_group(
        comparisons,
        "machine",
    )

    top_shift = get_top_group(
        comparisons,
        "shift",
    )

    key_findings: list[str] = []

    if top_category:
        key_findings.append(
            f"{top_category['group']} is the top observed root-cause "
            f"category by total downtime at "
            f"{top_category['total_downtime_minutes']:.1f} minutes."
        )

    if top_machine:
        key_findings.append(
            f"{top_machine['group']} is the top observed machine by "
            f"total downtime at "
            f"{top_machine['total_downtime_minutes']:.1f} minutes."
        )

    if top_shift:
        key_findings.append(
            f"{top_shift['group']} is the top observed shift by "
            f"total downtime at "
            f"{top_shift['total_downtime_minutes']:.1f} minutes."
        )

    priority_items = [
        {
            "comparison": "root_cause_category",
            "group": top_category["group"] if top_category else None,
            "priority_rank": (
                top_category["rank_by_total_downtime"]
                if top_category
                else None
            ),
        },
        {
            "comparison": "machine",
            "group": top_machine["group"] if top_machine else None,
            "priority_rank": (
                top_machine["rank_by_total_downtime"]
                if top_machine
                else None
            ),
        },
        {
            "comparison": "shift",
            "group": top_shift["group"] if top_shift else None,
            "priority_rank": (
                top_shift["rank_by_total_downtime"]
                if top_shift
                else None
            ),
        },
    ]

    return {
        "project_id": PROJECT_ID,
        "poc_title": POC_TITLE,
        "data_version": data_version,
        "method_version": METHOD_VERSION,
        "approved_track": ANALYTICAL_TRACK,
        "primary_analytical_question": PRIMARY_ANALYTICAL_QUESTION,
        "decision_to_be_supported": DECISION_TO_BE_SUPPORTED,
        "total_result_count": len(result_records),
        "key_findings": key_findings,
        "priority_items": priority_items,
        "validation_result": validation_result,
        "important_limitations": [
            "All source incidents are synthetic.",
            "Results are descriptive demonstration outputs only.",
            "Results must not be generalized as actual industrial performance.",
            "Results do not establish causal relationships.",
            "Results are not predictive evidence.",
            "Small group sizes may affect ranking stability.",
        ],
        "generation_timestamp": generated_at,
        "overall_metrics": analysis["overall_metrics"],
        "top_observed_root_cause_category": top_category,
        "top_observed_machine": top_machine,
        "top_observed_shift": top_shift,
    }


def export_intelligence_results() -> tuple[Path, Path]:
    """
    Execute comparative intelligence and export the standard result package.
    """

    project_root = get_project_root()

    canonical_path = (
        project_root
        / "data"
        / "canonical"
        / "intelligence_data.csv"
    )

    outputs_dir = project_root / "data-science" / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    analysis = run_comparative_intelligence(
        csv_path=canonical_path,
        minimum_group_size=1,
    )

    versions = analysis["data_versions_detected"]

    if len(versions) != 1:
        raise ValueError(
            "Exactly one canonical data version is required for export. "
            f"Detected: {versions}"
        )

    data_version = versions[0]
    generated_at = utc_timestamp()

    result_records = build_result_records(
        comparisons=analysis["comparisons"],
        data_version=data_version,
        generated_at=generated_at,
        quality_status="validated",
    )

    results_path = outputs_dir / "intelligence_results.json"

    with results_path.open("w", encoding="utf-8") as file:
        json.dump(result_records, file, indent=2)

    summary = build_summary(
        analysis=analysis,
        result_records=result_records,
        data_version=data_version,
        generated_at=generated_at,
        validation_result="PASS",
    )

    summary_path = outputs_dir / "intelligence_summary.json"

    with summary_path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    return results_path, summary_path


if __name__ == "__main__":
    results_file, summary_file = export_intelligence_results()

    print("Intelligence results generated:")
    print(results_file)

    print()

    print("Intelligence summary generated:")
    print(summary_file)