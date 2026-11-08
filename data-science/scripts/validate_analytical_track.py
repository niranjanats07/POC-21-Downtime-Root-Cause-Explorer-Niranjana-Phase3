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

EXPECTED_RESULT_COUNT = 11

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
# REQUIRED FLAT RESULT FIELDS
# ============================================================

REQUIRED_RESULT_FIELDS = {
    "result_id",
    "result_type",
    "record_id",
    "entity_id",
    "group_key",
    "period_start",
    "period_end",
    "metric_name",
    "result_value",
    "result_unit",
    "result_category",
    "priority_rank",
    "finding",
    "evidence",
    "method_version",
    "data_version",
    "generated_at",
    "quality_status",
    "limitation",
}


# ============================================================
# FILE LOADING
# ============================================================

def load_csv_rows(file_path: Path) -> list[dict[str, str]]:

    with file_path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        return list(csv.DictReader(file))


def load_json(file_path: Path):

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


# ============================================================
# VALUE NORMALISATION
# ============================================================

def is_true(value) -> bool:

    return str(value).strip().lower() in {
        "true",
        "1",
        "yes",
        "y",
    }


def parse_numeric(value):

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
            incident["duplicate_required_metric"] = True

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

        "total_incident_assignments":
            total_assignments,

        "complete_incident_count":
            complete_incident_count,

        "all_incidents_included_once": (
            total_assignments
            == complete_incident_count
        ),

        "group_sizes": dict(
            sorted(group_sizes.items())
        ),
    }


# ============================================================
# INDEPENDENT BASELINE CALCULATION
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
                    values[
                        "total_downtime_minutes"
                    ],

                "total_failure_frequency":
                    values[
                        "total_failure_frequency"
                    ],
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
# FLAT EXPORT STRUCTURE VALIDATION
# ============================================================

def validate_flat_results_structure(results):

    response = {
        "is_flat_array": isinstance(results, list),

        "expected_result_count":
            EXPECTED_RESULT_COUNT,

        "actual_result_count":
            len(results)
            if isinstance(results, list)
            else 0,

        "required_fields_present": False,

        "unique_result_ids": False,

        "versions_match": False,

        "quality_status_validated": False,

        "valid_result_categories": False,

        "passed": False,
    }

    if not isinstance(results, list):
        return response

    required_fields_present = all(
        isinstance(result, dict)
        and REQUIRED_RESULT_FIELDS.issubset(
            result.keys()
        )
        for result in results
    )

    result_ids = [
        result.get("result_id")
        for result in results
        if isinstance(result, dict)
    ]

    unique_result_ids = (
        len(result_ids)
        == len(set(result_ids))
        and len(result_ids)
        == len(results)
        and None not in result_ids
    )

    versions_match = all(
        isinstance(result, dict)
        and result.get("method_version")
        == METHOD_VERSION
        and result.get("data_version")
        == EXPECTED_DATA_VERSION
        for result in results
    )

    quality_status_validated = all(
        isinstance(result, dict)
        and result.get("quality_status")
        == "validated"
        for result in results
    )

    allowed_categories = {
        "root_cause_category",
        "machine",
        "shift",
    }

    valid_result_categories = all(
        isinstance(result, dict)
        and result.get("result_category")
        in allowed_categories
        for result in results
    )

    response.update(
        {
            "required_fields_present":
                required_fields_present,

            "unique_result_ids":
                unique_result_ids,

            "versions_match":
                versions_match,

            "quality_status_validated":
                quality_status_validated,

            "valid_result_categories":
                valid_result_categories,
        }
    )

    response["passed"] = (
        response["is_flat_array"]
        and response["actual_result_count"]
        == EXPECTED_RESULT_COUNT
        and required_fields_present
        and unique_result_ids
        and versions_match
        and quality_status_validated
        and valid_result_categories
    )

    return response


# ============================================================
# FLAT EXPORT GROUPING
# ============================================================

def build_flat_export_groups(results):

    grouped = {
        "root_cause_category": [],
        "machine": [],
        "shift": [],
    }

    if not isinstance(results, list):
        return grouped

    for result in results:

        if not isinstance(result, dict):
            continue

        category = str(
            result.get(
                "result_category",
                "",
            )
        ).strip()

        if category in grouped:
            grouped[category].append(result)

    return grouped


# ============================================================
# EVIDENCE EXTRACTION
# ============================================================

def get_evidence_value(
    result,
    factor_name,
):

    evidence = result.get(
        "evidence",
        [],
    )

    if not isinstance(evidence, list):
        return None

    for item in evidence:

        if not isinstance(item, dict):
            continue

        if item.get("factor") == factor_name:
            return item.get("value")

    return None


# ============================================================
# FLAT RESULT RANKING VALIDATION
# ============================================================

