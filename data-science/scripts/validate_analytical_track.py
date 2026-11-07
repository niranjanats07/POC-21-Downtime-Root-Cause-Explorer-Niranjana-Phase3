from __future__ import annotations

import csv
import json
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

MINIMUM_GROUP_SIZE = 1


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

def load_csv_rows(file_path):
    """Load CSV records as dictionaries."""

    with file_path.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        return list(csv.DictReader(file))


def load_json(file_path):
    """Load a JSON file."""

    with file_path.open(
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


# ============================================================
# VALUE NORMALISATION
# ============================================================

def is_true(value):
    """Return True when a value represents boolean true."""

    return str(value).strip().lower() in {
        "true",
        "1",
        "yes",
        "y",
    }


def parse_numeric(value):
    """
    Convert a value to float.

    Returns None when the value cannot be converted.
    """

    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    try:
        return float(value)

    except (TypeError, ValueError):
        return None


# ============================================================
# INCIDENT RECONSTRUCTION
# ============================================================

def reconstruct_incidents(rows):
    """
    Reconstruct incidents from canonical measurement rows.

    Each source incident should contain:
    - one downtime_minutes measurement
    - one failure_frequency measurement

    The source_record_id is used as the incident identifier.
    """

    incidents = {}

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
            }

        metric_name = str(
            row.get("metric_name", "")
        ).strip()

        numeric_value = parse_numeric(
            row.get("metric_value")
        )

        if metric_name in {
            "downtime_minutes",
            "failure_frequency",
        }:

            if numeric_value is None:

                incidents[incident_id][
                    "invalid_numeric"
                ] = True

            else:

                incidents[incident_id][
                    metric_name
                ] = numeric_value

    return incidents


# ============================================================
# COMPLETE INCIDENT VALIDATION
# ============================================================

def get_complete_incidents(incidents):
    """
    Return incidents containing both required measurements
    and required comparison fields.
    """

    complete_incidents = []

    for incident in incidents.values():

        if incident["invalid_numeric"]:
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

        complete_incidents.append(
            incident
        )

    return complete_incidents


# ============================================================
# GROUP COVERAGE
# ============================================================

def build_group_coverage(
    complete_incidents,
    field_name
):
    """
    Build coverage information for one grouping dimension.
    """

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
        "complete_incident_count": (
            complete_incident_count
        ),
        "all_incidents_included_once": (
            total_assignments
            == complete_incident_count
        ),
        "group_sizes": dict(
            sorted(group_sizes.items())
        ),
    }


# ============================================================

# ============================================================
# SIMPLE BASELINE VALIDATION
# ============================================================

def build_simple_baseline(
    complete_incidents,
    field_name
):
    """
    Independently calculate group totals from reconstructed
    complete incidents for baseline validation.
    """

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
        start=1
    ):
        result[
            "rank_by_total_downtime"
        ] = rank

    return baseline_results

# ============================================================
# BASELINE COMPARISON
# ============================================================

def compare_baseline_to_results(
    baseline_results,
    exported_results
):
    """
    Compare independently calculated baseline results against
    exported analytical results.
    """

    if (
        not isinstance(exported_results, list)
        or not exported_results
    ):
        return {
            "baseline_group_count":
                len(baseline_results),
            "exported_group_count": 0,
            "groups_match": False,
            "incident_counts_match": False,
            "downtime_totals_match": False,
            "failure_frequency_totals_match": False,
            "ranks_match": False,
            "passed": False,
        }

    baseline_by_group = {
        item["group"]: item
        for item in baseline_results
    }

    exported_by_group = {}

    try:

        for item in exported_results:

            group_name = str(
                item.get("group", "")
            ).strip()

            if not group_name:
                raise ValueError(
                    "Missing group name"
                )

            exported_by_group[group_name] = item

        groups_match = (
            set(baseline_by_group.keys())
            == set(exported_by_group.keys())
        )

        incident_counts_match = groups_match and all(
            baseline_by_group[group][
                "incident_count"
            ]
            == int(
                exported_by_group[group].get(
                    "incident_count"
                )
            )
            for group in baseline_by_group
        )

        downtime_totals_match = groups_match and all(
            abs(
                baseline_by_group[group][
                    "total_downtime_minutes"
                ]
                - float(
                    exported_by_group[group].get(
                        "total_downtime_minutes"
                    )
                )
            ) < 1e-9
            for group in baseline_by_group
        )

        failure_frequency_totals_match = (
            groups_match
            and all(
                abs(
                    baseline_by_group[group][
                        "total_failure_frequency"
                    ]
                    - float(
                        exported_by_group[group].get(
                            "total_failure_frequency"
                        )
                    )
                ) < 1e-9
                for group in baseline_by_group
            )
        )

        ranks_match = groups_match and all(
            baseline_by_group[group][
                "rank_by_total_downtime"
            ]
            == int(
                exported_by_group[group].get(
                    "rank_by_total_downtime"
                )
            )
            for group in baseline_by_group
        )

    except (
        TypeError,
        ValueError,
    ):

        return {
            "baseline_group_count":
                len(baseline_results),
            "exported_group_count":
                len(exported_results),
            "groups_match": False,
            "incident_counts_match": False,
            "downtime_totals_match": False,
            "failure_frequency_totals_match": False,
            "ranks_match": False,
            "passed": False,
        }

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
        "groups_match": groups_match,
        "incident_counts_match":
            incident_counts_match,
        "downtime_totals_match":
            downtime_totals_match,
        "failure_frequency_totals_match":
            failure_frequency_totals_match,
        "ranks_match": ranks_match,
        "passed": passed,
    }
