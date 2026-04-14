import { create } from "zustand";
import { apiFetch } from "../api/client";
import { cacheGet, cacheSet } from "../lib/cache";
import { useAuthStore } from "./authStore";
import type { Product } from "./productStore";
import { useUIStore } from "./uiStore";

type FavRow = { product_id: number; product: Product | null };

type FavoritesState = {
  ids: Set<number>;
  rows: FavRow[];
  load: () => Promise<void>;
  toggle: (productId: number) => Promise<void>;
};

function _setFromRows(rows: FavRow[]) {
  const ids = new Set<number>();
  for (const r of rows) ids.add(r.product_id);
  return ids;
}

export const useFavoritesStore = create<FavoritesState>((set, get) => ({
  ids: new Set<number>(cacheGet<number[]>("bvp.fav.ids") || []),
  rows: cacheGet<FavRow[]>("bvp.fav.rows") || [],
  load: async () => {
    const token = useAuthStore.getState().token;
    if (!token) {
      set({ rows: [], ids: new Set() });
      return;
    }
    const res = await apiFetch<{ ok: true; favorites: FavRow[] }>("/favorites/all", { method: "GET" });
    cacheSet("bvp.fav.rows", res.favorites, 1000 * 60 * 10);
    const idsArr = res.favorites.map((r) => r.product_id);
    cacheSet("bvp.fav.ids", idsArr, 1000 * 60 * 60);
    set({ rows: res.favorites, ids: _setFromRows(res.favorites) });
  },
  toggle: async (productId) => {
    const token = useAuthStore.getState().token;
    if (!token) return;
    const ids = new Set(get().ids);
    const has = ids.has(productId);
    if (has) {
      await apiFetch("/favorites/remove", { method: "POST", body: JSON.stringify({ product_id: productId }) });
      ids.delete(productId);
      useUIStore.getState().toast({ kind: "info", title: "Removed from Favorites" });
    } else {
      await apiFetch("/favorites/add", { method: "POST", body: JSON.stringify({ product_id: productId }) });
      ids.add(productId);
      useUIStore.getState().toast({ kind: "success", title: "Saved to Favorites" });
    }
    cacheSet("bvp.fav.ids", Array.from(ids), 1000 * 60 * 60);
    set({ ids });
    // Refresh rows in background
    get().load().catch(() => {});
  }
}));
