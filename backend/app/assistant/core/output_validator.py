REQUIRED_FIELDS = {
    "answer_id", "status", "intent", "answer", "evidence_references",
    "key_values", "metadata", "limitation", "suggested_follow_ups",
}


def validate_response(response):
    if not isinstance(response, dict) or not REQUIRED_FIELDS.issubset(response):
        raise ValueError("Assistant response does not satisfy its output contract.")
    if response["status"] not in {"answered", "unsupported", "unsafe", "unavailable", "error"}:
        raise ValueError("Invalid assistant response status.")
    if len(response["evidence_references"]) > 10:
        raise ValueError("Evidence reference limit exceeded.")
    if len(response["suggested_follow_ups"]) > 3:
        raise ValueError("Follow-up limit exceeded.")
    return response
