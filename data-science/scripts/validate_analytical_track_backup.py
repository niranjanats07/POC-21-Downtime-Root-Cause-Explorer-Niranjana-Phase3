from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ID = "POC-21"

ANALYTICAL_TRACK = "TRACK A - COMPARATIVE INTELLIGENCE"

METHOD_VERSION = "1.0.0"

EXPECTED_DATA_VERSION = "1.1.0"

EXPECTED_MEASUREMENT_ROWS = 60

EXPECTED_INCIDENTS = 30

MINIMUM_GROUP_SIZE = 3


# ============================================================
# PROJECT PATHS
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = SCRIPT_DIR.parent.parent

SOURCE_FILE = (
    PROJECT_ROOT
    / "data"
    / "canonical"
    / "intelligence_data.csv"
)

RESULTS_FILE = (
    PROJECT_ROOT
    / "data-science"
    / "outputs"
    / "intelligence_results.json"
)

VALIDATION_OUTPUT = (
    PROJECT_ROOT
    / "data-science"
    / "outputs"
    / "validation_metrics.json"
)

WEAK_CASE_OUTPUT = (
    PROJECT_ROOT
    / "data-science"
    / "outputs"
    / "weak_case_review.json"
)


# ============================================================
# FILE LOADING FUNCTIONS
# ============================================================

def load_csv_rows(file_path: Path) -> list[dict[str, str]]:
    """Load CSV records as dictionaries."""

    with file_path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        return list(csv.DictReader(file))


def load_json(file_path: Path):
    """Load a JSON file."""

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


# ============================================================
# VALUE NORMALISATION
# ============================================================

def is_true(value) -> bool:
    """Return True when a value represents boolean true."""

    return str(value).strip().lower() in {
        "true",
        "1",
        "yes",
        "y",
    }


def parse_numeric(value):
    """Convert a value to a finite float."""

    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return None

    if not math.isfinite(numeric_value):
        return None

    return numeric_value


# ============================================================
# INCIDENT RECONSTRUCTION
# ============================================================

def reconstruct_incidents(rows):

    incidents = {}

    required_metrics = {
        "downtime_minutes",
        "failure_frequency",
    }

    for row in rows:

        incident_id = str(
            row.get("source_record_id", "")
        ).strip()

        if not incident_id:
            continue

        if incident_id not in incidents:

            incidents[incident_id] = {
                "incident_id": incident_id,
                "entity_id": str(
                    row.get("entity_id", "")
                ).strip(),
                "category": str(
                    row.get("category", "")
                ).strip(),
                "shift": str(
                    row.get("shift", "")
                ).strip(),
                "data_version": str(
                    row.get("data_version", "")
                ).strip(),
                "is_synthetic": is_true(
                    row.get("is_synthetic")
                ),
                "downtime_minutes": None,
                "failure_frequency": None,
                "invalid_numeric": False,
                "duplicate_required_metric": False,
                "metadata_conflict": False,
                "metric_counts": defaultdict(int),
            }

        incident = incidents[incident_id]

        metadata_fields = (
            "entity_id",
            "category",
            "shift",
            "data_version",
        )

        for field_name in metadata_fields:

            row_value = str(
                row.get(field_name, "")
            ).strip()

            incident_value = str(
                incident.get(field_name, "")
            ).strip()

            if (
                incident_value
                and row_value
                and incident_value != row_value
            ):
                incident["metadata_conflict"] = True

        row_is_synthetic = is_true(
            row.get("is_synthetic")
        )

        if incident["is_synthetic"] != row_is_synthetic:
            incident["metadata_conflict"] = True

        metric_name = str(
            row.get("metric_name", "")
        ).strip()

        if metric_name not in required_metrics:
            continue

        incident["metric_counts"][metric_name] += 1

        if incident["metric_counts"][metric_name] > 1:
            incident[
                "duplicate_required_metric"
            ] = True

        numeric_value = parse_numeric(
            row.get("metric_value")
        )

        if numeric_value is None:
            incident["invalid_numeric"] = True
            continue

        incident[metric_name] = numeric_value

    for incident in incidents.values():
        incident["metric_counts"] = dict(
            incident["metric_counts"]
        )

    return incidents


# ============================================================
# COMPLETE INCIDENT VALIDATION
# ============================================================

