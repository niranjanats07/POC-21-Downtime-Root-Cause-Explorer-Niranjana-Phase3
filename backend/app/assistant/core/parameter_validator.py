import re

DIMENSIONS = {
    "root_cause_category": ("category", "categories", "root cause", "cause"),
    "machine": ("machine", "machines"),
    "shift": ("shift", "shifts"),
}

MACHINE_ID_PATTERN = re.compile(r"MCH-\d{2}\Z", re.IGNORECASE)


def validate_parameters(question, classification):
    intent = classification.get("intent")
    result_id = classification.get("result_id")

    if intent == "explain_result":
        if not result_id or not re.fullmatch(r"RES-\d{4}", result_id):
            return None, "A valid approved result ID is required."
        return {"result_id": result_id}, None

    if intent in ("compare_groups", "describe_segment", "list_priority_items"):
        text = question.casefold()
        dimension = classification.get("dimension")
        group_key = classification.get("group_key")

        if group_key is not None:
            if (
                not isinstance(group_key, str)
                or not MACHINE_ID_PATTERN.fullmatch(group_key)
                or dimension != "machine"
            ):
                return None, "Please provide a valid approved machine ID."

            return {
                "dimension": "machine",
                "group_key": group_key.upper(),
            }, None

        matches = [
            item for item, terms in DIMENSIONS.items()
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
