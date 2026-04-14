import { create } from "zustand";
import { cacheGet, cacheSet } from "../lib/cache";
import { apiFetch } from "../api/client";
import { useAuthStore } from "./authStore";

type DesignerState = {
  selected: {
    saree?: number;
    blouse?: number;
    accessories?: number;
    jewelry?: number;
  };
  setSelected: (category: "saree" | "blouse" | "accessories" | "jewelry", productId: number) => void;
  hydrateFromServer: () => Promise<void>;
  syncToServer: () => Promise<void>;
};

const KEY = "bvp.designer.selected";

export const useDesignerStore = create<DesignerState>((set, get) => ({
  selected: cacheGet<any>(KEY) || {},
  setSelected: (category, productId) => {
    const next = { ...get().selected, [category]: productId };
    cacheSet(KEY, next, 1000 * 60 * 60 * 24 * 30);
    set({ selected: next });
    // Best-effort sync.
    get().syncToServer().catch(() => {});
  },
  hydrateFromServer: async () => {
    const token = useAuthStore.getState().token;
    if (!token) return;
    const res = await apiFetch<{ ok: true; progress: any }>("/designer/progress", { method: "GET" });
    const selected = (res.progress && res.progress.selected) || {};
    cacheSet(KEY, selected, 1000 * 60 * 60 * 24 * 30);
    set({ selected });
  },
  syncToServer: async () => {
    const token = useAuthStore.getState().token;
    if (!token) return;
    const selected = get().selected || {};
    await apiFetch("/designer/progress", { method: "POST", body: JSON.stringify({ progress: { selected } }) });
  }
}));

