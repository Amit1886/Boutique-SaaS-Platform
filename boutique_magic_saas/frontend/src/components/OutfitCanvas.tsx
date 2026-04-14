import { useEffect, useMemo, useRef, useState } from "react";
import type { Accessory, Blouse, Saree } from "../store/useCatalogStore";

type Layer = {
  key: string;
  url: string;
  x: number;
  y: number;
  scale: number;
  z: number;
  blend: "normal" | "multiply" | "screen";
};

function clamp(v: number, a: number, b: number) {
  return Math.max(a, Math.min(b, v));
}

export default function OutfitCanvas({
  saree,
  blouse,
  accessories
}: {
  saree: Saree | null;
  blouse: Blouse | null;
  accessories: Accessory[];
}) {
  const base = "https://picsum.photos/seed/magic_user/900/1200";

  const layers = useMemo<Layer[]>(() => {
    const out: Layer[] = [];
    if (saree?.layer_body_png) out.push({ key: "saree_body", url: saree.layer_body_png, x: 0, y: 0, scale: 1, z: 3, blend: "multiply" });
    if (saree?.layer_border_png) out.push({ key: "saree_border", url: saree.layer_border_png, x: 0, y: 0, scale: 1, z: 5, blend: "screen" });
    if (saree?.layer_pallu_png) out.push({ key: "saree_pallu", url: saree.layer_pallu_png, x: 8, y: -6, scale: 1, z: 4, blend: "multiply" });
    if (blouse?.template_png) out.push({ key: "blouse", url: blouse.template_png, x: 0, y: 10, scale: 0.95, z: 6, blend: "screen" });
    accessories.forEach((a, i) => {
      if (a.image_png) out.push({ key: `acc_${a.id}`, url: a.image_png, x: -10 + i * 10, y: -12 + i * 2, scale: 0.55, z: 7 + i, blend: "screen" });
    });
    return out;
  }, [saree, blouse, accessories]);

  const [state, setState] = useState<Record<string, Layer>>({});
  const active = useRef<string | null>(null);
  const start = useRef<{ x: number; y: number; lx: number; ly: number } | null>(null);

  useEffect(() => {
    const next: Record<string, Layer> = {};
    for (const l of layers) next[l.key] = state[l.key] || l;
    setState(next);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [layers.map((l) => l.key).join("|")]);

  function onDown(key: string, e: React.PointerEvent) {
    active.current = key;
    const l = state[key];
    start.current = { x: e.clientX, y: e.clientY, lx: l.x, ly: l.y };
    (e.target as any).setPointerCapture?.(e.pointerId);
  }

  function onMove(e: React.PointerEvent) {
    if (!active.current || !start.current) return;
    const key = active.current;
    const s = start.current;
    const dx = e.clientX - s.x;
    const dy = e.clientY - s.y;
    setState((prev) => ({
      ...prev,
      [key]: { ...prev[key], x: clamp(s.lx + dx / 8, -40, 40), y: clamp(s.ly + dy / 8, -40, 40) }
    }));
  }

  function onUp() {
    active.current = null;
    start.current = null;
  }

  return (
    <div className="rounded-2xl border border-base-300 bg-base-100 overflow-hidden">
      <div className="p-3">
        <div className="font-bold">Drag & Drop Outfit Builder</div>
        <div className="text-xs opacity-70">Drag layers to compose. Blend modes simulate fabric realism.</div>
      </div>
      <div className="relative aspect-[3/4] bg-base-200 overflow-hidden" onPointerMove={onMove} onPointerUp={onUp} onPointerCancel={onUp}>
        <img src={base} className="absolute inset-0 w-full h-full object-cover" />
        {Object.values(state)
          .sort((a, b) => a.z - b.z)
          .map((l) => (
            <img
              key={l.key}
              src={`${import.meta.env.VITE_UPLOAD_BASE_URL || ""}${l.url}`}
              className="absolute inset-0 w-full h-full object-contain aura"
              style={{
                mixBlendMode: l.blend as any,
                transform: `translate(${l.x}%, ${l.y}%) scale(${l.scale})`,
                filter: "drop-shadow(0 10px 18px rgba(0,0,0,0.18))",
                touchAction: "none"
              }}
              onPointerDown={(e) => onDown(l.key, e)}
            />
          ))}
      </div>
    </div>
  );
}

