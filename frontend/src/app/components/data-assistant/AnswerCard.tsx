export default function AnswerCard({ answer, intent }: { answer: string; intent: string }) {
  return (
    <section className="rounded-xl border border-cyan-900/70 bg-cyan-950/20 p-5">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h3 className="font-semibold text-cyan-100">Grounded answer</h3>
        <span className="rounded-full border border-cyan-800 px-2 py-1 text-xs text-cyan-200">{intent.replace(/_/g, " ")}</span>
      </div>
      <p className="mt-3 whitespace-pre-wrap text-sm leading-7 text-slate-100">{answer}</p>
    </section>
  );
}