def validate_flat_rankings(comparison_results):

    checks = {}

    for category, results in comparison_results.items():

        checks[category] = False

        if not results:
            continue

        try:

            seen_groups = set()

            normalized = []

            for result in results:

                group_name = str(
                    result.get(
                        "group_key",
                        "",
                    )
                ).strip()

                result_value = float(
                    result.get(
                        "result_value",
                        0,
                    )
                )

                priority_rank = int(
                    result.get(
                        "priority_rank",
                        0,
                    )
                )

                incident_count = int(
                    get_evidence_value(
                        result,
                        "incident_count",
                    )
                )

                if not group_name:
                    raise ValueError(
                        "Missing group"
                    )

                if group_name in seen_groups:
                    raise ValueError(
                        "Duplicate group"
                    )

                if priority_rank < 1:
                    raise ValueError(
                        "Invalid rank"
                    )

                if incident_count < 1:
                    raise ValueError(
                        "Invalid incident count"
                    )

                if not math.isfinite(result_value):
                    raise ValueError(
                        "Invalid result value"
                    )

                seen_groups.add(group_name)

                normalized.append(
                    {
                        "group":
                            group_name,

                        "result_value":
                            result_value,

                        "incident_count":
                            incident_count,

                        "priority_rank":
                            priority_rank,
                    }
                )

            ranked_results = sorted(
                normalized,
                key=lambda item:
                    item["priority_rank"],
            )

            ranks = [
                item["priority_rank"]
                for item in ranked_results
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
                normalized,
                key=lambda item: (
                    -item["result_value"],
                    -item["incident_count"],
                    item["group"],
                ),
            )

            ranking_matches = all(
                item["priority_rank"]
                == expected_rank
                for expected_rank, item in enumerate(
                    expected_order,
                    start=1,
                )
            )

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

        "passed":
            all(checks.values()),
    }


# ============================================================
# INDEPENDENT BASELINE COMPARISON
# ============================================================

