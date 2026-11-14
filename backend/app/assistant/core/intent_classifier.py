
import re


def classify_intent(question):
    text = question.casefold()

    result_ids = re.findall(r"\bRES-\d{4}\b", question.upper())
    if result_ids and any(
        word in text for word in ("explain", "evidence", "detail", "result")
    ):
        return {"intent": "explain_result", "result_id": result_ids[0]}

    if any(word in text for word in ("limitation", "limitations", "synthetic", "caveat")):
        return {"intent": "explain_limitation"}

    if any(word in text for word in ("method", "methodology", "calculated", "calculation")):
        return {"intent": "explain_method"}

    if any(word in text for word in ("freshness", "generated", "data version", "method version", "when was")):
        return {"intent": "get_data_freshness"}

    if any(word in text for word in ("compare", "comparison", "rank", "ranking", "all machines", "all shifts", "all categories")):
        return {"intent": "compare_groups"}

    if any(word in text for word in ("top", "highest", "priority", "most downtime", "largest downtime", "which machine", "which shift", "which category", "which root cause")):
        return {"intent": "list_priority_items"}

    if any(word in text for word in ("summary", "overall", "total incidents", "total downtime", "overview")):
        return {"intent": "get_summary"}

    if any(word in text for word in ("show", "describe", "details for", "tell me about")):
        return {"intent": "describe_segment"}

    return {"intent": None}
