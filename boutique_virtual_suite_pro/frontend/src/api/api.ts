import { http } from "./http";

export async function apiGet<T>(path: string) {
  const res = await http.get<T>(path);
  return res.data as any;
}

export async function apiPost<T>(path: string, body?: any) {
  const res = await http.post<T>(path, body || {});
  return res.data as any;
}

