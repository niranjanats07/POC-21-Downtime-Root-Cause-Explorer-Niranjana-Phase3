
import math
import re


RESULT_ID_PATTERN = re.compile(r"RES-\d{4}\Z")

ALLOWED_SCALAR_TYPES = (str, int, float, bool, type(None))


def _is_valid_scalar(value):
    if not isinstance(value, ALLOWED_SCALAR_TYPES):
        return False

    if isinstance(value, float) and not math.isfinite(value):
        return False

    return True


def _validated_evidence_items(raw_evidence):
    if not isinstance(raw_evidence, list):
        return []

    validated = []

    for item in raw_evidence[:5]:
        if not isinstance(item, dict):
            continue

        if set(item.keys()) != {"factor", "value", "contribution"}:
            continue

        if not isinstance(item.get("factor"), str):
            continue

        if not item["factor"].strip():
            continue

        if not _is_valid_scalar(item.get("value")):
            continue

        if not _is_valid_scalar(item.get("contribution")):
            continue

        validated.append({
            "factor": item["factor"],
            "value": item["value"],
            "contribution": item["contribution"],
        })

    return validated


def build_evidence(payload, maximum=10, excerpt_limit=300):
    if not isinstance(payload, dict):
        return []

    references = []
    seen = set()

    def add_result(result):
        if not isinstance(result, dict):
            return

        result_id = result.get("result_id")

        if (
            not isinstance(result_id, str)
            or not RESULT_ID_PATTERN.fullmatch(result_id)
            or result_id in seen
        ):
            return

        if result.get("result_type") != "comparative_group_ranking":
            return

        finding = result.get("finding")

        if not isinstance(finding, str):
            return

        seen.add(result_id)

        references.append({
            "result_id": result_id,
            "result_type": result.get("result_type"),
            "group_key": result.get("group_key"),
            "result_category": result.get("result_category"),
            "finding": finding[:excerpt_limit],
            "metric_name": result.get("metric_name"),
            "result_value": result.get("result_value"),
            "result_unit": result.get("result_unit"),
            "priority_rank": result.get("priority_rank"),
            "evidence": _validated_evidence_items(
                result.get("evidence", [])
            ),
            "data_version": result.get("data_version"),
            "method_version": result.get("method_version"),
            "quality_status": result.get("quality_status"),
        })

    add_result(payload.get("result"))

    for result in payload.get("results", []):
        add_result(result)

    for result in payload.get("evidence_results", []):
        add_result(result)

    try:
        safe_maximum = max(0, min(int(maximum), 10))
    except (TypeError, ValueError, OverflowError):
        safe_maximum = 10

    return references[:safe_maximum]