def get_complete_incidents(incidents):

    complete_incidents = []

    for incident in incidents.values():

        if incident["invalid_numeric"]:
            continue

        if incident["duplicate_required_metric"]:
            continue

        if incident["metadata_conflict"]:
            continue

        if incident["downtime_minutes"] is None:
            continue

        if incident["failure_frequency"] is None:
            continue

        if not incident["category"]:
            continue

        if not incident["entity_id"]:
            continue

        if not incident["shift"]:
            continue

        if not incident["data_version"]:
            continue

        complete_incidents.append(incident)

    return complete_incidents


# ============================================================
# GROUP COVERAGE
# ============================================================

def build_group_coverage(
    complete_incidents,
    field_name,
):

    group_sizes = defaultdict(int)

    for incident in complete_incidents:

        group_value = str(
            incident.get(field_name, "")
        ).strip()

        if group_value:
            group_sizes[group_value] += 1

    total_assignments = sum(
        group_sizes.values()
    )

    complete_incident_count = len(
        complete_incidents
    )

    return {
        "group_count": len(group_sizes),
        "total_incident_assignments": total_assignments,
        "complete_incident_count": complete_incident_count,
        "all_incidents_included_once": (
            total_assignments
            == complete_incident_count
        ),
        "group_sizes": dict(
            sorted(group_sizes.items())
        ),
    }


# ============================================================
# SIMPLE BASELINE
# ============================================================

def build_simple_baseline(
    complete_incidents,
    field_name,
):

    group_totals = defaultdict(
        lambda: {
            "incident_count": 0,
            "total_downtime_minutes": 0.0,
            "total_failure_frequency": 0.0,
        }
    )

    for incident in complete_incidents:

        group_name = str(
            incident.get(field_name, "")
        ).strip()

        if not group_name:
            continue

        group_totals[group_name][
            "incident_count"
        ] += 1

        group_totals[group_name][
            "total_downtime_minutes"
        ] += incident["downtime_minutes"]

        group_totals[group_name][
            "total_failure_frequency"
        ] += incident["failure_frequency"]

    baseline_results = []

    for group_name, values in group_totals.items():

        baseline_results.append(
            {
                "group": group_name,
                "incident_count":
                    values["incident_count"],
                "total_downtime_minutes":
                    values["total_downtime_minutes"],
                "total_failure_frequency":
                    values["total_failure_frequency"],
            }
        )

    baseline_results.sort(
        key=lambda item: (
            -item["total_downtime_minutes"],
            -item["incident_count"],
            item["group"],
        )
    )

    for rank, result in enumerate(
        baseline_results,
        start=1,
    ):
        result[
            "rank_by_total_downtime"
        ] = rank

    return baseline_results


# ============================================================
# EXTRACT VALUES FROM ACTUAL EXPORTED JSON FORMAT
# ============================================================

def get_evidence_value(
    result,
    factor_name,
    default=None,
):
    """
    Extract a value from the exported evidence array.
    """

    evidence = result.get("evidence", [])

    if not isinstance(evidence, list):
        return default

    for item in evidence:

        if not isinstance(item, dict):
            continue

        if item.get("factor") == factor_name:
            return item.get("value", default)

    return default


# ============================================================
# NORMALISE EXPORTED RESULTS
# ============================================================

def normalize_exported_result(result):
    """
    Convert the actual intelligence_results.json structure into
    the common structure used by validation.

    Actual exported fields:
    - group_key
    - priority_rank
    - result_value
    - evidence[]
    """

    if not isinstance(result, dict):
        raise TypeError(
            "Exported result must be a dictionary"
        )

    group_name = str(
        result.get("group_key", "")
    ).strip()

    priority_rank = int(
        result.get("priority_rank")
    )

    total_downtime = float(
        result.get("result_value")
    )

    incident_count = int(
        get_evidence_value(
            result,
            "incident_count",
            0,
        )
    )

    total_failure_frequency = float(
        get_evidence_value(
            result,
            "total_failure_frequency",
            0,
        )
    )

    if not group_name:
        raise ValueError("Missing group_key")

    if priority_rank < 1:
        raise ValueError("Invalid priority rank")

    if incident_count < 1:
        raise ValueError("Invalid incident count")

    if total_downtime < 0:
        raise ValueError("Invalid downtime")

    if total_failure_frequency < 0:
        raise ValueError("Invalid failure frequency")

    if not math.isfinite(total_downtime):
        raise ValueError("Non-finite downtime")

    if not math.isfinite(
        total_failure_frequency
    ):
        raise ValueError(
            "Non-finite failure frequency"
        )

    return {
        "group": group_name,
        "incident_count": incident_count,
        "total_downtime_minutes": total_downtime,
        "total_failure_frequency":
            total_failure_frequency,
        "rank_by_total_downtime":
            priority_rank,
    }


