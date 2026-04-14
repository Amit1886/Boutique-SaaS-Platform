import { useEffect } from "react";
import { useTrylistStore } from "../stores/trylistStore";
import { useAuthStore } from "../stores/authStore";

export default function TrylistDrawer() {
  const open = useTrylistStore((s) => s.open);
  const setOpen = useTrylistStore((s) => s.setOpen);
  const items = useTrylistStore((s) => s.items);
  const load = useTrylistStore((s) => s.load);
  const remove = useTrylistStore((s) => s.remove);
  const move = useTrylistStore((s) => s.move);
  const token = useAuthStore((s) => s.token);

  useEffect(() => {
    if (open && token) load().catch(() => {});
  }, [open, token, load]);

  return (
    <div className={`fixed inset-0 z-50 ${open ? "" : "pointer-events-none"}`}>
      <div className={`absolute inset-0 transition ${open ? "bg-black/30" : "bg-transparent"}`} onClick={() => setOpen(false)} />
      <div className={`absolute right-0 top-0 h-full w-[92%] sm:w-[420px] transition-transform ${open ? "translate-x-0" : "translate-x-full"}`}>
        <div className="h-full glass border-l border-base-300 p-4">
          <div className="flex items-center justify-between">
            <div className="font-bold">Trylist</div>
            <button className="btn btn-ghost btn-sm" onClick={() => setOpen(false)}>
              Close
            </button>
          </div>
          {!token ? (
            <div className="mt-4 text-sm opacity-70">Login to use Trylist.</div>
          ) : (
            <div className="mt-4 space-y-3 overflow-auto max-h-[calc(100vh-90px)] pr-1">
              {items
                .slice()
                .sort((a, b) => a.position - b.position)
                .map((it) => (
                  <div key={it.product_id} className="rounded-2xl border border-base-300 bg-base-100 p-3">
                    <div className="flex gap-3">
                      <div className="w-16 h-16 rounded-xl overflow-hidden bg-base-200">
                        {it.product?.image_url ? <img src={it.product.image_url} className="w-full h-full object-cover" /> : null}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="font-semibold truncate">{it.product?.name || `#${it.product_id}`}</div>
                        <div className="text-xs opacity-70">{it.product?.category}</div>
                        <div className="mt-2 flex gap-2">
                          <button className="btn btn-xs" onClick={() => move(it.product_id, -1)}>
                            ↑
                          </button>
                          <button className="btn btn-xs" onClick={() => move(it.product_id, 1)}>
                            ↓
                          </button>
                          <button className="btn btn-xs btn-ghost" onClick={() => remove(it.product_id)}>
                            Remove
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              {!items.length ? <div className="text-sm opacity-70">Empty. Add items from Home.</div> : null}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

