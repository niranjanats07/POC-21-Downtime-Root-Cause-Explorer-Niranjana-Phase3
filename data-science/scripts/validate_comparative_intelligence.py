import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

CSV_PATH = ROOT / "data" / "canonical" / "intelligence_data.csv"

RESULTS_PATH = (
    ROOT / "data-science" / "outputs" / "intelligence_results.json"
)

VALIDATION_PATH = (
    ROOT / "data-science" / "outputs" / "analytical_validation.json"
)


VALIDATION_METHOD_VERSION = "1.0.0"


def to_number(value):
    """Convert a canonical metric value to float."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def independently_build_incidents(rows):
    """
    Independently reconstruct incident-level records from canonical
    measurement rows for validation.

    This implementation intentionally uses a separate calculation path
    from the analytical script.
    """

    incident_data = defaultdict(
        lambda: {
            "downtime_minutes": None,
            "failure_frequency": None,
            "category": "",
            "machine": "",
            "shift": "",
        }
    )

    for row in rows:
        incident_id = row.get(
            "source_record_id",
            ""
        ).strip()

        if not incident_id:
            continue

        incident = incident_data[incident_id]

        incident["category"] = (
            row.get("category", "").strip()
        )

        incident["machine"] = (
            row.get("entity_id", "").strip()
        )

        incident["shift"] = (
            row.get("shift", "").strip()
        )

        metric_name = row.get(
            "metric_name",
            ""
        ).strip()

        numeric_value = to_number(
            row.get("metric_value", "")
        )

        if metric_name == "downtime_minutes":
            incident["downtime_minutes"] = numeric_value

        if metric_name == "failure_frequency":
            incident["failure_frequency"] = numeric_value

    complete_incidents = {
        incident_id: incident
        for incident_id, incident in incident_data.items()
        if incident["downtime_minutes"] is not None
        and incident["failure_frequency"] is not None
    }

    return complete_incidents


def independently_group(
    complete_incidents,
    grouping_key
):
    """
    Independently calculate group metrics using sums and counters.
    """

    totals = {}

    for incident in complete_incidents.values():

        group_name = (
            incident.get(grouping_key, "").strip()
            or "(blank)"
        )

        if group_name not in totals:
            totals[group_name] = {
                "incident_count": 0,
                "total_downtime_minutes": 0.0,
                "total_failure_frequency": 0.0,
            }

        totals[group_name]["incident_count"] += 1

        totals[group_name]["total_downtime_minutes"] += (
            incident["downtime_minutes"]
        )

        totals[group_name]["total_failure_frequency"] += (
            incident["failure_frequency"]
        )

    independent_results = []

    for group_name, values in totals.items():

        count = values["incident_count"]

        independent_results.append({
            "group": group_name,
            "incident_count": count,
            "total_downtime_minutes": (
                values["total_downtime_minutes"]
            ),
            "average_downtime_minutes": (
                values["total_downtime_minutes"] / count
            ),
            "total_failure_frequency": (
                values["total_failure_frequency"]
            ),
            "average_failure_frequency": (
                values["total_failure_frequency"] / count
            ),
        })

    independent_results.sort(
        key=lambda item: (
            -item["total_downtime_minutes"],
            -item["incident_count"],
            item["group"].lower(),
        )
    )

    return independent_results


def compare_group_results(
    generated_groups,
    independently_calculated_groups
):
    """
    Compare generated analytical results against independently
    recalculated values.
    """

    generated_lookup = {
        item["group"]: item
        for item in generated_groups
    }

    independent_lookup = {
        item["group"]: item
        for item in independently_calculated_groups
    }

    all_groups = sorted(
        set(generated_lookup)
        | set(independent_lookup)
    )

    checks = []

    for group_name in all_groups:

        generated = generated_lookup.get(group_name)
        independent = independent_lookup.get(group_name)

        if generated is None or independent is None:
            checks.append({
                "group": group_name,
                "status": "FAIL",
                "reason": (
                    "Group is missing from one calculation."
                ),
            })
            continue

        metric_checks = {}

        for metric in [
            "incident_count",
            "total_downtime_minutes",
            "average_downtime_minutes",
            "total_failure_frequency",
            "average_failure_frequency",
        ]:

            generated_value = generated.get(metric)
            independent_value = independent.get(metric)

            matches = (
                abs(
                    float(generated_value)
                    - float(independent_value)
                )
                < 0.000001
            )

            metric_checks[metric] = {
                "generated": generated_value,
                "independent": independent_value,
                "matches": matches,
            }

        status = (
            "PASS"
            if all(
                check["matches"]
                for check in metric_checks.values()
            )
            else "FAIL"
        )

        checks.append({
            "group": group_name,
            "status": status,
            "metrics": metric_checks,
        })

    return checks


def main():

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Canonical CSV not found: {CSV_PATH}"
        )

    if not RESULTS_PATH.exists():
        raise FileNotFoundError(
            f"Generated intelligence results not found: {RESULTS_PATH}"
        )

    with CSV_PATH.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        rows = list(csv.DictReader(file))

    generated_results = json.loads(
        RESULTS_PATH.read_text(
            encoding="utf-8"
        )
    )

    complete_incidents = independently_build_incidents(rows)

    independent_category = independently_group(
        complete_incidents,
        "category"
    )

    independent_machine = independently_group(
        complete_incidents,
        "machine"
    )

    independent_shift = independently_group(
        complete_incidents,
        "shift"
    )

    generated_comparisons = (
        generated_results.get(
            "comparisons",
            {}
        )
    )

    category_checks = compare_group_results(
        generated_comparisons.get(
            "root_cause_category",
            []
        ),
        independent_category,
    )

    machine_checks = compare_group_results(
        generated_comparisons.get(
            "machine",
            []
        ),
        independent_machine,
    )

    shift_checks = compare_group_results(
        generated_comparisons.get(
            "shift",
            []
        ),
        independent_shift,
    )

    generated_overall = (
        generated_results.get(
            "overall_metrics",
            {}
        )
    )

    independent_total_downtime = sum(
        incident["downtime_minutes"]
        for incident in complete_incidents.values()
    )

    independent_total_frequency = sum(
        incident["failure_frequency"]
        for incident in complete_incidents.values()
    )

    independent_incident_count = len(
        complete_incidents
    )

    independent_average_downtime = (
        independent_total_downtime
        / independent_incident_count
    )

    independent_average_frequency = (
        independent_total_frequency
        / independent_incident_count
    )

    overall_checks = {
        "incident_count": {
            "generated": generated_overall.get(
                "incident_count"
            ),
            "independent": independent_incident_count,
        },
        "total_downtime_minutes": {
            "generated": generated_overall.get(
                "total_downtime_minutes"
            ),
            "independent": independent_total_downtime,
        },
        "average_downtime_minutes": {
            "generated": generated_overall.get(
                "average_downtime_minutes"
            ),
            "independent": independent_average_downtime,
        },
        "total_failure_frequency": {
            "generated": generated_overall.get(
                "total_failure_frequency"
            ),
            "independent": independent_total_frequency,
        },
        "average_failure_frequency": {
            "generated": generated_overall.get(
                "average_failure_frequency"
            ),
            "independent": independent_average_frequency,
        },
    }

    for check in overall_checks.values():

        generated_value = check["generated"]
        independent_value = check["independent"]

        check["matches"] = (
            generated_value is not None
            and abs(
                float(generated_value)
                - float(independent_value)
            )
            < 0.000001
        )

    comparison_checks = (
        category_checks
        + machine_checks
        + shift_checks
    )

    all_group_checks_pass = all(
        check["status"] == "PASS"
        for check in comparison_checks
    )

    all_overall_checks_pass = all(
        check["matches"]
        for check in overall_checks.values()
    )

    validation_status = (
        "PASS"
        if (
            all_group_checks_pass
            and all_overall_checks_pass
        )
        else "FAIL"
    )

    validation_result = {
        "project_id": "POC-21",
        "analytical_track": (
            "TRACK A — COMPARATIVE INTELLIGENCE"
        ),
        "data_version": generated_results.get(
            "data_version"
        ),
        "generated_method_version": generated_results.get(
            "method_version"
        ),
        "validation_method_version": (
            VALIDATION_METHOD_VERSION
        ),
        "source_measurement_rows": len(rows),
        "independently_reconstructed_incidents": (
            independent_incident_count
        ),
        "validation_status": validation_status,
        "overall_metric_checks": overall_checks,
        "group_validation": {
            "root_cause_category": category_checks,
            "machine": machine_checks,
            "shift": shift_checks,
        },
        "validation_conclusion": (
            "Independent deterministic recalculation matched the "
            "generated Track A comparative intelligence outputs."
            if validation_status == "PASS"
            else
            "Independent recalculation found one or more mismatches "
            "with the generated Track A intelligence outputs."
        ),
        "limitations": [
            (
                "Validation confirms calculation consistency, not "
                "real-world representativeness."
            ),
            (
                "The canonical dataset remains entirely synthetic."
            ),
            (
                "Results remain descriptive and do not establish "
                "causality or predictive capability."
            ),
        ],
    }

    VALIDATION_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    VALIDATION_PATH.write_text(
        json.dumps(
            validation_result,
            indent=2,
            ensure_ascii=False
        ) + "\n",
        encoding="utf-8",
    )

    print(
        f"Analytical validation generated: {VALIDATION_PATH}"
    )
    print(
        f"Validation status: {validation_status}"
    )
    print(
        f"Independent incidents: {independent_incident_count}"
    )
    print(
        f"Overall checks passed: {all_overall_checks_pass}"
    )
    print(
        f"Group checks passed: {all_group_checks_pass}"
    )


if __name__ == "__main__":
    main()