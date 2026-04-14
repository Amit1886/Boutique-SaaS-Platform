import { create } from "zustand";
import { apiGet } from "../api/client";

export type Saree = {
  id: number;
  name: string;
  price: number;
  primary_color: string;
  tags: string;
  layer_body_png: string;
  layer_pallu_png: string;
  layer_border_png: string;
};

export type Blouse = {
  id: number;
  name: string;
  price: number;
  primary_color: string;
  tags: string;
  template_png: string;
};

export type Accessory = {
  id: number;
  name: string;
  price: number;
  primary_color: string;
  tags: string;
  image_png: string;
};

type CatalogState = {
  sarees: Saree[];
  blouses: Blouse[];
  accessories: Accessory[];
  load: () => Promise<void>;
};

export const useCatalogStore = create<CatalogState>((set) => ({
  sarees: [],
  blouses: [],
  accessories: [],
  load: async () => {
    const [s, b, a] = await Promise.all([
      apiGet<{ ok: true; items: Saree[] }>("/sarees"),
      apiGet<{ ok: true; items: Blouse[] }>("/blouses"),
      apiGet<{ ok: true; items: Accessory[] }>("/accessories")
    ]);
    set({ sarees: s.items || [], blouses: b.items || [], accessories: a.items || [] });
  }
}));