# RESULT VALIDATION
# ============================================================

def validate_results_file(results):
    """
    Validate the exported Track A intelligence results.

    Expected structure:

    {
        ...
        "comparisons": {
            "root_cause_category": [...],
            "machine": [...],
            "shift": [...]
        }
    }

    Ranking rule must match the analytical generator:

    1. Descending total downtime
    2. Descending incident count
    3. Ascending group name

    Ranks must be sequential:
    1, 2, 3, ..., N
    """

    checks = {
        "root_cause_category": False,
        "machine": False,
        "shift": False,
    }

    required_categories = list(
        checks.keys()
    )

    # --------------------------------------------------------
    # Results must be a non-empty JSON object
    # --------------------------------------------------------

    if (
        not isinstance(results, dict)
        or not results
    ):

        return {
            "checks": checks,
            "passed": False,
        }

    comparisons = results.get(
        "comparisons"
    )

    # --------------------------------------------------------
    # Comparisons must be a dictionary
    # --------------------------------------------------------

    if not isinstance(
        comparisons,
        dict
    ):

        return {
            "checks": checks,
            "passed": False,
        }

    # --------------------------------------------------------
    # Validate each comparison dimension
    # --------------------------------------------------------

    for category in required_categories:

        category_results = comparisons.get(
            category,
            []
        )

        if (
            not isinstance(
                category_results,
                list
            )
            or not category_results
        ):

            checks[category] = False

            continue

        normalized_results = []

        try:

            # --------------------------------------------
            # Validate and normalise every result record
            # --------------------------------------------

            for result in category_results:

                if not isinstance(
                    result,
                    dict
                ):

                    raise TypeError(
                        "Comparison record must "
                        "be a dictionary"
                    )

                group_key = str(
                    result.get(
                        "group",
                        ""
                    )
                ).strip()

                priority_rank = int(
                    result.get(
                        "rank_by_total_downtime"
                    )
                )

                total_downtime = float(
                    result.get(
                        "total_downtime_minutes"
                    )
                )

                incident_count = int(
                    result.get(
                        "incident_count"
                    )
                )

                if not group_key:

                    raise ValueError(
                        "Missing group name"
                    )

                if priority_rank < 1:

                    raise ValueError(
                        "Invalid rank"
                    )

                if total_downtime < 0:

                    raise ValueError(
                        "Negative downtime"
                    )

                if incident_count < 1:

                    raise ValueError(
                        "Invalid incident count"
                    )

                normalized_results.append(
                    {
                        "group_key":
                            group_key,

                        "priority_rank":
                            priority_rank,

                        "total_downtime":
                            total_downtime,

                        "incident_count":
                            incident_count,
                    }
                )

            # --------------------------------------------
            # Validate sequential ranks
            # --------------------------------------------

            results_by_rank = sorted(
                normalized_results,
                key=lambda item:
                    item["priority_rank"]
            )

            ranks = [
                item["priority_rank"]
                for item in results_by_rank
            ]

            ranks_are_sequential = (
                ranks
                == list(
                    range(
                        1,
                        len(ranks) + 1
                    )
                )
            )

            # --------------------------------------------
            # Independently reproduce expected ranking
            #
            # 1. Total downtime descending
            # 2. Incident count descending
            # 3. Group name ascending
            # --------------------------------------------

            expected_order = sorted(
                normalized_results,
                key=lambda item: (
                    -item["total_downtime"],
                    -item["incident_count"],
                    item["group_key"],
                )
            )

            ranking_matches = True

            for expected_rank, item in enumerate(
                expected_order,
                start=1
            ):

                if (
                    item["priority_rank"]
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
        ):

            checks[category] = False

    return {
        "checks": checks,
        "passed": all(
            checks.values()
        ),
    }
# ============================================================
# WEAK CASE AND LIMITATION REVIEW
# ============================================================

