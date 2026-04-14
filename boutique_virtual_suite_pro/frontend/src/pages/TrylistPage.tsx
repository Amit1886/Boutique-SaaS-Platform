import { useEffect } from "react";
import { useTrylistStore } from "../stores/trylistStore";
import { useAuthStore } from "../stores/authStore";

export default function TrylistPage() {
  const token = useAuthStore((s) => s.token);
  const items = useTrylistStore((s) => s.items);
  const load = useTrylistStore((s) => s.load);
  const remove = useTrylistStore((s) => s.remove);

  useEffect(() => {
    if (token) load().catch(() => {});
  }, [token, load]);

  return (
    <div className="space-y-5 fade-in">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-2xl font-extrabold">Trylist Queue</div>
        <div className="mt-2 text-sm opacity-70">Sticky drawer + reorder + offline cache.</div>
      </div>
      {!token ? <div className="alert alert-warning">Login to use Trylist.</div> : null}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {items.map((it) => (
          <div key={it.product_id} className="rounded-2xl border border-base-300 bg-base-100 overflow-hidden">
            {it.product?.image_url ? <img src={it.product.image_url} className="w-full h-48 object-cover" /> : null}
            <div className="p-4">
              <div className="font-semibold">{it.product?.name || `#${it.product_id}`}</div>
              <div className="mt-2">
                <button className="btn btn-sm btn-ghost" onClick={() => remove(it.product_id)}>
                  Remove
                </button>
              </div>
            </div>
          </div>
        ))}
        {!items.length ? <div className="opacity-70">Empty.</div> : null}
      </div>
    </div>
  );
}

