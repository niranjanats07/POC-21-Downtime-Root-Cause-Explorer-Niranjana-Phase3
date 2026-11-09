type IntelligenceResult = {
  result_id: string;
  entity_id?: string | null;
  group_key: string;
  result_value: number;
  result_category: string;
  priority_rank: number;
  finding: string;
  evidence: {
    factor: string;
    value: string | number;
    contribution: number | null;
  }[];
  limitation: string;
};

type Props = {
  results: IntelligenceResult[];
  selectedDimension: string;
};

const DIMENSIONS = [
  { key: "root_cause_category", label: "Root-cause categories" },
  { key: "machine", label: "Machines" },
  { key: "shift", label: "Shifts" },
] as const;

const MINIMUM_GROUP_SIZE = 3;

function getIncidentCount(result: IntelligenceResult): number | null {
  const item = result.evidence.find(
    (entry) => entry.factor === "incident_count"
  );

  return typeof item?.value === "number" ? item.value : null;
}

function formatMinutes(value: number): string {
  return `${value.toLocaleString(undefined, {
    maximumFractionDigits: 1,
  })} min`;
}

export default function TrackAComparison({
  results,
  selectedDimension,
}: Props) {
  const comparativeResults = results.filter(
    (result) =>
      typeof result.result_value === "number" &&
      Number.isFinite(result.result_value) &&
      DIMENSIONS.some((dimension) => dimension.key === result.result_category)
  );

  const visibleDimensions =
    selectedDimension === "all"
      ? DIMENSIONS
      : DIMENSIONS.filter((dimension) => dimension.key === selectedDimension);

  return (
    <section
      aria-labelledby="track-a-comparison-heading"
      className="space-y-6"
    >
      <div>
        <h2
          id="track-a-comparison-heading"
          className="text-xl font-semibold text-white"
        >
          Track A comparative analysis
        </h2>
        <p className="mt-1 text-sm text-slate-300">
          Approved total-downtime measurements compared across root-cause
          categories, machines and shifts. The selected dimension filter
          applies to these comparisons.
        </p>
      </div>

      {visibleDimensions.map((dimension) => {
        const dimensionResults = comparativeResults
          .filter((result) => result.result_category === dimension.key)
          .sort((a, b) => a.priority_rank - b.priority_rank);

        const maximumDowntime = Math.max(
          1,
          ...dimensionResults.map((result) => result.result_value)
        );

        return (
          <section
            key={dimension.key}
            aria-labelledby={`comparison-${dimension.key}`}
            className="rounded-xl border border-slate-700 bg-slate-900/60 p-5"
          >
            <h3
              id={`comparison-${dimension.key}`}
              className="text-lg font-medium text-white"
            >
              {dimension.label}
            </h3>

            {dimensionResults.length === 0 ? (
              <p className="mt-3 text-sm text-slate-300">
                No approved comparison results are available for this dimension.
              </p>
            ) : (
              <div className="mt-5 space-y-5">
                {dimensionResults.map((result) => {
                  const incidentCount = getIncidentCount(result);
                  const meetsMinimum =
                    incidentCount !== null &&
                    incidentCount >= MINIMUM_GROUP_SIZE;
                  const label = result.entity_id || result.group_key;
                  const barWidth = Math.max(
                    2,
                    (result.result_value / maximumDowntime) * 100
                  );

                  return (
                    <article key={result.result_id} className="space-y-2">
                      <div className="flex flex-wrap items-center justify-between gap-2">
                        <div>
                          <p className="font-medium text-slate-100">
                            {label}
                          </p>
                          <p className="text-xs text-slate-300">
                            Rank #{result.priority_rank}
                          </p>
                        </div>

                        <p className="text-sm font-semibold tabular-nums text-slate-100">
                          {formatMinutes(result.result_value)}
                        </p>
                      </div>

                      <div
                        className="h-3 overflow-hidden rounded-full bg-slate-700"
                        role="img"
                        aria-label={`${label}: ${formatMinutes(result.result_value)} total downtime`}
                      >
                        <div
                          className="h-full rounded-full bg-sky-400"
                          style={{ width: `${barWidth}%` }}
                        />
                      </div>

                      <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
                        <span className="text-slate-300">
                          {incidentCount === null
                            ? "Incident count unavailable"
                            : `${incidentCount} incidents`}
                        </span>

                        <span
                          className={
                            incidentCount === null || !meetsMinimum
                              ? "text-amber-300"
                              : "text-emerald-300"
                          }
                        >
                          {incidentCount === null
                            ? "Group size not verified"
                            : meetsMinimum
                              ? "Meets minimum group size"
                              : "Below minimum — interpret with caution"}
                        </span>
                      </div>

                      <p className="text-sm leading-6 text-slate-300">
                        {result.finding}
                      </p>

                      {result.limitation && (
                        <p className="text-xs text-amber-200">
                          Limitation: {result.limitation}
                        </p>
                      )}
                    </article>
                  );
                })}
              </div>
            )}
          </section>
        );
      })}

      <section
        aria-labelledby="track-a-contribution-heading"
        className="rounded-xl border border-slate-700 bg-slate-900/60 p-5"
      >
        <h3
          id="track-a-contribution-heading"
          className="font-semibold text-slate-100"
        >
          Contribution measurement boundary
        </h3>
        <p className="mt-2 text-sm leading-6 text-slate-300">
          The approved results provide group-level downtime, incident-count
          and failure-frequency measurements. The output contract does not
          define a percentage contribution formula. No percentage shares or
          additional contribution metrics are calculated here. The approved
          evidence measurements remain available in the Supporting Evidence
          section.
        </p>
      </section>

      <section
        aria-labelledby="performance-gap-heading"
        className="rounded-xl border border-amber-700/60 bg-amber-950/20 p-5"
      >
        <h3
          id="performance-gap-heading"
          className="font-semibold text-amber-100"
        >
          Performance-gap analysis
        </h3>
        <p className="mt-2 text-sm text-slate-200">
          No independently approved performance-gap metric is supplied in the
          Track A output contract. This page does not calculate or infer one.
          Use the approved downtime and failure-frequency comparisons for
          investigation prioritisation.
        </p>
      </section>
    </section>
  );
}
