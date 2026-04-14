import { create } from "zustand";
import { apiFetch } from "../api/client";
import { cacheGet, cacheSet } from "../lib/cache";
import { useAuthStore } from "./authStore";

export type Mood = { key: string; name_en: string; name_hi: string; theme_color: string; banner: string };

type MoodState = {
  moods: Mood[];
  activeKey: string;
  banner: string;
  themeColor: string;
  loadMoods: () => Promise<void>;
  applyMood: (key: string) => Promise<void>;
};

export const useMoodStore = create<MoodState>((set) => ({
  moods: cacheGet<Mood[]>("bvp.moods") || [],
  activeKey: cacheGet<string>("bvp.mood.active") || "festive",
  banner: cacheGet<string>("bvp.mood.banner") || "",
  themeColor: cacheGet<string>("bvp.mood.color") || "#db2777",
  loadMoods: async () => {
    const cached = cacheGet<Mood[]>("bvp.moods");
    if (cached && cached.length) set({ moods: cached });
    const res = await apiFetch<{ ok: true; moods: Mood[] }>("/mood/list", { method: "GET" });
    cacheSet("bvp.moods", res.moods, 1000 * 60 * 60);
    set({ moods: res.moods });
  },
  applyMood: async (key: string) => {
    // Also update instantly for UX, even if server fails.
    const localMood = (cacheGet<Mood[]>("bvp.moods") || []).find((m) => m.key === key);
    if (localMood) {
      cacheSet("bvp.mood.active", localMood.key, 1000 * 60 * 60 * 24);
      cacheSet("bvp.mood.color", localMood.theme_color, 1000 * 60 * 60 * 24);
      cacheSet("bvp.mood.banner", localMood.banner, 1000 * 60 * 60 * 24);
      set({ activeKey: localMood.key, themeColor: localMood.theme_color, banner: localMood.banner });
    }
    const token = useAuthStore.getState().token;
    if (token) {
      const res = await apiFetch<{ ok: true; mood: { key: string; theme_color: string; banner: string } }>("/mood/apply", {
        method: "POST",
        body: JSON.stringify({ key })
      });
      cacheSet("bvp.mood.active", res.mood.key, 1000 * 60 * 60 * 24);
      cacheSet("bvp.mood.color", res.mood.theme_color, 1000 * 60 * 60 * 24);
      cacheSet("bvp.mood.banner", res.mood.banner, 1000 * 60 * 60 * 24);
      set({ activeKey: res.mood.key, themeColor: res.mood.theme_color, banner: res.mood.banner });
    }
  }
}));
