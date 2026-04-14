import { create } from "zustand";
import { apiGet } from "../api/client";

export type UXFlag = { key: string; enabled: boolean };

type UxState = {
  flags: Record<string, boolean>;
  load: () => Promise<void>;
  isOn: (key: string) => boolean;
};

export const useUxStore = create<UxState>((set, get) => ({
  flags: {},
  load: async () => {
    const res = await apiGet<{ ok: true; items: UXFlag[] }>("/uxflags");
    const map: Record<string, boolean> = {};
    for (const f of res.items || []) map[f.key] = !!f.enabled;
    set({ flags: map });
  },
  isOn: (key: string) => {
    const v = get().flags[key];
    return v === undefined ? true : !!v;
  }
}));

