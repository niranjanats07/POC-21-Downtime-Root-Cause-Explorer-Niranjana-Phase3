export default function LimitationNotice({ text }: { text: string }) {
  if (!text) return null;
  return (
    <aside className="rounded-lg border border-amber-800/70 bg-amber-950/20 p-4">
      <h3 className="text-sm font-semibold text-amber-200">Interpretation limitation</h3>
      <p className="mt-2 text-sm leading-6 text-amber-100/80">{text}</p>
    </aside>
  );
}
