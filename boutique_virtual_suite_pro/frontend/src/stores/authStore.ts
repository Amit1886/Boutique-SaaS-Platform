import { create } from "zustand";
import { cacheGet, cacheSet } from "../lib/cache";

type User = { id: number; email: string; name: string; language: string };

type AuthState = {
  token: string;
  user: User | null;
  setAuth: (token: string, user: User) => void;
  logout: () => void;
};

const TOKEN_KEY = "bvp.auth.token";
const USER_KEY = "bvp.auth.user";

export const useAuthStore = create<AuthState>((set) => ({
  token: cacheGet<string>(TOKEN_KEY) || "",
  user: cacheGet<User>(USER_KEY) || null,
  setAuth: (token, user) => {
    cacheSet(TOKEN_KEY, token, 1000 * 60 * 60 * 24 * 30);
    cacheSet(USER_KEY, user, 1000 * 60 * 60 * 24 * 30);
    set({ token, user });
  },
  logout: () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    set({ token: "", user: null });
  }
}));