# ============================================================
# SPLIT EXPORTED RESULTS BY CATEGORY
# ============================================================

def split_results_by_category(results):

    comparison_results = {
        "root_cause_category": [],
        "machine": [],
        "shift": [],
    }

    if not isinstance(results, list):
        return comparison_results

    for result in results:

        if not isinstance(result, dict):
            continue

        if (
            result.get("result_type")
            != "comparative_group_ranking"
        ):
            continue

        category = str(
            result.get(
                "result_category",
                "",
            )
        ).strip()

        if category in comparison_results:
            comparison_results[category].append(
                result
            )

    return comparison_results


# ============================================================
# BASELINE COMPARISON
# ============================================================

def compare_baseline_to_results(
    baseline_results,
    exported_results,
):

    base_response = {
        "baseline_group_count": len(baseline_results),
        "exported_group_count": (
            len(exported_results)
            if isinstance(exported_results, list)
            else 0
        ),
        "groups_match": False,
        "incident_counts_match": False,
        "downtime_totals_match": False,
        "failure_frequency_totals_match": False,
        "ranks_match": False,
        "duplicate_exported_groups": False,
        "passed": False,
    }

    if (
        not isinstance(exported_results, list)
        or not exported_results
    ):
        return base_response

    try:

        baseline_by_group = {
            item["group"]: item
            for item in baseline_results
        }

        exported_by_group = {}

        for raw_result in exported_results:

            item = normalize_exported_result(
                raw_result
            )

            group_name = item["group"]

            if group_name in exported_by_group:

                base_response[
                    "duplicate_exported_groups"
                ] = True

                return base_response

            exported_by_group[group_name] = item

        groups_match = (
            set(baseline_by_group.keys())
            == set(exported_by_group.keys())
        )

        incident_counts_match = (
            groups_match
            and all(
                baseline_by_group[group][
                    "incident_count"
                ]
                == exported_by_group[group][
                    "incident_count"
                ]
                for group in baseline_by_group
            )
        )

        downtime_totals_match = (
            groups_match
            and all(
                math.isclose(
                    baseline_by_group[group][
                        "total_downtime_minutes"
                    ],
                    exported_by_group[group][
                        "total_downtime_minutes"
                    ],
                    rel_tol=0.0,
                    abs_tol=1e-9,
                )
                for group in baseline_by_group
            )
        )

        failure_frequency_totals_match = (
            groups_match
            and all(
                math.isclose(
                    baseline_by_group[group][
                        "total_failure_frequency"
                    ],
                    exported_by_group[group][
                        "total_failure_frequency"
                    ],
                    rel_tol=0.0,
                    abs_tol=1e-9,
                )
                for group in baseline_by_group
            )
        )

        ranks_match = (
            groups_match
            and all(
                baseline_by_group[group][
                    "rank_by_total_downtime"
                ]
                == exported_by_group[group][
                    "rank_by_total_downtime"
                ]
                for group in baseline_by_group
            )
        )

        passed = (
            groups_match
            and incident_counts_match
            and downtime_totals_match
            and failure_frequency_totals_match
            and ranks_match
        )

        return {
            "baseline_group_count":
                len(baseline_results),

            "exported_group_count":
                len(exported_results),

            "groups_match":
                groups_match,

            "incident_counts_match":
                incident_counts_match,

            "downtime_totals_match":
                downtime_totals_match,

            "failure_frequency_totals_match":
                failure_frequency_totals_match,

            "ranks_match":
                ranks_match,

            "duplicate_exported_groups":
                False,

            "passed":
                passed,
        }

    except (
        TypeError,
        ValueError,
        KeyError,
        OverflowError,
    ):
        return base_response


# ============================================================
# RESULT RANKING VALIDATION
# ============================================================

