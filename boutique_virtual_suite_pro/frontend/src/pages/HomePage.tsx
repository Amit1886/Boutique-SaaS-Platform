import { useEffect } from "react";
import { useMoodStore } from "../stores/moodStore";
import { useProductStore } from "../stores/productStore";
import ProductCard from "../components/ProductCard";

export default function HomePage() {
  const banner = useMoodStore((s) => s.banner);
  const themeColor = useMoodStore((s) => s.themeColor);
  const loadMoods = useMoodStore((s) => s.loadMoods);
  const loadAll = useProductStore((s) => s.loadAll);
  const products = useProductStore((s) => s.products);
  const loading = useProductStore((s) => s.loading);
  const error = useProductStore((s) => s.error);

  useEffect(() => {
    loadMoods().catch(() => {});
    loadAll().catch(() => {});
  }, [loadMoods, loadAll]);

  return (
    <div className="space-y-6 fade-in">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-sm opacity-70">Moodboard banner</div>
        <div className="mt-1 text-2xl font-extrabold" style={{ color: themeColor || "var(--bvp-primary)" }}>
          {banner || "Boutique Virtual Suite Pro"}
        </div>
        <div className="mt-2 opacity-70 text-sm">Trylist + designer flow + live color swap (no reload).</div>
      </div>

      <div className="flex items-center justify-between">
        <div className="text-lg font-bold">Trending picks</div>
        <div className="text-xs opacity-60">Cached offline</div>
      </div>

      {error ? <div className="alert alert-error">{error}</div> : null}
      {loading && !products.length ? <div className="skeleton h-40 w-full" /> : null}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {products.slice(0, 24).map((p) => (
          <ProductCard key={p.id} p={p} />
        ))}
      </div>
    </div>
  );
}

