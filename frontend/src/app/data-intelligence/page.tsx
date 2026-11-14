
"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import TrackAComparison from "./TrackAComparison";
import AssistantPanel from "../components/data-assistant/AssistantPanel";

const API =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const EXPECTED_DATA_VERSION = "1.1.0";
const EXPECTED_METHOD_VERSION = "1.0.0";
const DIAGNOSTIC_REFERENCE = "DI-POC21-LOAD";

const STALE_AFTER_DAYS = (() => {
  const configured = Number(
    process.env.NEXT_PUBLIC_INTELLIGENCE_STALE_AFTER_DAYS
  );

  return Number.isFinite(configured) && configured > 0
    ? configured
    : 7;
})();

type IntelligenceResult = {
  result_id: string;
  result_type: string;
  group_key: string;
  metric_name: string;
  result_value: number;
  result_category: string;
  priority_rank: number;
  finding: string;
  evidence: {
    factor: string;
    value: string | number;
    contribution: number | null;
  }[];
  method_version: string;
  data_version: string;
  generated_at: string;
  quality_status: string;
  limitation: string;
};

type IntelligenceSummary = {
  project_id?: string;
  data_version?: string;
  method_version?: string;
  approved_track?: string;
  validation_result?: string;
  generation_timestamp?: string;
  total_result_count?: number;
  overall_metrics?: { incident_count?: number };
  [key: string]: unknown;
};

type IntelligenceMetadata = {
  data_version?: string;
  method_version?: string;
  generated_at?: string;
};