def validate_results_file(results):

    checks = {
        "root_cause_category": False,
        "machine": False,
        "shift": False,
    }

    if (
        not isinstance(results, list)
        or not results
    ):
        return {
            "checks": checks,
            "passed": False,
        }

    comparison_results = (
        split_results_by_category(results)
    )

    for category in checks:

        category_results = comparison_results.get(
            category,
            [],
        )

        if not category_results:
            continue

        try:

            normalized_results = [
                normalize_exported_result(result)
                for result in category_results
            ]

            seen_groups = set()

            for item in normalized_results:

                group_name = item["group"]

                if group_name in seen_groups:
                    raise ValueError(
                        "Duplicate group"
                    )

                seen_groups.add(group_name)

            results_by_rank = sorted(
                normalized_results,
                key=lambda item: item[
                    "rank_by_total_downtime"
                ],
            )

            ranks = [
                item["rank_by_total_downtime"]
                for item in results_by_rank
            ]

            ranks_are_sequential = (
                ranks
                == list(
                    range(
                        1,
                        len(ranks) + 1,
                    )
                )
            )

            expected_order = sorted(
                normalized_results,
                key=lambda item: (
                    -item[
                        "total_downtime_minutes"
                    ],
                    -item[
                        "incident_count"
                    ],
                    item["group"],
                ),
            )

            ranking_matches = True

            for expected_rank, item in enumerate(
                expected_order,
                start=1,
            ):

                if (
                    item[
                        "rank_by_total_downtime"
                    ]
                    != expected_rank
                ):
                    ranking_matches = False
                    break

            checks[category] = (
                ranks_are_sequential
                and ranking_matches
            )

        except (
            TypeError,
            ValueError,
            KeyError,
            OverflowError,
        ):
            checks[category] = False

    return {
        "checks": checks,
        "passed": all(checks.values()),
    }


# ============================================================
# WEAK CASE AND LIMITATION REVIEW
# ============================================================

def build_weak_case_review(
    complete_incidents,
    coverage,
):

    category_sizes = coverage[
        "category"
    ]["group_sizes"]

    machine_sizes = coverage[
        "machine"
    ]["group_sizes"]

    shift_sizes = coverage[
        "shift"
    ]["group_sizes"]

    weak_cases = []

    weak_cases.append(
        {
            "record_or_group":
                "maintenance",

            "comparison_dimension":
                "root_cause_category",

            "observed_output": (
                f"Maintenance contains "
                f"{category_sizes.get('maintenance', 0)} "
                "observed incidents."
            ),

            "expected_or_questionable_behaviour": (
                "Smaller groups are more sensitive to "
                "individual incidents."
            ),

            "possible_reason": (
                "Maintenance has fewer observed incidents "
                "than some other groups."
            ),

            "data_or_method_issue": (
                "Ranking sensitivity within a small "
                "synthetic dataset."
            ),

            "user_facing_limitation": (
                "The ranking must not be generalized "
                "to a wider industrial population."
            ),

            "required_correction": (
                "No calculation correction required."
            ),
        }
    )

    weak_cases.append(
        {
            "record_or_group":
                "Observed machine groups",

            "comparison_dimension":
                "machine",

            "observed_output": (
                f"The dataset represents "
                f"{len(machine_sizes)} machines across "
                f"{len(complete_incidents)} incidents."
            ),

            "expected_or_questionable_behaviour": (
                "Machine rankings may change when more "
                "incidents are observed."
            ),

            "possible_reason": (
                "Limited observation scope."
            ),

            "data_or_method_issue": (
                "Limited representativeness."
            ),

            "user_facing_limitation": (
                "Rankings describe only the approved "
                "synthetic sample."
            ),

            "required_correction": (
                "Reassess when additional data is available."
            ),
        }
    )

    weak_cases.append(
        {
            "record_or_group":
                "Observed shift groups",

            "comparison_dimension":
                "shift",

            "observed_output": (
                f"The dataset contains "
                f"{len(shift_sizes)} shift groups."
            ),

            "expected_or_questionable_behaviour": (
                "Shift rankings are descriptive."
            ),

            "possible_reason": (
                "The comparison does not control for "
                "all operational factors."
            ),

            "data_or_method_issue": (
                "Track A does not perform causal adjustment."
            ),

            "user_facing_limitation": (
                "Observed differences are not causal evidence."
            ),

            "required_correction": (
                "No calculation correction required."
            ),
        }
    )

    return {
        "project_id": PROJECT_ID,
        "analytical_track": ANALYTICAL_TRACK,
        "data_version": EXPECTED_DATA_VERSION,
        "method_version": METHOD_VERSION,
        "minimum_group_size": MINIMUM_GROUP_SIZE,

        "overall_limitation": (
            "All source incidents are synthetic. Results are "
            "descriptive demonstration outputs and must not "
            "be generalized as real-world industrial "
            "performance or causal evidence."
        ),

        "weak_case_review": weak_cases,

        "small_group_review": {
            "root_cause_category": [
                group
                for group, size in category_sizes.items()
                if size < MINIMUM_GROUP_SIZE
            ],

            "machine": [
                group
                for group, size in machine_sizes.items()
                if size < MINIMUM_GROUP_SIZE
            ],

            "shift": [
                group
                for group, size in shift_sizes.items()
                if size < MINIMUM_GROUP_SIZE
            ],
        },

        "known_limitations": [
            "All source incidents are synthetic.",
            "The observation scope is limited.",
            "Comparative rankings are descriptive.",
            "Results do not establish causal relationships.",
            "Results are not predictive evidence.",
        ],
    }


