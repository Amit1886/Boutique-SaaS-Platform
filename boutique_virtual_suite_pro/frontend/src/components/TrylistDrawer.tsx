import { useEffect, useRef, useState } from "react";
import { useTrylistStore } from "../stores/trylistStore";
import { useAuthStore } from "../stores/authStore";
import Modal from "./Modal";
import ImageCompareSlider from "./ImageCompareSlider";

export default function TrylistDrawer() {
  const open = useTrylistStore((s) => s.open);
  const setOpen = useTrylistStore((s) => s.setOpen);
  const items = useTrylistStore((s) => s.items);
  const load = useTrylistStore((s) => s.load);
  const remove = useTrylistStore((s) => s.remove);
  const move = useTrylistStore((s) => s.move);
  const syncOrder = useTrylistStore((s) => s.syncOrder);
  const token = useAuthStore((s) => s.token);
  const dragging = useRef<number | null>(null);
  const [preview, setPreview] = useState<{ title: string; url: string } | null>(null);

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
                  <div
                    key={it.product_id}
                    className="rounded-2xl border border-base-300 bg-base-100 p-3"
                    draggable
                    onDragStart={() => {
                      dragging.current = it.product_id;
                    }}
                    onDragOver={(e) => e.preventDefault()}
                    onDrop={() => {
                      if (!dragging.current || dragging.current === it.product_id) return;
                      // Move dragged item towards this item repeatedly (simple).
                      const sorted = items.slice().sort((a, b) => a.position - b.position);
                      const from = sorted.findIndex((x) => x.product_id === dragging.current);
                      const to = sorted.findIndex((x) => x.product_id === it.product_id);
                      if (from < 0 || to < 0) return;
                      const dir = from < to ? 1 : -1;
                      for (let k = from; k !== to; k += dir) {
                        const pid = sorted[k].product_id;
                        move(pid, dir as any);
                      }
                      syncOrder().catch(() => {});
                      dragging.current = null;
                    }}
                  >
                    <div className="flex gap-3">
                      <div className="w-16 h-16 rounded-xl overflow-hidden bg-base-200">
                        {it.product?.image_url ? <img src={it.product.image_url} className="w-full h-full object-cover" /> : null}
                      </div>
                      <div className="flex-1 min-w-0">
                        <button
                          className="font-semibold truncate text-left w-full hover:underline"
                          onClick={() =>
                            it.product?.image_url
                              ? setPreview({ title: it.product.name, url: it.product.image_url })
                              : null
                          }
                        >
                          {it.product?.name || `#${it.product_id}`}
                        </button>
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
    <Modal open={!!preview} title={preview?.title} onClose={() => setPreview(null)}>
      {preview?.url ? (
        <ImageCompareSlider beforeUrl={preview.url} afterUrl={preview.url} />
      ) : (
        <div className="opacity-70">No preview</div>
      )}
    </Modal>
  );
}
