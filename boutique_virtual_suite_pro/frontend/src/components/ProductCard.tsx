import { useRef } from "react";
import { useTrylistStore } from "../stores/trylistStore";
import type { Product } from "../stores/productStore";
import LiveColorSwapper from "./color/LiveColorSwapper";

export default function ProductCard({ p }: { p: Product }) {
  const add = useTrylistStore((s) => s.add);
  const imgRef = useRef<HTMLImageElement | null>(null);

  return (
    <div className="rounded-2xl border border-base-300 bg-base-100 overflow-hidden">
      <div className="relative">
        <img ref={imgRef} src={p.image_url} className="w-full h-56 object-cover" />
        <div className="absolute top-2 left-2 badge badge-primary">{p.mood_tag || "Mood"}</div>
      </div>
      <div className="p-4 space-y-2">
        <div className="font-semibold">{p.name}</div>
        <div className="text-xs opacity-70">
          {p.category} · {p.fabric} · {p.style_tag}
        </div>
        <LiveColorSwapper imgRef={imgRef} />
        <div className="flex items-center justify-between pt-2">
          <div className="font-bold">₹{p.price}</div>
          <button className="btn btn-primary btn-sm" onClick={() => add(p.id)}>
            Add to Trylist
          </button>
        </div>
      </div>
    </div>
  );
}
