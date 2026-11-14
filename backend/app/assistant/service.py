
import uuid

from app.assistant.core.policy import get_policy, get_supported_intents
from app.assistant.core.scope_guard import check_scope
from app.assistant.core.intent_classifier import classify_intent
from app.assistant.core.parameter_validator import validate_parameters
from app.assistant.core.query_router import route_query
from app.assistant.core.evidence_builder import build_evidence
from app.assistant.core.response_composer import compose_answer
from app.assistant.core.output_validator import validate_response
from app.intelligence.service import load_intelligence


def _response(status, question, answer=None, intent=None, evidence=None,
              key_values=None, metadata=None, limitation=None, follow_ups=None):
    policy = get_policy()
    response = {
        "answer_id": str(uuid.uuid4()),
        "status": status,
        "intent": intent,
        "answer": answer,
        "evidence_references": (evidence or [])[:policy["evidence_max_references"]],
        "key_values": key_values or {},
        "metadata": metadata or {},
        "limitation": limitation,
        "suggested_follow_ups": (follow_ups or [])[:policy["follow_up_max_items"]],
    }
    return validate_response(response)


def _comparison_values(results):
    ordered = sorted(
        results,
        key=lambda item: (
            item.get("priority_rank", 999999),
            item.get("result_id", ""),
        ),
    )
    return {
        "result_count": len(ordered),
        "groups": [
            {
                "result_id": item.get("result_id"),
                "group": item.get("group_key"),
                "rank": item.get("priority_rank"),
                "downtime": item.get("result_value"),
                "unit": item.get("result_unit"),
            }
            for item in ordered
        ],
    }


def answer_question(question):
    policy = get_policy()
    scope_status, scope_message = check_scope(question)

    if scope_status != "supported":
        status = "unsafe" if scope_status == "unsafe" else "unsupported"
        return _response(status, question, answer=scope_message)

    classification = classify_intent(question)
    intent = classification.get("intent")
    allowed = get_supported_intents()["supported_intents"]

    if intent not in allowed:
        return _response(
            "unsupported",
            question,
            answer=(
                "I can answer questions about approved Track A summaries, "
                "category/machine/shift comparisons, evidence, methodology, "
                "limitations and data freshness."
            ),
        )

    parameters, parameter_error = validate_parameters(question, classification)
    if parameter_error:
        return _response(
            "unsupported",
            question,
            answer=parameter_error,
            intent=intent,
        )

    try:
        package = load_intelligence()
    except (OSError, ValueError, KeyError, TypeError):
        return _response(
            "unavailable",
            question,
            answer="Approved intelligence results are unavailable or failed contract validation.",
            intent=intent,
        )

    metadata = package["metadata"]
    if (
        metadata.get("data_version") != policy["allowed_data_version"]
        or metadata.get("method_version") != policy["allowed_method_version"]
        or str(metadata.get("quality_status", "")).upper()
        != policy["require_quality_status"]
    ):
        return _response(
            "unavailable",
            question,
            answer="The approved data or method version does not match the assistant policy.",
            intent=intent,
            metadata=metadata,
        )

    payload = route_query(package, intent, parameters or {})
    if payload is None or (
        intent == "explain_result" and payload.get("result") is None
    ):
        return _response(
            "unavailable",
            question,
            answer="The requested approved result is not available.",
            intent=intent,
            metadata=metadata,
        )

    evidence = build_evidence(
        payload,
        maximum=policy["evidence_max_references"],
        excerpt_limit=policy["evidence_excerpt_max_characters"],
    )
    answer = compose_answer(intent, payload)

    key_values = {}

    if intent == "get_summary":
        key_values = payload["summary"].get("overall_metrics", {})

    elif intent == "explain_result":
        result = payload["result"]
        key_values = {
            "result_id": result["result_id"],
            "group": result["group_key"],
            "result_value": result["result_value"],
            "result_unit": result["result_unit"],
            "priority_rank": result["priority_rank"],
        }

    elif intent in ("compare_groups", "describe_segment", "list_priority_items"):
        key_values = _comparison_values(payload.get("results", []))

    elif intent == "get_data_freshness":
        key_values = dict(payload.get("metadata", {}))

    elif intent == "explain_limitation":
        key_values = {"limitations": payload.get("limitations", [])}

    limitation = (
        "All source incidents are synthetic. These results are descriptive "
        "demonstration outputs only; they do not establish causation, prediction "
        "or actual industrial performance."
    )

    return _response(
        "answered",
        question,
        answer=answer,
        intent=intent,
        evidence=evidence,
        key_values=key_values,
        metadata=metadata,
        limitation=limitation,
        follow_ups=[
            "Compare machines by observed downtime.",
            "Which shift ranks highest by observed downtime?",
            "What limitations apply to these results?",
        ],
    )
