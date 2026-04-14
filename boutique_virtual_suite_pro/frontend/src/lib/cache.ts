type CacheEntry<T> = { v: T; t: number; ttl: number };

export function cacheGet<T>(key: string): T | null {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as CacheEntry<T>;
    if (!parsed || typeof parsed.t !== "number") return null;
    if (Date.now() - parsed.t > parsed.ttl) return null;
    return parsed.v;
  } catch {
    return null;
  }
}

export function cacheSet<T>(key: string, value: T, ttlMs: number) {
  const entry: CacheEntry<T> = { v: value, t: Date.now(), ttl: ttlMs };
  localStorage.setItem(key, JSON.stringify(entry));
}

