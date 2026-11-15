import io
import json
import sys
from pathlib import Path
import urllib.error

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.assistant import service
from app.assistant.core import gemini_explainer
from app.assistant.core.gemini_explainer import (
    generate_explanation,
    validate_explanation,
)


APPROVED_CONTEXT = {
    "deterministic_answer": (
        "Machine comparison by observed downtime: "
        "#1 MCH-02: 850 minutes (RES-0005)."
    ),
    "key_values": {
        "groups": [
            {
                "result_id": "RES-0005",
                "group": "MCH-02",
                "rank": 1,
                "downtime": 850,
                "unit": "minutes",
            }
        ]
    },
    "evidence_references": [{"result_id": "RES-0005"}],
    "limitation": "All source incidents are synthetic.",
}


def call_gemini():
    return generate_explanation(
        "Why is MCH-02 ranked first?",
        APPROVED_CONTEXT["deterministic_answer"],
        APPROVED_CONTEXT["key_values"],
        APPROVED_CONTEXT["evidence_references"],
        APPROVED_CONTEXT["limitation"],
    )


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


def test_missing_api_key_returns_safe_fallback(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    explanation, status = call_gemini()

    assert explanation is None
    assert status == "fallback_missing_key"


def test_gemini_api_error_returns_safe_fallback(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-placeholder")

    def fake_urlopen(request, timeout):
        raise RuntimeError("Simulated API or quota failure")

    monkeypatch.setattr(
        gemini_explainer.urllib.request,
        "urlopen",
        fake_urlopen,
    )

    explanation, status = call_gemini()

    assert explanation is None
    assert status == "fallback_error"


def test_gemini_quota_exhaustion_returns_safe_fallback(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-placeholder")

    def fake_urlopen(request, timeout):
        error_body = json.dumps({
            "error": {
                "code": 429,
                "status": "RESOURCE_EXHAUSTED",
                "message": "Simulated Gemini quota exhaustion",
            }
        }).encode("utf-8")

        raise urllib.error.HTTPError(
            url=request.full_url,
            code=429,
            msg="Too Many Requests",
            hdrs=None,
            fp=io.BytesIO(error_body),
        )

    monkeypatch.setattr(
        gemini_explainer.urllib.request,
        "urlopen",
        fake_urlopen,
    )

    explanation, status = call_gemini()

    assert explanation is None
    assert status == "fallback_error"

    monkeypatch.setattr(
        service,
        "generate_explanation",
        lambda **kwargs: call_gemini(),
    )

    response = service.answer_question(
        "Why is MCH-02 ranked first?"
    )

    assert response["status"] == "answered"
    assert "MCH-02" in response["answer"]
    assert "850 minutes" in response["answer"]
    assert response["gemini_status"] == "fallback_error"
    assert response["gemini_explanation"] is None

    assert "RES-0005" in [
        item["result_id"]
        for item in response["evidence_references"]
    ]

    assert "synthetic" in response["limitation"].lower()


def test_successful_gemini_response_is_accepted(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-placeholder")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-3.8-flash")

    expected_explanation = (
        "MCH-02 ranks first with 850 observed downtime minutes. "
        "The approved comparison identifies it as the highest-ranked "
        "machine in this dataset."
    )

    payload = {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {"text": expected_explanation}
                    ]
                }
            }
        ]
    }

    def fake_urlopen(request, timeout):
        assert timeout == gemini_explainer.GEMINI_TIMEOUT_SECONDS
        assert request.get_method() == "POST"
        assert request.get_header("X-goog-api-key") == "test-placeholder"
        return FakeResponse(payload)

    monkeypatch.setattr(
        gemini_explainer.urllib.request,
        "urlopen",
        fake_urlopen,
    )

    explanation, status = call_gemini()

    assert status == "generated"
    assert explanation == expected_explanation


def test_invalid_numeric_claim_is_rejected():
    explanation = (
        "MCH-02 ranks first with 999 observed downtime minutes."
    )

    assert validate_explanation(
        explanation, APPROVED_CONTEXT
    ) is False


def test_contradictory_ranking_is_rejected():
    explanation = "MCH-02 ranks second in the approved comparison."

    assert validate_explanation(
        explanation, APPROVED_CONTEXT
    ) is False


def test_unsupported_causal_claim_is_rejected():
    explanation = (
        "MCH-02 ranks first because of bearing failure."
    )

    assert validate_explanation(
        explanation, APPROVED_CONTEXT
    ) is False


def test_valid_grounded_explanation_is_accepted():
    explanation = (
        "MCH-02 ranks first with 850 observed downtime minutes. "
        "The approved comparison identifies it as the highest-ranked "
        "machine in this dataset."
    )

    assert validate_explanation(
        explanation, APPROVED_CONTEXT
    ) is True


def test_gemini_failure_preserves_deterministic_response(monkeypatch):
    monkeypatch.setattr(
        service,
        "generate_explanation",
        lambda **kwargs: (None, "fallback_error"),
    )

    response = service.answer_question(
        "Why is MCH-02 ranked first?"
    )

    assert response["status"] == "answered"
    assert "MCH-02" in response["answer"]
    assert "850 minutes" in response["answer"]
    assert response["gemini_status"] == "fallback_error"
    assert response["gemini_explanation"] is None

    assert "RES-0005" in [
        item["result_id"]
        for item in response["evidence_references"]
    ]

    assert "synthetic" in response["limitation"].lower()