# ============================================================
# MAIN VALIDATION PROCESS
# ============================================================

def main():

    print("Analytical Track Validation")

    # --------------------------------------------------------
    # Load canonical source data
    # --------------------------------------------------------

    rows = load_csv_rows(
        SOURCE_FILE
    )

    # --------------------------------------------------------
    # Reconstruct incidents
    # --------------------------------------------------------

    incidents = reconstruct_incidents(
        rows
    )

    complete_incidents = (
        get_complete_incidents(
            incidents
        )
    )

    # --------------------------------------------------------
    # Data version detection
    # --------------------------------------------------------

    data_versions_detected = sorted(
        {
            str(
                row.get(
                    "data_version",
                    "",
                )
            ).strip()

            for row in rows

            if str(
                row.get(
                    "data_version",
                    "",
                )
            ).strip()
        }
    )

    # --------------------------------------------------------
    # Synthetic data validation
    # --------------------------------------------------------

    all_records_synthetic = (
        len(rows) > 0
        and all(
            is_true(
                row.get("is_synthetic")
            )
            for row in rows
        )
    )

    # --------------------------------------------------------
    # Invalid numeric rows
    # --------------------------------------------------------

    invalid_numeric_rows = 0

    for row in rows:

        metric_name = str(
            row.get(
                "metric_name",
                "",
            )
        ).strip()

        if metric_name in {
            "downtime_minutes",
            "failure_frequency",
        }:

            if parse_numeric(
                row.get(
                    "metric_value"
                )
            ) is None:

                invalid_numeric_rows += 1

    # --------------------------------------------------------
    # Group coverage
    # --------------------------------------------------------

    category_coverage = (
        build_group_coverage(
            complete_incidents,
            "category",
        )
    )

    machine_coverage = (
        build_group_coverage(
            complete_incidents,
            "entity_id",
        )
    )

    shift_coverage = (
        build_group_coverage(
            complete_incidents,
            "shift",
        )
    )

    # --------------------------------------------------------
    # Load intelligence results
    # --------------------------------------------------------

    try:

        results = load_json(
            RESULTS_FILE
        )

    except (
        FileNotFoundError,
        json.JSONDecodeError,
        OSError,
    ):

        results = []

    # --------------------------------------------------------
    # Diagnostic output
    # --------------------------------------------------------

    print(
        f"Results JSON type: "
        f"{type(results).__name__}"
    )

    print(
        f"Exported results loaded: "
        f"{len(results) if isinstance(results, list) else 0}"
    )

    # --------------------------------------------------------
    # Split results by category
    # --------------------------------------------------------

    comparison_results = (
        split_results_by_category(results)
    )

    # --------------------------------------------------------
    # Validate rankings
    # --------------------------------------------------------

    ranking_validation = (
        validate_results_file(results)
    )

    # --------------------------------------------------------
    # Independent baseline validation
    # --------------------------------------------------------

    baseline_validation = {

        "root_cause_category":
            compare_baseline_to_results(
                build_simple_baseline(
                    complete_incidents,
                    "category",
                ),
                comparison_results[
                    "root_cause_category"
                ],
            ),

        "machine":
            compare_baseline_to_results(
                build_simple_baseline(
                    complete_incidents,
                    "entity_id",
                ),
                comparison_results[
                    "machine"
                ],
            ),

        "shift":
            compare_baseline_to_results(
                build_simple_baseline(
                    complete_incidents,
                    "shift",
                ),
                comparison_results[
                    "shift"
                ],
            ),
    }

    baseline_validation["passed"] = all(
        baseline_validation[group]["passed"]
        for group in (
            "root_cause_category",
            "machine",
            "shift",
        )
    )

    # --------------------------------------------------------
    # Validation checks
    # --------------------------------------------------------

    checks = {

        "source_measurement_rows": {
            "expected":
                EXPECTED_MEASUREMENT_ROWS,

            "actual":
                len(rows),

            "passed":
                len(rows)
                == EXPECTED_MEASUREMENT_ROWS,
        },

        "reconstructed_incidents": {
            "expected":
                EXPECTED_INCIDENTS,

            "actual":
                len(incidents),

            "passed":
                len(incidents)
                == EXPECTED_INCIDENTS,
        },

        "complete_incidents": {
            "expected":
                EXPECTED_INCIDENTS,

            "actual":
                len(complete_incidents),

            "passed":
                len(complete_incidents)
                == EXPECTED_INCIDENTS,
        },

        "data_version": {
            "expected":
                EXPECTED_DATA_VERSION,

            "actual":
                data_versions_detected,

            "passed":
                data_versions_detected
                == [EXPECTED_DATA_VERSION],
        },

        "synthetic_data": {
            "all_records_synthetic":
                all_records_synthetic,

            "passed":
                all_records_synthetic,
        },

        "invalid_numeric_rows": {
            "actual":
                invalid_numeric_rows,

            "passed":
                invalid_numeric_rows == 0,
        },

        "group_coverage": {
            "category":
                category_coverage,

            "machine":
                machine_coverage,

            "shift":
                shift_coverage,

            "passed": (
                category_coverage[
                    "all_incidents_included_once"
                ]
                and machine_coverage[
                    "all_incidents_included_once"
                ]
                and shift_coverage[
                    "all_incidents_included_once"
                ]
            ),
        },

        "ranking_validation":
            ranking_validation,

        "simple_baseline_validation":
            baseline_validation,
    }

    # --------------------------------------------------------
    # Overall status
    # --------------------------------------------------------

    validation_status = (
        "PASS"

        if all(
            check.get(
                "passed",
                False,
            )
            for check in checks.values()
        )

        else "FAIL"
    )

    # --------------------------------------------------------
    # Validation metrics
    # --------------------------------------------------------

    validation_metrics = {
        "project_id": PROJECT_ID,
        "analytical_track": ANALYTICAL_TRACK,
        "method_version": METHOD_VERSION,
        "data_version_expected":
            EXPECTED_DATA_VERSION,
        "data_versions_detected":
            data_versions_detected,
        "validation_status":
            validation_status,
        "checks": checks,
    }

    # --------------------------------------------------------
    # Weak-case review
    # --------------------------------------------------------

    weak_case_review = (
        build_weak_case_review(
            complete_incidents,
            {
                "category":
                    category_coverage,

                "machine":
                    machine_coverage,

                "shift":
                    shift_coverage,
            },
        )
    )

    # --------------------------------------------------------
    # Create output directory
    # --------------------------------------------------------

    VALIDATION_OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Write validation metrics
    # --------------------------------------------------------

    with VALIDATION_OUTPUT.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            validation_metrics,
            file,
            indent=2,
        )

    # --------------------------------------------------------
    # Write weak-case review
    # --------------------------------------------------------

    with WEAK_CASE_OUTPUT.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            weak_case_review,
            file,
            indent=2,
        )

    # --------------------------------------------------------
    # Console output
    # --------------------------------------------------------

    print(
        f"Validation status: "
        f"{validation_status}"
    )

    print(
        f"Measurement rows: "
        f"{len(rows)}"
    )

    print(
        f"Reconstructed incidents: "
        f"{len(incidents)}"
    )

    print(
        f"Complete incidents: "
        f"{len(complete_incidents)}"
    )

    print(
        "Data versions detected: "
        + (
            ", ".join(
                data_versions_detected
            )

            if data_versions_detected
            else "None"
        )
    )

    print(
        "Ranking validation: "
        f"{'PASS' if ranking_validation['passed'] else 'FAIL'}"
    )

    print(
        "Simple baseline validation: "
        f"{'PASS' if baseline_validation['passed'] else 'FAIL'}"
    )

    print(
        "Validation metrics generated: "
        f"{VALIDATION_OUTPUT}"
    )

    print(
        "Weak-case review generated: "
        f"{WEAK_CASE_OUTPUT}"
    )


# ============================================================
# SCRIPT ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
