import { useMemo, useState } from "react";

export default function ImageCompareSlider({ beforeUrl, afterUrl }: { beforeUrl: string; afterUrl: string }) {
  const [v, setV] = useState(50);
  const clip = useMemo(() => ({ clipPath: `inset(0 ${100 - v}% 0 0)` }), [v]);

  return (
    <div className="rounded-2xl border border-base-300 bg-base-100 overflow-hidden">
      <div className="relative aspect-[4/5] bg-base-200">
        <img src={beforeUrl} className="absolute inset-0 w-full h-full object-cover" loading="lazy" />
        <img src={afterUrl} className="absolute inset-0 w-full h-full object-cover" style={clip} loading="lazy" />
        <div className="absolute inset-x-0 bottom-3 px-3">
          <input className="range range-primary" type="range" min={0} max={100} value={v} onChange={(e) => setV(Number(e.target.value))} />
        </div>
        <div className="absolute top-3 left-3 badge badge-ghost">Before</div>
        <div className="absolute top-3 right-3 badge badge-primary">After</div>
      </div>
    </div>
  );
}