def build_weak_case_review(
    complete_incidents,
    coverage
):
    """
    Build explicit weak-case and limitation review.

    These entries document known limitations without treating
    descriptive results as causal or predictive evidence.
    """

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

    # --------------------------------------------------------
    # Root-cause category sensitivity
    # --------------------------------------------------------

    if "maintenance" in category_sizes:

        weak_cases.append(
            {
                "record_or_group":
                    "maintenance",

                "comparison_dimension":
                    "root_cause_category",

                "observed_output": (
                    f"Maintenance contains "
                    f"{category_sizes['maintenance']} "
                    "observed incidents in the approved "
                    "dataset."
                ),

                "expected_or_questionable_behaviour": (
                    "The observed ranking is valid for the "
                    "approved dataset, but smaller group "
                    "sizes make totals and averages more "
                    "sensitive to individual incidents."
                ),

                "possible_reason": (
                    "Maintenance has fewer observed incidents "
                    "than some other root-cause groups."
                ),

                "data_or_method_issue": (
                    "No calculation error was identified. "
                    "The limitation is ranking sensitivity "
                    "within a small synthetic dataset."
                ),

                "user_facing_limitation": (
                    "This observed ranking must not be "
                    "generalized to a wider industrial "
                    "population."
                ),

                "required_correction": (
                    "No correction to the approved "
                    "calculation. Retain the limitation and "
                    "reassess when additional canonical data "
                    "is available."
                ),
            }
        )

    # --------------------------------------------------------
    # Machine representativeness
    # --------------------------------------------------------

    weak_cases.append(
        {
            "record_or_group":
                "Observed machine groups",

            "comparison_dimension":
                "machine",

            "observed_output": (
                f"The approved dataset represents "
                f"{len(machine_sizes)} machines across "
                f"{len(complete_incidents)} complete "
                "incidents."
            ),

            "expected_or_questionable_behaviour": (
                "Machine rankings are deterministic for the "
                "current dataset but may change when "
                "additional incidents are observed."
            ),

            "possible_reason": (
                "Only a limited number of machines are "
                "represented and the observation period is "
                "limited."
            ),

            "data_or_method_issue": (
                "Limited representativeness rather than a "
                "calculation failure."
            ),

            "user_facing_limitation": (
                "Machine rankings describe only the approved "
                "synthetic sample and are not population-wide "
                "performance rankings."
            ),

            "required_correction": (
                "No correction to the current approved "
                "method. Reassess ranking stability if the "
                "canonical dataset expands."
            ),
        }
    )

    # --------------------------------------------------------
    # Shift interpretation
    # --------------------------------------------------------

    weak_cases.append(
        {
            "record_or_group":
                "Observed shift groups",

            "comparison_dimension":
                "shift",

            "observed_output": (
                f"The approved dataset contains "
                f"{len(shift_sizes)} observed shift groups."
            ),

            "expected_or_questionable_behaviour": (
                "Comparative shift rankings are descriptive "
                "and must not be interpreted as causal shift "
                "effects."
            ),

            "possible_reason": (
                "The comparison does not control for "
                "operating hours, production volume or "
                "other unobserved factors."
            ),

            "data_or_method_issue": (
                "Track A is descriptive and does not "
                "perform causal adjustment."
            ),

            "user_facing_limitation": (
                "Observed shift differences are comparison "
                "signals only and are not causal evidence."
            ),

            "required_correction": (
                "No calculation correction. Preserve the "
                "explicit non-causal interpretation."
            ),
        }
    )

    # --------------------------------------------------------
    # Ranking stability
    # --------------------------------------------------------

    weak_cases.append(
        {
            "record_or_group":
                "All comparison groups",

            "comparison_dimension":
                "ranking_stability",

            "observed_output": (
                "Rankings are calculated deterministically "
                "using total downtime as the primary ordering "
                "rule, followed by incident count and group "
                "name for deterministic tie handling."
            ),

            "expected_or_questionable_behaviour": (
                "Small datasets can experience ranking "
                "changes when a small number of additional "
                "incidents are introduced."
            ),

            "possible_reason": (
                f"The approved canonical dataset contains "
                f"only {len(complete_incidents)} distinct "
                "synthetic incidents."
            ),

            "data_or_method_issue": (
                "Ranking stability is limited by sample size "
                "and observation scope."
            ),

            "user_facing_limitation": (
                "Ranks should be treated as observed-sample "
                "priorities, not stable population rankings."
            ),

            "required_correction": (
                "No correction to the deterministic ranking "
                "method. Retain the stability limitation and "
                "reassess with additional canonical "
                "observations."
            ),
        }
    )

    # --------------------------------------------------------
    # Synthetic data scope
    # --------------------------------------------------------

    weak_cases.append(
        {
            "record_or_group":
                "All analytical outputs",

            "comparison_dimension":
                "synthetic_data_scope",

            "observed_output": (
                "All comparative findings are generated from "
                "the approved synthetic canonical dataset."
            ),

            "expected_or_questionable_behaviour": (
                "Results demonstrate the approved analytical "
                "method but do not demonstrate real-world "
                "industrial performance."
            ),

            "possible_reason": (
                "The project source data is explicitly "
                "synthetic."
            ),

            "data_or_method_issue": (
                "This is a source-data limitation rather "
                "than a calculation error."
            ),

            "user_facing_limitation": (
                "Do not use these results as predictive, "
                "causal or generalizable industrial evidence."
            ),

            "required_correction": (
                "No correction within the approved Track A "
                "scope. Real-world claims would require an "
                "appropriate non-synthetic canonical dataset."
            ),
        }
    )

    # --------------------------------------------------------
    # Small group review
    # --------------------------------------------------------

    small_group_review = {
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
    }

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
            "All source incidents are synthetic. Results are "
            "descriptive demonstration outputs and must not "
            "be generalized as real-world industrial "
            "performance or causal evidence."
        ),

        "weak_case_review":
            weak_cases,

        "small_group_review":
            small_group_review,

        "known_limitations": [
            "All 30 source incidents are synthetic.",

            (
                "Only a limited number of machines are "
                "represented."
            ),

            "The observation period is limited.",

            (
                "Sampling methodology and population "
                "inclusion probabilities are not established."
            ),

            "The wider machine population is unknown.",

            "Geographic coordinates are unavailable.",

            "Lifecycle-stage information is unavailable.",

            "Source accuracy is not independently verified.",

            (
                "Small group sizes may affect ranking "
                "stability."
            ),

            (
                "Comparative rankings are descriptive and do "
                "not establish causal relationships."
            ),

            (
                "Observed comparative results are not "
                "predictive evidence."
            ),
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
                    ""
                )
            ).strip()

            for row in rows

            if str(
                row.get(
                    "data_version",
                    ""
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
                row.get(
                    "is_synthetic"
                )
            )
            for row in rows
        )
    )

    # --------------------------------------------------------
    # Invalid numeric measurement rows
    # --------------------------------------------------------

    invalid_numeric_rows = 0

    for row in rows:

        metric_name = str(
            row.get(
                "metric_name",
                ""
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
    ):

        results = {}

    # --------------------------------------------------------
    # Validate exported rankings
    # --------------------------------------------------------

    ranking_validation = (
        validate_results_file(
            results
        )
    )

    # --------------------------------------------------------
    # Validation checks
    # --------------------------------------------------------
    # --------------------------------------------------------
    # Independent simple baseline validation
    # --------------------------------------------------------

    baseline_validation = {
        "root_cause_category": compare_baseline_to_results(
            build_simple_baseline(
                complete_incidents,
                "category"
            ),
            results["comparisons"]["root_cause_category"]
        ),
        "machine": compare_baseline_to_results(
            build_simple_baseline(
                complete_incidents,
                "entity_id"
            ),
            results["comparisons"]["machine"]
        ),
        "shift": compare_baseline_to_results(
            build_simple_baseline(
                complete_incidents,
                "shift"
            ),
            results["comparisons"]["shift"]
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

            "passed": (
                len(rows)
                == EXPECTED_MEASUREMENT_ROWS
            ),
        },

        "reconstructed_incidents": {
            "expected":
                EXPECTED_INCIDENTS,

            "actual":
                len(incidents),

            "passed": (
                len(incidents)
                == EXPECTED_INCIDENTS
            ),
        },

        "complete_incidents": {
            "expected":
                EXPECTED_INCIDENTS,

            "actual":
                len(complete_incidents),

            "passed": (
                len(complete_incidents)
                == EXPECTED_INCIDENTS
            ),
        },

        "data_version": {
            "expected":
                EXPECTED_DATA_VERSION,

            "actual":
                data_versions_detected,

            "passed": (
                data_versions_detected
                == [EXPECTED_DATA_VERSION]
            ),
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

            "passed": (
                invalid_numeric_rows == 0
            ),
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
                and category_coverage[
                    "group_count"
                ] > 0
                and machine_coverage[
                    "group_count"
                ] > 0
                and shift_coverage[
                    "group_count"
                ] > 0
            ),
        },

        "ranking_validation":
            ranking_validation,
    
        "simple_baseline_validation":
            baseline_validation,
    }

    # --------------------------------------------------------
    # Overall validation status
    # --------------------------------------------------------

    validation_status = (
        "PASS"

        if all(
            check.get(
                "passed",
                False
            )
            for check in checks.values()
        )

        else "FAIL"
    )

    # --------------------------------------------------------
    # Build validation metrics output
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Build weak-case review
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
        encoding="utf-8"
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
        encoding="utf-8"
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






