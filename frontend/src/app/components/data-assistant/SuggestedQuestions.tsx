const QUESTIONS = [
  "Give me an overall summary.",
  "Which root-cause category ranks highest by downtime?",
  "Which machine ranks highest by downtime?",
  "Which shift ranks highest by observed downtime?",
  "Compare machines by observed downtime.",
  "Compare shifts.",
  "What are the limitations?",
  "Did analytical validation pass?",
];

export default function SuggestedQuestions({ onSelect, disabled }: {
  onSelect: (question: string) => void; disabled: boolean;
}) {
  return (
    <div>
      <h3 className="text-sm font-medium text-slate-300">Suggested questions</h3>
      <div className="mt-3 flex flex-wrap gap-2">
        {QUESTIONS.map((question) => (
          <button key={question} type="button" disabled={disabled}
            onClick={() => onSelect(question)}
            className="rounded-full border border-slate-700 bg-slate-950 px-3 py-2 text-left text-xs text-slate-300 hover:border-cyan-700 hover:text-cyan-200 disabled:opacity-50">
            {question}
          </button>
        ))}
      </div>
    </div>
  );
}
