import { useEffect } from "react";
import { useAuthStore } from "../stores/authStore";
import { useFavoritesStore } from "../stores/favoritesStore";
import ProductCard from "../components/ProductCard";

export default function FavoritesPage() {
  const token = useAuthStore((s) => s.token);
  const rows = useFavoritesStore((s) => s.rows);
  const load = useFavoritesStore((s) => s.load);

  useEffect(() => {
    if (token) load().catch(() => {});
  }, [token, load]);

  return (
    <div className="space-y-5 fade-in">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-2xl font-extrabold">Favorites</div>
        <div className="mt-2 text-sm opacity-70">Saved items sync across devices.</div>
      </div>
      {!token ? <div className="alert alert-warning">Login to use Favorites.</div> : null}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {rows.filter((r) => r.product).map((r) => (
          <ProductCard key={r.product_id} p={r.product!} />
        ))}
        {token && !rows.length ? <div className="opacity-70">No favorites yet.</div> : null}
      </div>
    </div>
  );
}

