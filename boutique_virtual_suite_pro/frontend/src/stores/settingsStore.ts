import { create } from "zustand";
import { cacheGet, cacheSet } from "../lib/cache";

type Theme = "bvp_light" | "dark";
type Lang = "en" | "hi";

type SettingsState = {
  theme: Theme;
  lang: Lang;
  setTheme: (t: Theme) => void;
  setLang: (l: Lang) => void;
};

export const useSettingsStore = create<SettingsState>((set) => ({
  theme: (cacheGet<Theme>("bvp.theme") as Theme) || "bvp_light",
  lang: (cacheGet<Lang>("bvp.lang") as Lang) || "en",
  setTheme: (theme) => {
    cacheSet("bvp.theme", theme, 1000 * 60 * 60 * 24 * 365);
    set({ theme });
  },
  setLang: (lang) => {
    cacheSet("bvp.lang", lang, 1000 * 60 * 60 * 24 * 365);
    set({ lang });
  }
}));

