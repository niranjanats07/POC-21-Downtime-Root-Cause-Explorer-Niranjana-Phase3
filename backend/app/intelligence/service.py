import json
import math
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]

RESULTS_FILE = (
    PROJECT_ROOT
    / "data-science"
    / "outputs"
    / "intelligence_results.json"
)

SUMMARY_FILE = (
    PROJECT_ROOT
    / "data-science"
    / "outputs"
    / "intelligence_summary.json"
)

EXPECTED_PROJECT_ID = "POC-21"
EXPECTED_DATA_VERSION = "1.1.0"
EXPECTED_METHOD_VERSION = "1.0.0"

ALLOWED_CATEGORIES = {
    "root_cause_category",
    "machine",
    "shift",
}

ALLOWED_METRICS = {
    "total_downtime_minutes",
}

REQUIRED_EVIDENCE_FACTORS = {
    "grouping_dimension",
    "incident_count",
    "average_downtime_minutes",
    "total_failure_frequency",
    "average_failure_frequency",
}

REQUIRED_RESULT_FIELDS = {
    "result_id",
    "result_type",
    "group_key",
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

OPTIONAL_NULLABLE_FIELDS = {
    "record_id",
    "entity_id",
    "period_start",
    "period_end",
}


class IntelligenceContractError(ValueError):
    """Raised when intelligence data violates its output contract."""


def _require_non_empty_string(value, field, result_id):
    if not isinstance(value, str) or not value.strip():
        raise IntelligenceContractError(
            f"{result_id}: {field} must be a non-empty string."
        )


def _require_finite_number(value, field, result_id):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise IntelligenceContractError(
            f"{result_id}: {field} must be numeric."
        )

    if not math.isfinite(value):
        raise IntelligenceContractError(
            f"{result_id}: {field} must be finite."
        )

    if value < 0:
        raise IntelligenceContractError(
            f"{result_id}: {field} cannot be negative."
        )


def _validate_timestamp(value, field):
    if not isinstance(value, str) or not value.strip():
        raise IntelligenceContractError(
            f"{field} must be a non-empty ISO timestamp."
        )

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise IntelligenceContractError(
            f"{field} is not a valid ISO timestamp."
        ) from exc

    if parsed.tzinfo is None:
        raise IntelligenceContractError(
            f"{field} must include a timezone."
        )


def _load_json_file(path, label):
    if not path.is_file():
        raise FileNotFoundError(f"{label} not found: {path.name}")

    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as exc:
        raise IntelligenceContractError(
            f"{label} contains invalid JSON: {exc.msg}."
        ) from exc


def _validate_summary(summary, result_count):
    if not isinstance(summary, dict):
        raise IntelligenceContractError(
            "intelligence_summary.json must contain a JSON object."
        )

    required_summary_fields = {
        "project_id",
        "data_version",
        "method_version",
        "total_result_count",
        "validation_result",
        "generation_timestamp",
    }

    missing = required_summary_fields - summary.keys()

    if missing:
        raise IntelligenceContractError(
            f"Summary is missing fields: {sorted(missing)}"
        )

    if summary["project_id"] != EXPECTED_PROJECT_ID:
        raise IntelligenceContractError("Project ID mismatch.")

    if summary["data_version"] != EXPECTED_DATA_VERSION:
        raise IntelligenceContractError("Data version mismatch.")

    if summary["method_version"] != EXPECTED_METHOD_VERSION:
        raise IntelligenceContractError("Method version mismatch.")

    if summary["validation_result"] != "PASS":
        raise IntelligenceContractError(
            "Analytical validation status is not PASS."
        )

    if (
        isinstance(summary["total_result_count"], bool)
        or not isinstance(summary["total_result_count"], int)
    ):
        raise IntelligenceContractError(
            "Summary result count must be an integer."
        )

    if summary["total_result_count"] != result_count:
        raise IntelligenceContractError(
            "Summary/result count mismatch."
        )

    _validate_timestamp(
        summary["generation_timestamp"],
        "Summary generation_timestamp",
    )


def _validate_result(result, index):
    if not isinstance(result, dict):
        raise IntelligenceContractError(
            f"Result at index {index} must be a JSON object."
        )

    missing = REQUIRED_RESULT_FIELDS - result.keys()

    if missing:
        raise IntelligenceContractError(
            f"Result at index {index} is missing fields: "
            f"{sorted(missing)}"
        )

    result_id = result["result_id"]

    _require_non_empty_string(result_id, "result_id", str(index))

    for field in {
        "result_type",
        "group_key",
        "metric_name",
        "result_unit",
        "result_category",
        "finding",
        "method_version",
        "data_version",
        "quality_status",
        "limitation",
    }:
        _require_non_empty_string(result[field], field, result_id)

    if result["result_type"] != "comparative_group_ranking":
        raise IntelligenceContractError(
            f"{result_id}: unsupported result_type."
        )

    if result["result_category"] not in ALLOWED_CATEGORIES:
        raise IntelligenceContractError(
            f"{result_id}: unsupported result_category."
        )

    if result["metric_name"] not in ALLOWED_METRICS:
        raise IntelligenceContractError(
            f"{result_id}: unsupported metric_name."
        )

    if result["result_unit"] != "minutes":
        raise IntelligenceContractError(
            f"{result_id}: unsupported result_unit."
        )

    if result["data_version"] != EXPECTED_DATA_VERSION:
        raise IntelligenceContractError(
            f"{result_id}: data version mismatch."
        )

    if result["method_version"] != EXPECTED_METHOD_VERSION:
        raise IntelligenceContractError(
            f"{result_id}: method version mismatch."
        )

    if result["quality_status"] != "validated":
        raise IntelligenceContractError(
            f"{result_id}: result is not validated."
        )

    _require_finite_number(
        result["result_value"], "result_value", result_id
    )

    rank = result["priority_rank"]

    if isinstance(rank, bool) or not isinstance(rank, int) or rank < 1:
        raise IntelligenceContractError(
            f"{result_id}: priority_rank must be a positive integer."
        )

    for field in OPTIONAL_NULLABLE_FIELDS:
        if field in result and result[field] is not None:
            if not isinstance(result[field], str):
                raise IntelligenceContractError(
                    f"{result_id}: {field} must be a string or null."
                )

    _validate_timestamp(
        result["generated_at"],
        f"{result_id} generated_at",
    )

    evidence = result["evidence"]

    if not isinstance(evidence, list) or not evidence:
        raise IntelligenceContractError(
            f"{result_id}: evidence must be a non-empty array."
        )

    factors = set()

    for entry in evidence:
        if not isinstance(entry, dict):
            raise IntelligenceContractError(
                f"{result_id}: evidence entries must be objects."
            )

        if not {"factor", "value", "contribution"}.issubset(entry):
            raise IntelligenceContractError(
                f"{result_id}: evidence entry has missing fields."
            )

        factor = entry["factor"]

        _require_non_empty_string(factor, "evidence.factor", result_id)

        if factor in factors:
            raise IntelligenceContractError(
                f"{result_id}: duplicate evidence factor {factor}."
            )

        factors.add(factor)

        contribution = entry["contribution"]

        if contribution is not None:
            _require_finite_number(
                contribution,
                "evidence.contribution",
                result_id,
            )

    if factors != REQUIRED_EVIDENCE_FACTORS:
        raise IntelligenceContractError(
            f"{result_id}: evidence factors do not match the contract."
        )


def load_intelligence():
    results = _load_json_file(
        RESULTS_FILE,
        "intelligence_results.json",
    )

    summary = _load_json_file(
        SUMMARY_FILE,
        "intelligence_summary.json",
    )

    if not isinstance(results, list):
        raise IntelligenceContractError(
            "intelligence_results.json must be a JSON array."
        )

    for index, result in enumerate(results):
        _validate_result(result, index)

    result_ids = [item["result_id"] for item in results]

    if len(result_ids) != len(set(result_ids)):
        raise IntelligenceContractError(
            "Duplicate intelligence result IDs detected."
        )

    _validate_summary(summary, len(results))

    return {
        "metadata": {
            "project_id": summary["project_id"],
            "data_version": summary["data_version"],
            "method_version": summary["method_version"],
            "approved_track": summary.get("approved_track"),
            "generated_at": summary["generation_timestamp"],
            "quality_status": summary["validation_result"],
        },
        "summary": summary,
        "results": results,
    }
