import { create } from "zustand";
import { apiFetch } from "../api/client";
import { cacheGet, cacheSet } from "../lib/cache";

export type Product = {
  id: number;
  name: string;
  category: string;
  image_url: string;
  base_color: string;
  fabric: string;
  style_tag: string;
  mood_tag: string;
  price: number;
};

type ProductState = {
  products: Product[];
  loading: boolean;
  error: string;
  loadAll: () => Promise<void>;
};

export const useProductStore = create<ProductState>((set) => ({
  products: cacheGet<Product[]>("bvp.products") || [],
  loading: false,
  error: "",
  loadAll: async () => {
    const cached = cacheGet<Product[]>("bvp.products");
    if (cached && cached.length) set({ products: cached });
    set({ loading: true, error: "" });
    try {
      const res = await apiFetch<{ ok: true; products: Product[] }>("/products/all", { method: "GET" });
      cacheSet("bvp.products", res.products, 1000 * 60 * 10);
      set({ products: res.products, loading: false });
    } catch (e: any) {
      set({ loading: false, error: e?.message || "Failed" });
    }
  }
}));