def compare_flat_results_to_baseline(
    baseline_results,
    exported_results,
):

    response = {
        "baseline_group_count":
            len(baseline_results),

        "exported_group_count":
            len(exported_results),

        "groups_match": False,

        "incident_counts_match": False,

        "downtime_totals_match": False,

        "failure_frequency_totals_match":
            False,

        "ranks_match": False,

        "minimum_group_size_passed":
            False,

        "passed": False,
    }

    if not exported_results:
        return response

    try:

        baseline_by_group = {
            item["group"]: item
            for item in baseline_results
        }

        exported_by_group = {}

        for result in exported_results:

            group_name = str(
                result.get(
                    "group_key",
                    "",
                )
            ).strip()

            if not group_name:
                return response

            if group_name in exported_by_group:
                return response

            exported_by_group[group_name] = result

        groups_match = (
            set(baseline_by_group.keys())
            == set(exported_by_group.keys())
        )

        incident_counts_match = (
            groups_match
            and all(
                int(
                    get_evidence_value(
                        exported_by_group[group],
                        "incident_count",
                    )
                )
                == baseline_by_group[group][
                    "incident_count"
                ]
                for group in baseline_by_group
            )
        )

        downtime_totals_match = (
            groups_match
            and all(
                math.isclose(
                    float(
                        exported_by_group[group][
                            "result_value"
                        ]
                    ),
                    baseline_by_group[group][
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
                    float(
                        get_evidence_value(
                            exported_by_group[group],
                            "total_failure_frequency",
                        )
                    ),
                    baseline_by_group[group][
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
                int(
                    exported_by_group[group][
                        "priority_rank"
                    ]
                )
                == baseline_by_group[group][
                    "rank_by_total_downtime"
                ]
                for group in baseline_by_group
            )
        )

        minimum_group_size_passed = (
            groups_match
            and all(
                baseline_by_group[group][
                    "incident_count"
                ]
                >= MINIMUM_GROUP_SIZE
                for group in baseline_by_group
            )
        )

        response.update(
            {
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

                "minimum_group_size_passed":
                    minimum_group_size_passed,
            }
        )

        response["passed"] = (
            groups_match
            and incident_counts_match
            and downtime_totals_match
            and failure_frequency_totals_match
            and ranks_match
            and minimum_group_size_passed
        )

        return response

    except (
        TypeError,
        ValueError,
        KeyError,
        OverflowError,
    ):

        return response


# ============================================================
# WEAK CASE REVIEW
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

    return {
        "project_id":
            PROJECT_ID,

        "analytical_track":
            ANALYTICAL_TRACK,

        "data_version":
            EXPECTED_DATA_VERSION,

        "method_version":
            METHOD_VERSION,

        "minimum_group_size":
            MINIMUM_GROUP_SIZE,

        "overall_limitation": (
            "All source incidents are synthetic. "
            "Results are descriptive demonstration outputs "
            "and must not be generalized as real-world "
            "industrial performance, causal evidence or "
            "predictive evidence."
        ),

        "small_group_review": {

            "root_cause_category": [
                group
                for group, size
                in category_sizes.items()
                if size < MINIMUM_GROUP_SIZE
            ],

            "machine": [
                group
                for group, size
                in machine_sizes.items()
                if size < MINIMUM_GROUP_SIZE
            ],

            "shift": [
                group
                for group, size
                in shift_sizes.items()
                if size < MINIMUM_GROUP_SIZE
            ],
        },

        "known_limitations": [
            "All source incidents are synthetic.",
            "The observation scope is limited.",
            "Comparative rankings are descriptive.",
            "Results do not establish causal relationships.",
            "Results are not predictive evidence.",
            "Rankings may change when additional observations become available.",
        ],

        "weak_case_review": [
            {
                "comparison_dimension":
                    "root_cause_category",

                "minimum_group_size":
                    MINIMUM_GROUP_SIZE,

                "group_sizes":
                    category_sizes,
            },

            {
                "comparison_dimension":
                    "machine",

                "minimum_group_size":
                    MINIMUM_GROUP_SIZE,

                "group_sizes":
                    machine_sizes,
            },

            {
                "comparison_dimension":
                    "shift",

                "minimum_group_size":
                    MINIMUM_GROUP_SIZE,

                "group_sizes":
                    shift_sizes,
            },
        ],
    }


# ============================================================
# MAIN VALIDATION PROCESS
# ============================================================

def main():

    print("Analytical Track Validation")

    rows = load_csv_rows(
        SOURCE_FILE
    )

    incidents = reconstruct_incidents(
        rows
    )

    complete_incidents = (
        get_complete_incidents(
            incidents
        )
    )

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

    all_records_synthetic = (
        len(rows) > 0
        and all(
            is_true(
                row.get("is_synthetic")
            )
            for row in rows
        )
    )

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
                row.get("metric_value")
            ) is None:

                invalid_numeric_rows += 1

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

    try:

        results = load_json(
            RESULTS_FILE
        )

    except (
        FileNotFoundError,
        json.JSONDecodeError,
        OSError,
    ):

        results = None

    print(
        f"Results JSON type: "
        f"{type(results).__name__}"
    )

    flat_structure_validation = (
        validate_flat_results_structure(
            results
        )
    )

    comparison_results = (
        build_flat_export_groups(
            results
        )
    )

    ranking_validation = (
        validate_flat_rankings(
            comparison_results
        )
    )

    baseline_validation = {

        "root_cause_category":
            compare_flat_results_to_baseline(
                build_simple_baseline(
                    complete_incidents,
                    "category",
                ),
                comparison_results[
                    "root_cause_category"
                ],
            ),

        "machine":
            compare_flat_results_to_baseline(
                build_simple_baseline(
                    complete_incidents,
                    "entity_id",
                ),
                comparison_results[
                    "machine"
                ],
            ),

        "shift":
            compare_flat_results_to_baseline(
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

        "flat_export_structure":
            flat_structure_validation,

        "ranking_validation":
            ranking_validation,

        "independent_baseline_validation":
            baseline_validation,
    }

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

    validation_metrics = {
        "project_id":
            PROJECT_ID,

        "analytical_track":
            ANALYTICAL_TRACK,

        "method_version":
            METHOD_VERSION,

        "data_version_expected":
            EXPECTED_DATA_VERSION,

        "data_versions_detected":
            data_versions_detected,

        "validation_status":
            validation_status,

        "checks":
            checks,
    }

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

    VALIDATION_OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with VALIDATION_OUTPUT.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            validation_metrics,
            file,
            indent=2,
        )

    with WEAK_CASE_OUTPUT.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            weak_case_review,
            file,
            indent=2,
        )

    print(
        f"Exported results loaded: "
        f"{len(results) if isinstance(results, list) else 0}"
    )

    print(
        f"Validation status: "
        f"{validation_status}"
    )

    print(
        "Flat export validation: "
        f"{'PASS' if flat_structure_validation['passed'] else 'FAIL'}"
    )

    print(
        "Ranking validation: "
        f"{'PASS' if ranking_validation['passed'] else 'FAIL'}"
    )

    print(
        "Independent baseline validation: "
        f"{'PASS' if baseline_validation['passed'] else 'FAIL'}"
    )

    print(
        f"Validation metrics generated: "
        f"{VALIDATION_OUTPUT}"
    )

    print(
        f"Weak-case review generated: "
        f"{WEAK_CASE_OUTPUT}"
    )


# ============================================================
# SCRIPT ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()