export default function DataIntelligencePage() {
  const [summary, setSummary] =
    useState<IntelligenceSummary | null>(null);
  const [results, setResults] =
    useState<IntelligenceResult[]>([]);
  const [generatedAt, setGeneratedAt] = useState("");
  const [freshnessCheckedAt, setFreshnessCheckedAt] =
    useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedDimension, setSelectedDimension] =
    useState("all");
  const [retryCount, setRetryCount] = useState(0);

  useEffect(() => {
    let cancelled = false;

    async function loadData() {
      try {
        setLoading(true);
        setError("");

        const [
          summaryResponse,
          resultsResponse,
          metadataResponse,
        ] = await Promise.all([
          fetch(`${API}/api/intelligence/summary`),
          fetch(`${API}/api/intelligence/results`),
          fetch(`${API}/api/intelligence/metadata`),
        ]);

        if (!summaryResponse.ok) {
          throw new Error(
            "Unable to load intelligence summary."
          );
        }

        if (!resultsResponse.ok) {
          throw new Error(
            "Unable to load intelligence results."
          );
        }

        if (!metadataResponse.ok) {
          throw new Error(
            "Unable to load intelligence metadata."
          );
        }

        const summaryData: IntelligenceSummary =
          await summaryResponse.json();

        const resultsData: unknown =
          await resultsResponse.json();

        const metadataData: IntelligenceMetadata =
          await metadataResponse.json();

        if (!Array.isArray(resultsData)) {
          throw new Error(
            "The intelligence results response has an invalid format."
          );
        }

        if (
          metadataData.data_version !== EXPECTED_DATA_VERSION ||
          metadataData.method_version !== EXPECTED_METHOD_VERSION
        ) {
          throw new Error(
            "Intelligence metadata version mismatch."
          );
        }

        if (
          summaryData.data_version !== EXPECTED_DATA_VERSION ||
          summaryData.method_version !== EXPECTED_METHOD_VERSION
        ) {
          throw new Error(
            "Intelligence version mismatch. The approved data or method version is not being served."
          );
        }

        const validatedResults =
          resultsData as IntelligenceResult[];

        for (const result of validatedResults) {
          if (
            result.data_version !== EXPECTED_DATA_VERSION ||
            result.method_version !== EXPECTED_METHOD_VERSION
          ) {
            throw new Error(
              "One or more intelligence results have a version mismatch."
            );
          }
        }

        if (cancelled) return;

        setSummary(summaryData);
        setResults(validatedResults);
        setGeneratedAt(
          metadataData.generated_at ||
            summaryData.generation_timestamp ||
            ""
        );
        setFreshnessCheckedAt(Date.now());
      } catch (err) {
        if (cancelled) return;

        setError(
          err instanceof Error
            ? err.message
            : "Unable to load the Data Intelligence page."
        );
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadData();

    return () => {
      cancelled = true;
    };
  }, [retryCount]);

  const filteredResults = useMemo(() => {
    if (selectedDimension === "all") {
      return results;
    }

    return results.filter(
      (result) =>
        result.result_category === selectedDimension
    );
  }, [results, selectedDimension]);

  const generatedAtDate = generatedAt
    ? new Date(generatedAt)
    : null;

  const generatedAtTimestamp =
    generatedAtDate?.getTime();

  const generatedAtValid =
    freshnessCheckedAt !== null &&
    generatedAtTimestamp !== undefined &&
    Number.isFinite(generatedAtTimestamp) &&
    generatedAtTimestamp <= freshnessCheckedAt;

  const ageInDays =
    generatedAtValid &&
    freshnessCheckedAt !== null &&
    generatedAtTimestamp !== undefined
      ? (freshnessCheckedAt - generatedAtTimestamp) /
        (1000 * 60 * 60 * 24)
      : null;

  const freshnessStatus =
    ageInDays === null
      ? "Unknown"
      : ageInDays <= STALE_AFTER_DAYS
        ? "Fresh"
        : "Stale";

  const freshnessColor =
    freshnessStatus === "Fresh"
      ? "text-emerald-300"
      : freshnessStatus === "Stale"
        ? "text-amber-300"
        : "text-slate-400";

  const formattedGeneratedAt = generatedAtValid
    ? generatedAtDate!.toLocaleString()
    : "Timestamp unavailable";

  const validatedCount = results.filter(
    (result) => result.quality_status === "validated"
  ).length;

  const topResults = [...results]
    .sort(
      (a, b) => a.priority_rank - b.priority_rank
    )
    .slice(0, 3);

  const selectedDimensionLabel =
    selectedDimension === "all"
      ? "All dimensions"
      : selectedDimension === "root_cause_category"
        ? "Root cause category"
        : selectedDimension === "machine"
          ? "Machine"
          : selectedDimension === "shift"
            ? "Shift"
            : selectedDimension;

  if (loading) {
    return (
      <main
        className="min-h-screen bg-slate-950 px-6 py-10 text-white"
        aria-busy="true"
        aria-live="polite"
      >
        <div className="mx-auto max-w-7xl">
          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-8">
            <div
              className="mb-4 h-5 w-64 animate-pulse rounded bg-slate-800"
              aria-hidden="true"
            />
            <div
              className="h-4 w-96 max-w-full animate-pulse rounded bg-slate-800"
              aria-hidden="true"
            />
            <p className="mt-5 text-sm text-slate-400">
              Loading approved downtime intelligence...
            </p>
          </div>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="min-h-screen bg-slate-950 px-6 py-10 text-white">
        <div className="mx-auto max-w-4xl">
          <div
            className="rounded-2xl border border-red-900 bg-red-950/40 p-8"
            role="alert"
            aria-live="assertive"
          >
            <h1 className="text-2xl font-semibold">
              Data Intelligence unavailable
            </h1>

            <p className="mt-3 text-sm leading-6 text-red-200">
              {error}
            </p>

            <p className="mt-3 text-xs text-slate-400">
              Diagnostic reference: {DIAGNOSTIC_REFERENCE}
            </p>

            <div className="mt-6 flex flex-wrap gap-3">
              <button
                type="button"
                onClick={() =>
                  setRetryCount((count) => count + 1)
                }
                className="rounded-lg bg-cyan-700 px-4 py-2 text-sm font-medium text-white hover:bg-cyan-600"
              >
                Retry loading
              </button>

              <Link
                href="/"
                className="inline-flex items-center rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-200 hover:bg-slate-800"
              >
                Return to Operational Dashboard
              </Link>
            </div>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-8 text-white">
      <div className="mx-auto max-w-7xl space-y-8">
        {/* Header */}
        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-xl">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <div className="mb-3 flex flex-wrap items-center gap-2">
                <span className="rounded-full border border-cyan-800 bg-cyan-950/50 px-3 py-1 text-xs font-medium text-cyan-300">
                  DATA INTELLIGENCE
                </span>

                <span className="rounded-full border border-slate-700 bg-slate-800 px-3 py-1 text-xs text-slate-300">
                  Track A - Comparative Intelligence
                </span>
              </div>

              <h1 className="text-3xl font-bold tracking-tight">
                Downtime Intelligence
              </h1>

              <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">
                Approved comparative intelligence showing which observed
                root-cause categories, machines, and shifts contribute the
                greatest downtime and failure-frequency burden.
              </p>
            </div>

            <nav aria-label="Main navigation">
              <Link
                href="/"
                className="inline-flex items-center justify-center rounded-lg border border-slate-700 bg-slate-800 px-4 py-2 text-sm font-medium text-slate-200 hover:bg-slate-700"
              >
                Operational Dashboard
              </Link>
            </nav>
          </div>

          <div className="mt-6 grid gap-3 md:grid-cols-3">
            <MetadataCard
              label="Data Version"
              value={summary?.data_version || "-"}
            />

            <MetadataCard
              label="Method Version"
              value={summary?.method_version || "-"}
            />

            <MetadataCard
              label="Validation"
              value={summary?.validation_result || "-"}
            />

            <MetadataCard
              label="Approved Track"
              value={summary?.approved_track || "-"}
            />

            <MetadataCard
              label="Data Freshness"
              value={freshnessStatus}
              valueClassName={freshnessColor}
            />

            <MetadataCard
              label="Generated At"
              value={formattedGeneratedAt}
            />
          </div>
        </section>

        {/* Freshness warning */}
        {freshnessStatus !== "Fresh" && (
          <section
            className="rounded-xl border border-amber-800 bg-amber-950/30 p-4"
            role="status"
          >
            <h2 className="text-sm font-semibold text-amber-200">
              Data freshness warning
            </h2>

            <p className="mt-2 text-sm leading-6 text-amber-100/80">
              {freshnessStatus === "Stale"
                ? `The approved intelligence output is older than ${STALE_AFTER_DAYS} days. Review its freshness before relying on this comparison.`
                : "The generation timestamp is missing or invalid. Data freshness could not be verified."}
            </p>
          </section>
        )}

        {/* KPI summary */}
        <section className="grid gap-4 md:grid-cols-4">
          <MetricCard
            label="Intelligence Results"
            value={results.length}
          />

          <MetricCard
            label="Validated Results"
            value={validatedCount}
          />

          <MetricCard
            label="Source Incidents"
            value={
              summary?.overall_metrics?.incident_count ?? "—"
            }
          />

          <MetricCard
            label="Data Quality"
            value={summary?.validation_result ?? "—"}
          />
        </section>

        {/* Key findings */}
        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <div className="mb-5">
            <h2 className="text-xl font-semibold">
              Key Comparative Findings
            </h2>

            <p className="mt-1 text-sm text-slate-400">
              Highest-priority validated intelligence from the approved
              analytical output.
            </p>
          </div>

          <div className="grid gap-4 lg:grid-cols-3">
            {topResults.map((result) => (
              <div
                key={result.result_id}
                className="rounded-xl border border-slate-800 bg-slate-950 p-5"
              >
                <div className="flex items-center justify-between gap-3">
                  <span className="text-xs font-medium uppercase tracking-wide text-cyan-400">
                    Priority #{result.priority_rank}
                  </span>

                  <span className="rounded-full border border-emerald-800 bg-emerald-950/40 px-2 py-1 text-xs text-emerald-300">
                    {result.quality_status}
                  </span>
                </div>

                <h3 className="mt-4 text-lg font-semibold">
                  {result.group_key}
                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-300">
                  {result.finding}
                </p>

                <div className="mt-4 rounded-lg bg-slate-900 p-3">
                  <p className="text-xs text-slate-300">
                    {result.metric_name}
                  </p>

                  <p className="mt-1 text-xl font-semibold text-cyan-300">
                    {result.result_value}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Results */}
        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <h2 className="text-xl font-semibold">
                Ranked Comparative Intelligence
              </h2>

              <p className="mt-1 text-sm text-slate-400">
                Results are served from the validated analytical output.
              </p>
            </div>

            <div>
              <label
                htmlFor="result-dimension"
                className="mb-2 block text-xs font-medium uppercase tracking-wide text-slate-300"
              >
                Compare by
              </label>

              <select
                id="result-dimension"
                value={selectedDimension}
                onChange={(event) =>
                  setSelectedDimension(event.target.value)
                }
                className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white outline-none"
              >
                <option value="all">All dimensions</option>
                <option value="root_cause_category">
                  Root cause category
                </option>
                <option value="machine">Machine</option>
                <option value="shift">Shift</option>
              </select>
            </div>
          </div>

          <div className="mt-6 overflow-x-auto">
            <table className="w-full min-w-[900px] border-collapse text-left">
              <thead>
                <tr className="border-b border-slate-800 text-xs uppercase tracking-wide text-slate-300">
                  <th className="px-4 py-3">Rank</th>
                  <th className="px-4 py-3">Type</th>
                  <th className="px-4 py-3">Group</th>
                  <th className="px-4 py-3">Metric</th>
                  <th className="px-4 py-3">Value</th>
                  <th className="px-4 py-3">Category</th>
                  <th className="px-4 py-3">Quality</th>
                </tr>
              </thead>

              <tbody>
                {filteredResults.map((result) => (
                  <tr
                    key={result.result_id}
                    className="border-b border-slate-800/70 text-sm"
                  >
                    <td className="px-4 py-4 font-semibold text-cyan-300">
                      #{result.priority_rank}
                    </td>

                    <td className="px-4 py-4 text-slate-300">
                      {result.result_type}
                    </td>

                    <td className="px-4 py-4 font-medium text-white">
                      {result.group_key}
                    </td>

                    <td className="px-4 py-4 text-slate-400">
                      {result.metric_name}
                    </td>

                    <td className="px-4 py-4 font-semibold text-white">
                      {result.result_value}
                    </td>

                    <td className="px-4 py-4 text-slate-400">
                      {result.result_category}
                    </td>

                    <td className="px-4 py-4">
                      <span
                        className={`rounded-full px-2 py-1 text-xs ${
                          result.quality_status === "validated"
                            ? "bg-emerald-950 text-emerald-300"
                            : result.quality_status === "conditional"
                              ? "bg-amber-950 text-amber-300"
                              : "bg-red-950 text-red-300"
                        }`}
                      >
                        {result.quality_status}
                      </span>
                    </td>
                  </tr>
                ))}

                {filteredResults.length === 0 && (
                  <tr>
                    <td
                      colSpan={7}
                      className="px-4 py-10 text-center text-sm text-slate-300"
                    >
                      <p>
                        No intelligence results match this selection.
                      </p>

                      <p className="mt-2 text-xs text-slate-400">
                        Active filter: {selectedDimensionLabel}
                      </p>

                      <button
                        type="button"
                        onClick={() => setSelectedDimension("all")}
                        className="mt-4 rounded-lg border border-slate-700 px-4 py-2 text-sm text-cyan-300 hover:bg-slate-800"
                      >
                        Clear filters
                      </button>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>

        {/* Approved Track A comparative analysis */}
        <TrackAComparison
          results={filteredResults}
          selectedDimension={selectedDimension}
        />

        {/* Supporting evidence */}
        <section>
          <div className="mb-4">
            <h2 className="text-xl font-semibold">
              Supporting Evidence
            </h2>

            <p className="mt-1 text-sm text-slate-400">
              Evidence and limitations attached to each analytical result.
            </p>
          </div>

          <div className="grid gap-4 lg:grid-cols-2">
            {filteredResults.map((result) => (
              <div
                key={`${result.result_id}-evidence`}
                className="rounded-2xl border border-slate-800 bg-slate-900 p-5"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="text-xs uppercase tracking-wide text-slate-300">
                      {result.result_type}
                    </p>

                    <h3 className="mt-1 font-semibold">
                      {result.group_key}
                    </h3>
                  </div>

                  <span className="text-sm font-semibold text-cyan-300">
                    #{result.priority_rank}
                  </span>
                </div>

                <div className="mt-4 space-y-2">
                  {result.evidence.map((item, index) => (
                    <div
                      key={`${item.factor}-${index}`}
                      className="flex flex-wrap items-center justify-between gap-2 rounded-lg bg-slate-950 p-3 text-sm"
                    >
                      <span className="text-slate-400">
                        {item.factor.replace(/_/g, " ")}
                      </span>

                      <span className="font-medium text-slate-200">
                        {item.value}
                      </span>

                      {item.contribution !== null && (
                        <span className="text-cyan-300">
                          Contribution: {item.contribution}
                        </span>
                      )}
                    </div>
                  ))}
                </div>

                <div className="mt-4 rounded-lg border border-slate-800 bg-slate-950 p-4">
                  <p className="text-xs font-medium uppercase tracking-wide text-slate-300">
                    Limitation
                  </p>

                  <p className="mt-2 text-sm leading-6 text-slate-400">
                    {result.limitation}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Methodology */}
        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
          <h2 className="text-xl font-semibold">
            Methodology
          </h2>

          <div className="mt-4 grid gap-4 md:grid-cols-3">
            <MethodCard
              title="Analytical Track"
              text="Track A - Comparative Intelligence"
            />

            <MethodCard
              title="Decision Support"
              text="Deterministic review and prioritisation based on comparative downtime and failure-frequency results."
            />

            <MethodCard
              title="Validation"
              text="Approved analytical output with validated data and method versions."
            />
          </div>
        </section>

        {/* Grounded Data Assistant - Phase 3 Post #5 */}
        <AssistantPanel />

        {/* Limitations */}
        <section className="rounded-2xl border border-amber-900/60 bg-amber-950/20 p-6">
          <h2 className="text-xl font-semibold text-amber-200">
            Limitations and Responsible Use
          </h2>

          <div className="mt-4 space-y-3 text-sm leading-6 text-amber-100/80">
            <p>
              All source incidents are synthetic and are intended for
              demonstration purposes.
            </p>

            <p>
              The results are descriptive comparative intelligence and
              should not be interpreted as causal relationships.
            </p>

            <p>
              The results are not predictive evidence and must not be
              presented as actual industrial performance.
            </p>

            <p>
              Small group sizes may affect ranking stability.
            </p>
          </div>
        </section>

        {/* Footer */}
        <footer className="border-t border-slate-800 pt-5 text-xs text-slate-300">
          <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
            <span>
              Downtime Root Cause Explorer | Data Intelligence
            </span>

            <span>
              Data {summary?.data_version || "-"} | Method{" "}
              {summary?.method_version || "-"}
            </span>
          </div>
        </footer>
      </div>
    </main>
  );
}

function MetadataCard({
  label,
  value,
  valueClassName = "text-slate-200",
}: {
  label: string;
  value: string;
  valueClassName?: string;
}) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
      <p className="text-xs uppercase tracking-wide text-slate-300">
        {label}
      </p>

      <p className={`mt-2 text-sm font-semibold ${valueClassName}`}>
        {value}
      </p>
    </div>
  );
}

function MetricCard({
  label,
  value,
}: {
  label: string;
  value: string | number;
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
      <p className="text-xs uppercase tracking-wide text-slate-300">
        {label}
      </p>

      <p className="mt-2 text-3xl font-bold text-white">
        {value}
      </p>
    </div>
  );
}

function MethodCard({
  title,
  text,
}: {
  title: string;
  text: string;
}) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
      <h3 className="font-semibold text-slate-200">
        {title}
      </h3>

      <p className="mt-2 text-sm leading-6 text-slate-400">
        {text}
      </p>
    </div>
  );
}
