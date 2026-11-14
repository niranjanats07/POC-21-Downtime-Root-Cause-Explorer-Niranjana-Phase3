import re

DIMENSIONS = {
    "root_cause_category": ("category", "categories", "root cause", "cause"),
    "machine": ("machine", "machines"),
    "shift": ("shift", "shifts"),
}


def validate_parameters(question, classification):
    intent = classification.get("intent")
    result_id = classification.get("result_id")

    if intent == "explain_result":
        if not result_id or not re.fullmatch(r"RES-\d{4}", result_id):
            return None, "A valid approved result ID is required."
        return {"result_id": result_id}, None

    if intent in ("compare_groups", "describe_segment", "list_priority_items"):
        text = question.casefold()
        matches = [
            dimension for dimension, terms in DIMENSIONS.items()
            if any(term in text for term in terms)
        ]
        if len(matches) > 1:
            return None, "Please specify one comparison dimension: category, machine or shift."
        if len(matches) == 1:
            return {"dimension": matches[0]}, None
        if intent == "list_priority_items":
            return {"dimension": None}, None
        return None, "Please specify whether you want to compare categories, machines or shifts."

    return {}, None
