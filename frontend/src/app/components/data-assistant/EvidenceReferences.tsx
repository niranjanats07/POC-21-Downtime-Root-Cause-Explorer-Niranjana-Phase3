type Evidence = {
  result_id: string; result_type?: string; group_key?: string;
  result_category?: string; finding?: string; metric_name?: string;
  result_value?: number; result_unit?: string; priority_rank?: number;
  data_version?: string; method_version?: string;
  evidence?: { factor: string; value: string | number; contribution: number | null }[];
};

export default function EvidenceReferences({ items }: { items: Evidence[] }) {
  if (!items.length) return <p className="text-sm text-slate-400">No evidence references were returned for this response.</p>;
  return (
    <div className="space-y-3">
      <h3 className="text-sm font-semibold text-slate-200">Evidence references ({items.length})</h3>
      {items.slice(0, 10).map((item) => (
        <article key={item.result_id} className="rounded-lg border border-slate-800 bg-slate-950 p-4">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <span className="font-mono text-xs text-cyan-300">{item.result_id}</span>
            <span className="text-xs text-slate-400">{item.result_category || "Approved result"} · Rank {item.priority_rank ?? "—"}</span>
          </div>
          <p className="mt-2 text-sm font-medium text-slate-200">{item.group_key || item.result_type}</p>
          {item.finding && <p className="mt-1 text-sm leading-6 text-slate-400">{item.finding}</p>}
          {item.metric_name && <p className="mt-2 text-xs text-slate-400">{item.metric_name}: {item.result_value} {item.result_unit}</p>}
          {item.evidence?.length ? (
            <dl className="mt-3 grid gap-2 sm:grid-cols-2">
              {item.evidence.slice(0, 5).map((factor, index) => (
                <div key={`${factor.factor}-${index}`} className="rounded bg-slate-900 p-2">
                  <dt className="text-xs text-slate-400">{factor.factor.replace(/_/g, " ")}</dt>
                  <dd className="mt-1 text-sm text-slate-200">{factor.value}</dd>
                </div>
              ))}
            </dl>
          ) : null}
        </article>
      ))}
    </div>
  );
}
