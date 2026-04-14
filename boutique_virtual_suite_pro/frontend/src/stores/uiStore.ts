import { create } from "zustand";

export type ToastKind = "success" | "error" | "info";
export type Toast = { id: string; kind: ToastKind; title: string; message?: string };

type UIState = {
  toasts: Toast[];
  toast: (t: Omit<Toast, "id">) => void;
  dismiss: (id: string) => void;
};

function _id() {
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

export const useUIStore = create<UIState>((set, get) => ({
  toasts: [],
  toast: (t) => {
    const id = _id();
    const next = [...get().toasts, { ...t, id }].slice(-5);
    set({ toasts: next });
    setTimeout(() => get().dismiss(id), 3200);
  },
  dismiss: (id) => set({ toasts: get().toasts.filter((x) => x.id !== id) })
}));

