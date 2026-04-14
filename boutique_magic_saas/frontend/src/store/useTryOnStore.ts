import { create } from "zustand";
import type { Accessory, Blouse, Saree } from "./useCatalogStore";

type TryOnState = {
  selectedSaree: Saree | null;
  selectedBlouse: Blouse | null;
  selectedAccessories: Accessory[];
  setSaree: (s: Saree | null) => void;
  setBlouse: (b: Blouse | null) => void;
  toggleAccessory: (a: Accessory) => void;
  clear: () => void;
};

export const useTryOnStore = create<TryOnState>((set, get) => ({
  selectedSaree: null,
  selectedBlouse: null,
  selectedAccessories: [],
  setSaree: (s) => set({ selectedSaree: s }),
  setBlouse: (b) => set({ selectedBlouse: b }),
  toggleAccessory: (a) => {
    const has = get().selectedAccessories.some((x) => x.id === a.id);
    if (has) set({ selectedAccessories: get().selectedAccessories.filter((x) => x.id !== a.id) });
    else set({ selectedAccessories: [...get().selectedAccessories, a] });
  },
  clear: () => set({ selectedSaree: null, selectedBlouse: null, selectedAccessories: [] })
}));

