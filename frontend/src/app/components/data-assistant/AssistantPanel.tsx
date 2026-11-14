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
  result_id: string; result_type?: string; group_key?: string;
  result_category?: string; finding?: string; metric_name?: string;
  result_value?: number; result_unit?: string; priority_rank?: number;
  data_version?: string; method_version?: string;
  evidence?: { factor: string; value: string | number; contribution: number | null }[];
};

type AssistantResponse = {
  answer_id: string;
  status: "answered" | "unsupported" | "unsafe" | "unavailable" | "error";
  intent: string;
  answer: string;
  evidence_references: Evidence[];
  key_values: Record<string, unknown>;
  metadata: { data_version: string; method_version: string; generated_at: string; quality_status: string };
  limitation: string;
  suggested_follow_ups: string[];
};

export default function AssistantPanel() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState<AssistantResponse | null>(null);
  const [requestStatus, setRequestStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [error, setError] = useState("");

  async function ask(value = question) {
    const trimmed = value.trim();
    if (!trimmed || trimmed.length > 500 || requestStatus === "loading") return;
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
      const data = await result.json() as AssistantResponse;
      if (!data || typeof data.answer !== "string" || !data.metadata ||
          !Array.isArray(data.evidence_references) || !Array.isArray(data.suggested_follow_ups)) {
        throw new Error("The assistant response did not match the expected response contract.");
      }
      setResponse(data);
      setRequestStatus("success");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Assistant request failed.");
      setRequestStatus("error");
    }
  }

  return (
    <section aria-labelledby="data-assistant-title" className="space-y-5 rounded-2xl border border-cyan-900/70 bg-slate-900 p-6 shadow-xl">
      <div>
        <div className="flex flex-wrap items-center gap-2">
          <span className="rounded-full border border-cyan-800 bg-cyan-950/50 px-3 py-1 text-xs font-medium text-cyan-300">POST #5</span>
          <span className="text-xs text-slate-400">Mode A · Deterministic guided assistant</span>
        </div>
        <h2 id="data-assistant-title" className="mt-3 text-xl font-semibold text-white">Grounded Data Assistant</h2>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">
          Ask questions about approved comparative intelligence. Answers use validated Track A results and show their evidence and limitations.
        </p>
      </div>

      <SuggestedQuestions onSelect={(value) => { setQuestion(value); void ask(value); }} disabled={requestStatus === "loading"} />
      <QuestionInput value={question} onChange={setQuestion} onSubmit={() => void ask()} disabled={requestStatus === "loading"} />

      <AssistantStatus status={requestStatus} message={requestStatus === "error" ? error : undefined} />

      {response && (
        <div className="space-y-4">
          {response.status === "answered" ? (
            <>
              <AnswerCard answer={response.answer} intent={response.intent} />
              <EvidenceReferences items={response.evidence_references} />
            </>
          ) : (
            <UnsupportedQuestionState status={response.status} answer={response.answer} />
          )}

          <LimitationNotice text={response.limitation} />

          {response.suggested_follow_ups.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-slate-200">Suggested follow-ups</h3>
              <div className="mt-2 flex flex-wrap gap-2">
                {response.suggested_follow_ups.slice(0, 3).map((item) => (
                  <button key={item} type="button" disabled={requestStatus === "loading"}
                    onClick={() => { setQuestion(item); void ask(item); }}
                    className="rounded-full border border-slate-700 px-3 py-2 text-xs text-slate-300 hover:border-cyan-700 hover:text-cyan-200 disabled:opacity-50">
                    {item}
                  </button>
                ))}
              </div>
            </div>
          )}

          <p className="text-xs text-slate-500">
            Data {response.metadata.data_version} · Method {response.metadata.method_version} · Quality {response.metadata.quality_status} · Generated {response.metadata.generated_at}
          </p>
        </div>
      )}
    </section>
  );
}
