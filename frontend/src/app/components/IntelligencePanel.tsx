
"use client";

type Incident = {
  incident_id: string;
  machine_id: string;
  incident_date: string;
  shift: string;
  root_cause: string;
  sub_cause: string;
  downtime_minutes: number;
  failure_frequency: number;
  severity: string;
  status: string;
  description: string;
};

type Props = {
  incident: Incident | null;
  onClose: () => void;
};

export default function IntelligencePanel({
  incident,
  onClose,
}: Props) {
  if (!incident) return null;

  const recommendations: Record<string, string> = {
    Mechanical:
      "Review mechanical wear, lubrication, bearings and preventive maintenance intervals.",
    Electrical:
      "Inspect electrical connections, motors, sensors and power supply stability.",
    Operational:
      "Review machine operating procedures, material flow and operator training.",
    Maintenance:
      "Review preventive maintenance scheduling and overdue maintenance tasks.",
  };

  const recommendation =
    recommendations[incident.root_cause] ??
    "Conduct a detailed engineering investigation to identify the underlying failure mechanism.";

  const priority =
    incident.severity.toLowerCase() === "high"
      ? "High"
      : incident.severity.toLowerCase() === "medium"
        ? "Medium"
        : "Low";

  const details = [
    ["Machine", incident.machine_id],
    ["Date", incident.incident_date],
    ["Shift", incident.shift],
    ["Failure frequency", incident.failure_frequency],
    ["Root cause", incident.root_cause],
    ["Sub-cause", incident.sub_cause],
    ["Severity", incident.severity],
    ["Status", incident.status],
  ] as const;

  return (
    <div className="fixed inset-0 z-50">
      <button
        type="button"
        aria-label="Close investigation panel"
        onClick={onClose}
        className="absolute inset-0 bg-black/75 backdrop-blur-sm"
      />

      <aside
        role="dialog"
        aria-modal="true"
        aria-labelledby="investigation-title"
        className="custom-scrollbar absolute right-0 top-0 flex h-full w-full max-w-xl flex-col overflow-y-auto border-l border-slate-700 bg-[#0c1722] p-5 text-white shadow-2xl sm:p-8"
      >
        <header className="mb-7 flex items-start justify-between gap-4">
          <div className="min-w-0">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-teal-400">
              Operations Investigation
            </p>

            <h2
              id="investigation-title"
              className="mt-2 text-2xl font-bold tracking-tight"
            >
              Incident Investigation
            </h2>

            <p className="mt-2 break-all text-sm text-slate-400">
              Evidence record: {incident.incident_id}
            </p>
          </div>

          <button
            type="button"
            onClick={onClose}
            aria-label="Close investigation"
            className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg border border-slate-600 text-xl text-slate-300 transition hover:border-teal-400 hover:bg-slate-800 hover:text-white focus:outline-none focus:ring-2 focus:ring-teal-400"
          >
            ×
          </button>
        </header>

        <section className="mb-6 rounded-xl border border-teal-500/30 bg-teal-500/5 p-5">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                Recorded downtime
              </p>

              <p className="mt-2 text-4xl font-bold tabular-nums text-teal-300">
                {incident.downtime_minutes}
                <span className="ml-2 text-sm font-medium text-slate-400">
                  minutes
                </span>
              </p>
            </div>

            <span className="rounded-full border border-slate-600 bg-slate-900 px-3 py-1 text-xs font-semibold text-slate-300">
              {incident.severity} severity
            </span>
          </div>

          <div className="mt-4 grid grid-cols-2 gap-3 border-t border-slate-700/70 pt-4">
            <div>
              <p className="text-xs text-slate-400">Machine</p>
              <p className="mt-1 break-words font-semibold text-white">
                {incident.machine_id}
              </p>
            </div>

            <div>
              <p className="text-xs text-slate-400">Root cause</p>
              <p className="mt-1 break-words font-semibold text-white">
                {incident.root_cause}
              </p>
            </div>
          </div>
        </section>

        <section className="mb-6">
          <div className="mb-4">
            <h3 className="text-lg font-semibold">
              Recorded incident details
            </h3>
            <p className="mt-1 text-xs text-slate-400">
              Values shown are from the selected incident record.
            </p>
          </div>

          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            {details.map(([label, value]) => (
              <div
                key={label}
                className="min-w-0 rounded-lg border border-slate-700 bg-slate-900/80 p-4"
              >
                <p className="text-xs text-slate-400">{label}</p>
                <p className="mt-2 break-words text-sm font-semibold text-slate-100">
                  {value}
                </p>
              </div>
            ))}
          </div>
        </section>

        <section className="mb-6 rounded-xl border border-slate-700 bg-slate-900/70 p-5">
          <h3 className="font-semibold text-white">
            Recorded failure description
          </h3>

          <p className="mt-3 whitespace-pre-wrap break-words text-sm leading-7 text-slate-300">
            {incident.description || "No description is available for this incident."}
          </p>
        </section>

        <section className="mb-6 rounded-xl border border-amber-500/30 bg-amber-500/5 p-5">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h3 className="font-semibold text-white">
              Investigation priority
            </h3>

            <span className="rounded-full border border-amber-500/30 bg-amber-500/10 px-3 py-1 text-xs font-semibold text-amber-300">
              {priority}
            </span>
          </div>

          <p className="mt-3 text-sm leading-7 text-slate-300">
            {incident.severity} severity is recorded for this
            incident. Review its downtime impact, recurrence
            and operational context before prioritizing action.
          </p>
        </section>

        <section className="mb-6 rounded-xl border border-teal-500/30 bg-teal-500/5 p-5">
          <h3 className="font-semibold text-teal-300">
            Management investigation recommendation
          </h3>

          <p className="mt-3 text-sm leading-7 text-slate-200">
            {recommendation}
          </p>

          <p className="mt-4 border-t border-teal-500/20 pt-4 text-xs leading-6 text-slate-400">
            This is a general decision-support suggestion based
            on the recorded root-cause category, not a verified
            diagnosis. Validate findings against maintenance
            records and engineering evidence.
          </p>
        </section>

        <footer className="mt-auto border-t border-slate-700 pt-5">
          <button
            type="button"
            onClick={onClose}
            className="w-full rounded-lg bg-teal-500 px-4 py-3 font-semibold text-slate-950 transition hover:bg-teal-400 focus:outline-none focus:ring-2 focus:ring-teal-300 focus:ring-offset-2 focus:ring-offset-[#0c1722]"
          >
            Close investigation
          </button>
        </footer>
      </aside>
    </div>
  );
}
