import { useEffect, useMemo, useState } from "react";
import { useProductStore } from "../stores/productStore";
import ProductCard from "../components/ProductCard";

export default function ProductListingPage() {
  const loadAll = useProductStore((s) => s.loadAll);
  const products = useProductStore((s) => s.products);
  const loading = useProductStore((s) => s.loading);
  const [q, setQ] = useState("");
  const [category, setCategory] = useState<string>("all");
  const [maxPrice, setMaxPrice] = useState<number>(999999);

  useEffect(() => {
    loadAll().catch(() => {});
  }, [loadAll]);

  const filtered = useMemo(() => {
    const qq = q.trim().toLowerCase();
    return products
      .filter((p) => (category === "all" ? true : p.category === category))
      .filter((p) => (p.price || 0) <= maxPrice)
      .filter((p) => (!qq ? true : `${p.name} ${p.fabric} ${p.style_tag} ${p.mood_tag}`.toLowerCase().includes(qq)));
  }, [products, q, category, maxPrice]);

  return (
    <div className="space-y-5">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-2xl font-extrabold">Products</div>
        <div className="mt-2 grid md:grid-cols-[1fr_160px_160px] gap-3">
          <input className="input input-bordered w-full" placeholder="Search saree/blouse/style..." value={q} onChange={(e) => setQ(e.target.value)} />
          <select className="select select-bordered w-full" value={category} onChange={(e) => setCategory(e.target.value)}>
            <option value="all">All</option>
            <option value="saree">Saree</option>
            <option value="blouse">Blouse</option>
            <option value="accessories">Accessories</option>
            <option value="jewelry">Jewelry</option>
          </select>
          <select className="select select-bordered w-full" value={String(maxPrice)} onChange={(e) => setMaxPrice(Number(e.target.value))}>
            <option value="999999">Any price</option>
            <option value="1500">≤ 1500</option>
            <option value="2500">≤ 2500</option>
            <option value="5000">≤ 5000</option>
          </select>
        </div>
        <div className="mt-3 text-xs opacity-70">Instant results + filters. Images lazy-load.</div>
      </div>

      {loading && !products.length ? <div className="skeleton h-40 w-full" /> : null}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.slice(0, 60).map((p) => (
          <ProductCard key={p.id} p={p} />
        ))}
        {!loading && !filtered.length ? <div className="opacity-70">No results.</div> : null}
      </div>
    </div>
  );
}

