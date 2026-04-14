import { http } from "./http";

export async function apiFetch<T>(path: string, opts: RequestInit = {}): Promise<T> {
  const method = (opts.method || "GET").toUpperCase();
  let data: any = undefined;
  if (opts.body) {
    try {
      data = JSON.parse(String(opts.body));
    } catch {
      data = opts.body;
    }
  }
  if (method === "GET") {
    const res = await http.get<T>(path);
    return res.data as any;
  }
  const res = await http.request<T>({ url: path, method, data });
  return res.data as any;
}
