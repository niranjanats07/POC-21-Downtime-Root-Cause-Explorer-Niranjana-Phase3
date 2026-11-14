type Props = { status: "idle" | "loading" | "success" | "error"; message?: string };

export default function AssistantStatus({ status, message }: Props) {
  if (status === "idle") return null;
  const styles = {
    loading: "border-cyan-800 bg-cyan-950/30 text-cyan-200",
    success: "border-emerald-800 bg-emerald-950/30 text-emerald-200",
    error: "border-rose-800 bg-rose-950/30 text-rose-200",
    idle: "border-slate-700 bg-slate-900 text-slate-300",
  };
  return (
    <p role="status" aria-live="polite" className={`rounded-lg border p-3 text-sm ${styles[status]}`}>
      {message || (status === "loading" ? "Checking approved intelligence…" : status === "success" ? "Response received." : "The request could not be completed.")}
    </p>
  );
}
