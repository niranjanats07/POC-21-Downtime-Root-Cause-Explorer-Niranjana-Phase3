import re
from app.assistant.core.policy import get_policy, get_supported_intents

UNSAFE_PATTERNS = [
    r"\b(system prompt|hidden prompt|developer instructions)\b",
    r"\b(api[_ -]?key|password|secret|environment variables?)\b",
    r"\b(reveal|show|print|display|expose|dump)\b.{0,60}\b(instructions|secrets|credentials|tokens)\b",
    r"\b(ignore (all )?(previous|prior) instructions|reveal your instructions)\b",
    r"\b(ignore|bypass|override|disregard)\b.{0,60}\b(previous|prior|all|safety|security|system|assistant|scope|rules|restrictions|limitations)\b",
    r"\b(follow|obey|execute)\b.{0,80}\b(instructions|commands|directions)\b",
    r"\b(answer|respond|operate)\b.{0,60}\b(without restrictions|without limitations|without rules)\b",
    r"\b(source|source data|source description|record|document|evidence|dataset)\b.{0,120}\b(instructs?|instructions|commands|tells you|says to|asks you to)\b",
    r"\b(export|download|dump|show|list|return)\b.{0,100}\b(all|every|complete|entire)\b.{0,80}\b(canonical|raw|source)?\s*(data|records|rows|incidents)\b",
    r"\b(arbitrary sql|execute code|run python|shell command)\b",
]

UNSUPPORTED_PATTERNS = [
    r"\b(predict|prediction|forecast|forecasting)\b",
    r"\b(causal|root cause why|prove that .* caused)\b",
    r"\b(statistical significance|p[- ]value|confidence interval)\b",
    r"\b(trend|over time|period change|month[- ]to[- ]month)\b",
    r"\b(probability of failure|failure probability)\b",
]


def check_scope(question):
    policy = get_policy()
    get_supported_intents()

    if not isinstance(question, str) or not question.strip():
        return "unsupported", "Please enter a question."

    if len(question) > policy["question_max_characters"]:
        return "unsupported", "The question exceeds the 500-character limit."

    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, question, re.IGNORECASE):
            return "unsafe", "This request is outside the assistant's permitted security scope."
    for pattern in UNSUPPORTED_PATTERNS:
        if re.search(pattern, question, re.IGNORECASE):
            return "unsupported", "This capability is not supported by the approved Track A results."

    return "supported", None
