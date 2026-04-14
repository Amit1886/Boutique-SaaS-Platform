import { http } from "./http";

export async function apiGet<T>(path: string, config?: { headers?: Record<string, string> }) {
  const res = await http.get<T>(path, config);
  return res.data as any;
}

export async function apiPost<T>(path: string, body?: any, headers?: Record<string, string>) {
  const res = await http.post<T>(path, body || {}, headers ? { headers } : undefined);
  return res.data as any;
}

export async function apiDelete<T>(path: string, headers?: Record<string, string>) {
  const res = await http.delete<T>(path, headers ? { headers } : undefined);
  return res.data as any;
}

export async function apiPut<T>(path: string, body?: any, headers?: Record<string, string>) {
  const res = await http.put<T>(path, body || {}, headers ? { headers } : undefined);
  return res.data as any;
}
