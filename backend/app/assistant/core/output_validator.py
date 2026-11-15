REQUIRED_FIELDS = {
    "answer_id",
    "status",
    "intent",
    "answer",
    "evidence_references",
    "key_values",
    "metadata",
    "limitation",
    "suggested_follow_ups",
    "gemini_explanation",
    "gemini_status",
}

VALID_STATUSES = {
    "answered",
    "unsupported",
    "unsafe",
    "unavailable",
    "error",
}

VALID_GEMINI_STATUSES = {
    "generated",
    "fallback_missing_key",
    "fallback_error",
    "fallback_invalid",
    "not_attempted",
}


def validate_response(response):
    if not isinstance(response, dict):
        raise ValueError("Assistant response must be an object.")

    if not REQUIRED_FIELDS.issubset(response):
        raise ValueError(
            "Assistant response does not satisfy its output contract."
        )

    if response["status"] not in VALID_STATUSES:
        raise ValueError("Invalid assistant response status.")

    if response["gemini_status"] not in VALID_GEMINI_STATUSES:
        raise ValueError("Invalid Gemini explanation status.")

    if response["gemini_explanation"] is not None and not isinstance(
        response["gemini_explanation"], str
    ):
        raise ValueError("Gemini explanation must be text or null.")

    if not isinstance(response["evidence_references"], list):
        raise ValueError("Evidence references must be a list.")

    if not isinstance(response["suggested_follow_ups"], list):
        raise ValueError("Suggested follow-ups must be a list.")

    if not isinstance(response["key_values"], dict):
        raise ValueError("Key values must be an object.")

    if not isinstance(response["metadata"], dict):
        raise ValueError("Metadata must be an object.")

    if len(response["evidence_references"]) > 10:
        raise ValueError("Evidence reference limit exceeded.")

    if len(response["suggested_follow_ups"]) > 3:
        raise ValueError("Follow-up limit exceeded.")

    if response["gemini_status"] == "generated":
        if not response["gemini_explanation"]:
            raise ValueError(
                "Generated Gemini status requires an explanation."
            )

    elif response["gemini_explanation"] is not None:
        raise ValueError(
            "Fallback Gemini status must not contain an explanation."
        )

    return response
