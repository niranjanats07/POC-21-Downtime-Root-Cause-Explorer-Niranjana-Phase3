from app.assistant.queries.track_a_queries import (
    get_result_by_id,
    get_results_for_dimension,
)

DIMENSIONS = ("root_cause_category", "machine", "shift")


def _evidence_results(package, maximum=10):
    selected = []
    for dimension in DIMENSIONS:
        selected.extend(get_results_for_dimension(package, dimension))
    selected.sort(
        key=lambda item: (
            item.get("priority_rank", 999999),
            item.get("result_id", ""),
        )
    )
    return selected[:maximum]


def route_query(package, intent, parameters):
    summary = package["summary"]
    metadata = package["metadata"]
    evidence_results = _evidence_results(package)

    if intent == "get_summary":
        return {
            "summary": summary,
            "evidence_results": evidence_results,
        }

    if intent == "list_priority_items":
        dimension = parameters.get("dimension")
        results = (
            get_results_for_dimension(package, dimension)
            if dimension
            else evidence_results
        )
        return {"results": results}

    if intent in ("compare_groups", "describe_segment"):
        dimension = parameters.get("dimension")
        if dimension not in DIMENSIONS:
            return None
        return {
            "dimension": dimension,
            "results": get_results_for_dimension(package, dimension),
        }

    if intent == "explain_result":
        result = get_result_by_id(package, parameters["result_id"])
        return {"result": result} if result else {"result": None}

    if intent == "explain_method":
        return {
            "method_version": metadata["method_version"],
            "approved_track": summary.get("approved_track"),
            "primary_analytical_question": summary.get(
                "primary_analytical_question"
            ),
            "decision_to_be_supported": summary.get(
                "decision_to_be_supported"
            ),
            "evidence_results": evidence_results,
        }

    if intent == "explain_limitation":
        return {
            "limitations": summary.get("important_limitations", []),
            "evidence_results": evidence_results,
        }

    if intent == "get_data_freshness":
        return {
            "metadata": metadata,
            "evidence_results": evidence_results,
        }

    return None
