export default function QuestionInput({ value, onChange, onSubmit, disabled }: {
  value: string; onChange: (value: string) => void; onSubmit: () => void; disabled: boolean;
}) {
  return (
    <form onSubmit={(event) => { event.preventDefault(); onSubmit(); }} className="space-y-3">
      <label htmlFor="assistant-question" className="block text-sm font-medium text-slate-200">
        Ask about the approved Track A results
      </label>
      <textarea id="assistant-question" value={value} maxLength={500}
        onChange={(event) => onChange(event.target.value)}
        placeholder="For example: Which machine ranks highest by downtime?"
        rows={3} disabled={disabled}
        className="w-full rounded-xl border border-slate-700 bg-slate-950 p-3 text-sm text-white placeholder:text-slate-500 focus:border-cyan-600 focus:outline-none disabled:opacity-60" />
      <div className="flex items-center justify-between gap-3">
        <span className="text-xs text-slate-400">{value.length}/500 characters</span>
        <button type="submit" disabled={disabled || !value.trim()}
          className="rounded-lg bg-cyan-700 px-5 py-2 text-sm font-semibold text-white hover:bg-cyan-600 disabled:cursor-not-allowed disabled:opacity-50">
          Ask assistant
        </button>
      </div>
    </form>
  );
}
