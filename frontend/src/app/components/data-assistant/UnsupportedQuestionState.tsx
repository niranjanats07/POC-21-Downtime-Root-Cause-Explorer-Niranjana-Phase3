export default function UnsupportedQuestionState({ status, answer }: {
  status: "unsupported" | "unsafe" | "unavailable" | "error"; answer: string;
}) {
  const title = status === "unsafe" ? "Request not permitted" :
    status === "unavailable" ? "Assistant unavailable" :
    status === "error" ? "Unable to answer" : "Question outside supported scope";
  return (
    <div role="status" className="rounded-xl border border-amber-800 bg-amber-950/20 p-4">
      <h3 className="font-semibold text-amber-200">{title}</h3>
      <p className="mt-2 text-sm leading-6 text-amber-100/80">{answer}</p>
      <p className="mt-2 text-xs text-amber-200/70">Ask about approved Track A summaries, rankings, comparisons, evidence, validation or limitations.</p>
    </div>
  );
}
