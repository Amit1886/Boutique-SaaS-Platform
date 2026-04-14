import { create } from "zustand";
import { apiFetch } from "../api/client";
import { cacheGet, cacheSet } from "../lib/cache";
import type { Product } from "./productStore";
import { useUIStore } from "./uiStore";

type TryItem = { product_id: number; position: number; product: Product | null };

type TrylistState = {
  items: TryItem[];
  open: boolean;
  setOpen: (v: boolean) => void;
  load: () => Promise<void>;
  add: (productId: number) => Promise<void>;
  remove: (productId: number) => Promise<void>;
  move: (productId: number, dir: -1 | 1) => void;
  syncOrder: () => Promise<void>;
};

export const useTrylistStore = create<TrylistState>((set, get) => ({
  items: cacheGet<TryItem[]>("bvp.trylist") || [],
  open: false,
  setOpen: (open) => set({ open }),
  load: async () => {
    const cached = cacheGet<TryItem[]>("bvp.trylist");
    if (cached) set({ items: cached });
    const res = await apiFetch<{ ok: true; items: TryItem[] }>("/trylist/all", { method: "GET" });
    cacheSet("bvp.trylist", res.items, 1000 * 60 * 5);
    set({ items: res.items });
  },
  add: async (productId) => {
    await apiFetch("/trylist/add", { method: "POST", body: JSON.stringify({ product_id: productId }) });
    await get().load();
    set({ open: true });
    useUIStore.getState().toast({ kind: "success", title: "Added to Trylist" });
  },
  remove: async (productId) => {
    await apiFetch("/trylist/remove", { method: "POST", body: JSON.stringify({ product_id: productId }) });
    await get().load();
    useUIStore.getState().toast({ kind: "info", title: "Removed from Trylist" });
  },
  move: (productId, dir) => {
    const items = [...get().items].sort((a, b) => a.position - b.position);
    const idx = items.findIndex((i) => i.product_id === productId);
    const j = idx + dir;
    if (idx < 0 || j < 0 || j >= items.length) return;
    const a = items[idx];
    const b = items[j];
    const tmp = a.position;
    a.position = b.position;
    b.position = tmp;
    const normalized = items
      .sort((x, y) => x.position - y.position)
      .map((x, k) => ({ ...x, position: k + 1 }));
    cacheSet("bvp.trylist", normalized, 1000 * 60 * 60);
    set({ items: normalized });
    // Best-effort sync to server (no blocking UX).
    get().syncOrder().catch(() => {});
  },
  syncOrder: async () => {
    const items = get().items.slice().sort((a, b) => a.position - b.position);
    const order = items.map((i) => i.product_id);
    await apiFetch("/trylist/reorder", { method: "POST", body: JSON.stringify({ order }) });
  },
}));
