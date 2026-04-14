export default function StepProgressBar({ step, total, labels }: { step: number; total: number; labels: string[] }) {
  const pct = Math.round((Math.max(1, Math.min(step, total)) / total) * 100);
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between text-xs opacity-70">
        <div>
          Step {step}/{total}
        </div>
        <div>{pct}%</div>
      </div>
      <progress className="progress progress-primary w-full" value={pct} max={100} />
      <div className="flex flex-wrap gap-2">
        {labels.map((l, i) => (
          <span key={l} className={`badge ${i + 1 === step ? "badge-primary" : "badge-ghost"}`}>
            {l}
          </span>
        ))}
      </div>
    </div>
  );
}

