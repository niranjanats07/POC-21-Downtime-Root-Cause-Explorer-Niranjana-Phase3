import json
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

EXPECTED_DATA_VERSION = "1.1.0"
EXPECTED_METHOD_VERSION = "1.0.0"


def load_intelligence():
    if not RESULTS_FILE.exists():
        raise FileNotFoundError("intelligence_results.json not found.")

    if not SUMMARY_FILE.exists():
        raise FileNotFoundError("intelligence_summary.json not found.")

    with RESULTS_FILE.open("r", encoding="utf-8") as file:
        results = json.load(file)

    with SUMMARY_FILE.open("r", encoding="utf-8") as file:
        summary = json.load(file)

    if not isinstance(results, list):
        raise ValueError("intelligence_results.json must be a JSON array.")

    if summary.get("data_version") != EXPECTED_DATA_VERSION:
        raise ValueError("Data version mismatch.")

    if summary.get("method_version") != EXPECTED_METHOD_VERSION:
        raise ValueError("Method version mismatch.")

    required_fields = {
        "result_id",
        "result_type",
        "group_key",
        "metric_name",
        "result_value",
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

    for result in results:
        missing = required_fields - result.keys()

        if missing:
            raise ValueError(
                f"Intelligence result is missing fields: {sorted(missing)}"
            )

        if result["data_version"] != EXPECTED_DATA_VERSION:
            raise ValueError("Result data version mismatch.")

        if result["method_version"] != EXPECTED_METHOD_VERSION:
            raise ValueError("Result method version mismatch.")

        if result["quality_status"] not in {
            "validated",
            "conditional",
            "rejected",
        }:
            raise ValueError("Unsupported quality status.")

    result_ids = [item["result_id"] for item in results]

    if len(result_ids) != len(set(result_ids)):
        raise ValueError("Duplicate intelligence result IDs detected.")

    if summary.get("total_result_count") != len(results):
        raise ValueError("Summary/result count mismatch.")

    return {
        "metadata": {
            "project_id": summary.get("project_id"),
            "data_version": summary.get("data_version"),
            "method_version": summary.get("method_version"),
            "approved_track": summary.get("approved_track"),
            "generated_at": summary.get("generation_timestamp"),
            "quality_status": summary.get("validation_result"),
        },
        "summary": summary,
        "results": results,
    }