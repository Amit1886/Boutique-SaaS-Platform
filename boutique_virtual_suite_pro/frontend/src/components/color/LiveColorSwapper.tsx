import { useEffect, useId, useState } from "react";

const swatches = [
  { name: "Rose", hue: 0, sat: 1.1 },
  { name: "Indigo", hue: 220, sat: 1.2 },
  { name: "Emerald", hue: 120, sat: 1.2 },
  { name: "Amber", hue: 45, sat: 1.15 },
  { name: "Slate", hue: 200, sat: 0.9 }
];

export default function LiveColorSwapper({ imgRef }: { imgRef: { current: HTMLImageElement | null } }) {
  const [active, setActive] = useState(swatches[0]);
  const id = useId();

  useEffect(() => {
    const imageEl = imgRef.current;
    if (!imageEl) return;
    imageEl.style.filter = `hue-rotate(${active.hue}deg) saturate(${active.sat})`;
    return () => {
      imageEl.style.filter = "";
    };
  }, [active, imgRef]);

  return (
    <div className="flex gap-2 items-center">
      {swatches.map((s) => (
        <button
          key={`${id}-${s.name}`}
          className={`w-6 h-6 rounded-full border ${s.name === active.name ? "border-primary" : "border-base-300"}`}
          style={{ background: `hsl(${s.hue} 80% 55%)` }}
          title={s.name}
          onClick={() => setActive(s)}
        />
      ))}
      <div className="text-xs opacity-60">{active.name}</div>
    </div>
  );
}
