import { useAuthStore } from "../stores/authStore";

const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000/api";

export async function apiFetch<T>(path: string, opts: RequestInit = {}): Promise<T> {
  const token = useAuthStore.getState().token;
  const headers = new Headers(opts.headers || {});
  headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const res = await fetch(`${baseUrl}${path}`, { ...opts, headers });
  const json = await res.json().catch(() => ({}));
  if (!res.ok || (json && json.ok === false)) {
    const msg = (json && json.error) || `Request failed (${res.status})`;
    throw new Error(msg);
  }
  return json as T;
}

