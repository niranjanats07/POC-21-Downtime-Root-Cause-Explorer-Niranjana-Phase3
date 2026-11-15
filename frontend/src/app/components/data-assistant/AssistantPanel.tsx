"use client";

import { useState } from "react";
import AnswerCard from "./AnswerCard";
import AssistantStatus from "./AssistantStatus";
import EvidenceReferences from "./EvidenceReferences";
import LimitationNotice from "./LimitationNotice";
import QuestionInput from "./QuestionInput";
import SuggestedQuestions from "./SuggestedQuestions";
import UnsupportedQuestionState from "./UnsupportedQuestionState";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type Evidence = {
  result_id: string;
  result_type?: string;
  group_key?: string;
  result_category?: string;
  finding?: string;
  metric_name?: string;
  result_value?: number;
  result_unit?: string;
  priority_rank?: number;
  data_version?: string;
  method_version?: string;
  evidence?: {
    factor: string;
    value: string | number;
    contribution: number | null;
  }[];
};

type GeminiStatus =
  | "generated"
  | "fallback_missing_key"
  | "fallback_error"
  | "fallback_invalid"
  | "not_attempted";

type AssistantResponse = {
  answer_id: string;
  status: "answered" | "unsupported" | "unsafe" | "unavailable" | "error";
  intent: string | null;
  answer: string;
  evidence_references: Evidence[];
  key_values: Record<string, unknown>;
  metadata: {
    data_version?: string;
    method_version?: string;
    generated_at?: string;
    quality_status?: string;
  } | null;
  limitation: string | null;
  suggested_follow_ups: string[];
  gemini_explanation: string | null;
  gemini_status: GeminiStatus;
};

function GeminiExplanation({
  explanation,
  status,
}: {
  explanation: string | null;
  status: GeminiStatus;
}) {
  if (status === "generated" && explanation) {
    return (
      <section
        aria-labelledby="gemini-explanation-title"
        className="rounded-xl border border-violet-800/70 bg-violet-950/30 p-5"
      >
        <div className="flex flex-wrap items-center gap-2">
          <h3
            id="gemini-explanation-title"
            className="text-sm font-semibold text-violet-200"
          >
            Gemini explanation
          </h3>
          <span className="rounded-full border border-violet-700 bg-violet-900/50 px-2 py-1 text-xs text-violet-200">
            Generated
          </span>
        </div>

        <p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-slate-200">
          {explanation}
        </p>

        <p className="mt-3 text-xs leading-5 text-slate-400">
          This explanation uses approved deterministic findings. The
          deterministic answer and evidence remain the authoritative results.
        </p>
      </section>
    );
  }

  let message =
    "Gemini could not provide a validated explanation. The deterministic answer and its evidence are still available.";

  if (status === "fallback_missing_key") {
    message =
      "Gemini is not configured on the backend. The deterministic answer and its evidence are still available.";
  } else if (status === "fallback_error") {
    message =
      "Gemini is temporarily unavailable or its request failed. The deterministic answer and its evidence are still available.";
  } else if (status === "fallback_invalid") {
    message =
      "Gemini returned an explanation that did not pass grounding validation. It has been withheld; the deterministic answer and its evidence are still available.";
  } else if (status === "not_attempted") {
    message =
      "A Gemini explanation was not requested for this response. The deterministic response remains available.";
  }

  return (
    <section
      aria-labelledby="gemini-explanation-title"
      className="rounded-xl border border-amber-800/70 bg-amber-950/20 p-5"
    >
      <div className="flex flex-wrap items-center gap-2">
        <h3
          id="gemini-explanation-title"
          className="text-sm font-semibold text-amber-200"
        >
          Gemini explanation
        </h3>
        <span className="rounded-full border border-amber-800 bg-amber-950/50 px-2 py-1 text-xs text-amber-200">
          Deterministic fallback
        </span>
      </div>

      <p className="mt-3 text-sm leading-6 text-slate-300">{message}</p>
    </section>
  );
}

