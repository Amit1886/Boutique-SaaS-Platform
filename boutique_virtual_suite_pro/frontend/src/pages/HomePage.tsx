import React, { useEffect } from "react";
import { useMoodStore } from "../stores/moodStore";
import { useProductStore } from "../stores/productStore";
import ProductCard from "../components/ProductCard";
import { useAuthStore } from "../stores/authStore";
import { apiFetch } from "../api/client";
import { cacheGet, cacheSet } from "../lib/cache";

export default function HomePage() {
  const banner = useMoodStore((s) => s.banner);
  const themeColor = useMoodStore((s) => s.themeColor);
  const loadMoods = useMoodStore((s) => s.loadMoods);
  const loadAll = useProductStore((s) => s.loadAll);
  const products = useProductStore((s) => s.products);
  const loading = useProductStore((s) => s.loading);
  const error = useProductStore((s) => s.error);
  const token = useAuthStore((s) => s.token);
  const activeMoodKey = useMoodStore((s) => s.activeKey);
  const moods = useMoodStore((s) => s.moods);
  const [personal, setPersonal] = React.useState<any[]>(cacheGet<any[]>("bvp.feed.personal") || []);
  const [moodPicks, setMoodPicks] = React.useState<any[]>(cacheGet<any[]>("bvp.feed.mood") || []);

  useEffect(() => {
    loadMoods().catch(() => {});
    loadAll().catch(() => {});
  }, [loadMoods, loadAll]);

  useEffect(() => {
    if (!token) return;
    apiFetch<{ ok: true; products: any[] }>("/feed/personalized", { method: "GET" })
      .then((r) => {
        cacheSet("bvp.feed.personal", r.products, 1000 * 60 * 5);
        setPersonal(r.products || []);
      })
      .catch(() => {});
  }, [token]);

  const moodName = (moods.find((m) => m.key === activeMoodKey)?.name_en || "").trim();

  useEffect(() => {
    if (!moodName) return;
    apiFetch<{ ok: true; products: any[] }>(`/products/by-mood?mood=${encodeURIComponent(moodName)}`, { method: "GET" })
      .then((r) => {
        cacheSet("bvp.feed.mood", r.products || [], 1000 * 60 * 5);
        setMoodPicks(r.products || []);
      })
      .catch(() => {});
  }, [moodName]);

  return (
    <div className="space-y-6 fade-in">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-sm opacity-70">Moodboard banner</div>
        <div className="mt-1 text-2xl font-extrabold" style={{ color: themeColor || "var(--bvp-primary)" }}>
          {banner || "Boutique Virtual Suite Pro"}
        </div>
        <div className="mt-2 opacity-70 text-sm">Trylist + designer flow + live color swap (no reload).</div>
      </div>

      {token && personal.length ? (
        <>
          <div className="flex items-center justify-between">
            <div className="text-lg font-bold">For you</div>
            <div className="text-xs opacity-60">Personalized</div>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {personal.slice(0, 12).map((p: any) => (
              <ProductCard key={p.id} p={p} />
            ))}
          </div>
        </>
      ) : null}

      {moodPicks.length ? (
        <>
          <div className="flex items-center justify-between">
            <div className="text-lg font-bold">Mood picks</div>
            <div className="text-xs opacity-60">{moodName}</div>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {moodPicks.slice(0, 12).map((p) => (
              <ProductCard key={p.id} p={p} />
            ))}
          </div>
        </>
      ) : null}

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
