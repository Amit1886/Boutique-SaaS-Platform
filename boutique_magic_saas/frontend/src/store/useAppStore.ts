import { create } from "zustand";

export type MoodKey = "festive" | "wedding" | "bridal" | "party" | "traditional";

type AppState = {
  userName: string;
  mood: MoodKey;
  magicColor: string;
  setUserName: (v: string) => void;
  setMood: (mood: MoodKey, color: string) => void;
};

export const useAppStore = create<AppState>((set) => ({
  userName: localStorage.getItem("magic.userName") || "Guest",
  mood: (localStorage.getItem("magic.mood") as MoodKey) || "festive",
  magicColor: localStorage.getItem("magic.color") || "#db2777",
  setUserName: (v) => {
    localStorage.setItem("magic.userName", v);
    set({ userName: v || "Guest" });
  },
  setMood: (mood, color) => {
    localStorage.setItem("magic.mood", mood);
    localStorage.setItem("magic.color", color);
    set({ mood, magicColor: color });
  }
}));