export default function AssistantPanel() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState<AssistantResponse | null>(null);
  const [requestStatus, setRequestStatus] = useState<
    "idle" | "loading" | "success" | "error"
  >("idle");
  const [error, setError] = useState("");

  async function ask(value = question) {
    const trimmed = value.trim();

    if (!trimmed || trimmed.length > 500 || requestStatus === "loading") {
      return;
    }

    setQuestion(trimmed);
    setResponse(null);
    setError("");
    setRequestStatus("loading");

    try {
      const result = await fetch(`${API}/api/assistant/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: trimmed }),
      });

      if (!result.ok) {
        const detail = await result.json().catch(() => null);
        throw new Error(detail?.detail || `Request failed (${result.status}).`);
      }

      const data = (await result.json()) as AssistantResponse;

      const validStatuses = [
        "answered",
        "unsupported",
        "unsafe",
        "unavailable",
        "error",
      ];

      const validGeminiStatuses = [
        "generated",
        "fallback_missing_key",
        "fallback_error",
        "fallback_invalid",
        "not_attempted",
      ];

      if (
        !data ||
        typeof data.answer !== "string" ||
        !validStatuses.includes(data.status) ||
        !Array.isArray(data.evidence_references) ||
        !Array.isArray(data.suggested_follow_ups)
      ) {
        throw new Error(
          "The assistant response did not match the expected response contract."
        );
      }

      if (data.status === "answered") {
        if (
          typeof data.intent !== "string" ||
          !data.metadata ||
          typeof data.metadata.data_version !== "string" ||
          typeof data.metadata.method_version !== "string" ||
          typeof data.metadata.generated_at !== "string" ||
          typeof data.metadata.quality_status !== "string" ||
          typeof data.limitation !== "string" ||
          !validGeminiStatuses.includes(data.gemini_status) ||
          !(
            data.gemini_explanation === null ||
            typeof data.gemini_explanation === "string"
          )
        ) {
          throw new Error(
            "The answered response did not match the expected Mode B contract."
          );
        }

        if (
          data.gemini_status === "generated" &&
          !data.gemini_explanation?.trim()
        ) {
          throw new Error(
            "The assistant returned an invalid Gemini explanation."
          );
        }
      } else if (
        data.metadata !== null &&
        (typeof data.metadata !== "object" || Array.isArray(data.metadata))
      ) {
        throw new Error("The unsupported response contains invalid metadata.");
      }

      setResponse(data);
      setRequestStatus("success");
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Assistant request failed."
      );
      setRequestStatus("error");
    }
  }

  return (
    <section
      aria-labelledby="data-assistant-title"
      className="space-y-5 rounded-2xl border border-cyan-900/70 bg-slate-900 p-6 shadow-xl"
    >
      <div>
        <div className="flex flex-wrap items-center gap-2">
          <span className="rounded-full border border-cyan-800 bg-cyan-950/50 px-3 py-1 text-xs font-medium text-cyan-300">
            POST #5
          </span>

          <span className="rounded-full border border-violet-800 bg-violet-950/40 px-3 py-1 text-xs font-medium text-violet-200">
            Mode B · Grounded Gemini explanation
          </span>
        </div>

        <h2
          id="data-assistant-title"
          className="mt-3 text-xl font-semibold text-white"
        >
          Grounded Data Assistant
        </h2>

        <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">
          Ask questions about approved comparative intelligence. Deterministic
          retrieval provides the findings and evidence; Gemini provides a
          separately validated natural-language explanation.
        </p>
      </div>

      <SuggestedQuestions
        onSelect={(value) => {
          setQuestion(value);
          void ask(value);
        }}
        disabled={requestStatus === "loading"}
      />

      <QuestionInput
        value={question}
        onChange={setQuestion}
        onSubmit={() => void ask()}
        disabled={requestStatus === "loading"}
      />

      <AssistantStatus
        status={requestStatus}
        message={requestStatus === "error" ? error : undefined}
      />

      {response && (
        <div className="space-y-4">
          {response.status === "answered" ? (
            <>
              {response.intent && (
                <AnswerCard
                  answer={response.answer}
                  intent={response.intent}
                />
              )}

              <GeminiExplanation
                explanation={response.gemini_explanation}
                status={response.gemini_status}
              />

              <EvidenceReferences items={response.evidence_references} />
            </>
          ) : (
            <UnsupportedQuestionState
              status={response.status}
              answer={response.answer}
            />
          )}

          {response.limitation && <LimitationNotice text={response.limitation} />}

          {response.suggested_follow_ups.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-slate-200">
                Suggested follow-ups
              </h3>

              <div className="mt-2 flex flex-wrap gap-2">
                {response.suggested_follow_ups.slice(0, 3).map((item) => (
                  <button
                    key={item}
                    type="button"
                    disabled={requestStatus === "loading"}
                    onClick={() => {
                      setQuestion(item);
                      void ask(item);
                    }}
                    className="rounded-full border border-slate-700 px-3 py-2 text-xs text-slate-300 hover:border-cyan-700 hover:text-cyan-200 disabled:opacity-50"
                  >
                    {item}
                  </button>
                ))}
              </div>
            </div>
          )}

          {response.metadata?.data_version && (
            <p className="text-xs text-slate-500">
              Data {response.metadata.data_version} · Method{" "}
              {response.metadata.method_version} · Quality{" "}
              {response.metadata.quality_status} · Generated{" "}
              {response.metadata.generated_at}
            </p>
          )}
        </div>
      )}
    </section>
  );
}
