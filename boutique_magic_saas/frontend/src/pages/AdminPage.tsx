import { useEffect, useState } from "react";
import { apiDelete, apiGet, apiPost, apiPut } from "../api/client";

async function uploadFile(path: string, token: string, file: File, extra?: Record<string, string>) {
  const fd = new FormData();
  fd.append("file", file);
  const url = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8008/api") + path;
  const res = await fetch(url, {
    method: "POST",
    headers: { "X-Admin-Token": token, ...(extra || {}) } as any,
    body: fd
  });
  const json = await res.json();
  if (!res.ok || json.ok === false) throw new Error(json.error || json.detail || "upload failed");
  return json.path as string;
}

type Saree = any;
type Blouse = any;
type Accessory = any;
type UXFlag = { key: string; enabled: boolean };

function hdr(token: string) {
  return { "X-Admin-Token": token };
}

export default function AdminPage() {
  const [token, setToken] = useState(localStorage.getItem("magic.admin") || "");
  const [sarees, setSarees] = useState<Saree[]>([]);
  const [blouses, setBlouses] = useState<Blouse[]>([]);
  const [accessories, setAccessories] = useState<Accessory[]>([]);
  const [flags, setFlags] = useState<UXFlag[]>([]);
  const [selectedSareeId, setSelectedSareeId] = useState<number | null>(null);
  const [festivals, setFestivals] = useState<any[]>([]);
  const [festivalForm, setFestivalForm] = useState({ name: "Holi", start_date: "2026-03-10", end_date: "2026-03-20", theme_color: "#0ea5e9", banner_text: "Color Bloom" });
  const [msg, setMsg] = useState("");

  async function refresh() {
    const [s, b, a] = await Promise.all([
      apiGet<{ ok: true; items: Saree[] }>("/sarees"),
      apiGet<{ ok: true; items: Blouse[] }>("/blouses"),
      apiGet<{ ok: true; items: Accessory[] }>("/accessories")
    ]);
    setSarees(s.items || []);
    setBlouses(b.items || []);
    setAccessories(a.items || []);
    if (token) {
      const f = await apiGet<{ ok: true; items: UXFlag[] }>("/admin/uxflags", { headers: hdr(token) });
      setFlags(f.items || []);
      const fe = await apiGet<{ ok: true; items: any[] }>("/admin/festivals", { headers: hdr(token) });
      setFestivals(fe.items || []);
    }
  }

  useEffect(() => {
    refresh().catch(() => {});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function saveToken() {
    localStorage.setItem("magic.admin", token);
    setMsg("Saved admin token.");
    refresh().catch(() => {});
  }

  async function addSaree() {
    const payload = { name: "New Saree", price: 1999, primary_color: "#db2777", tags: "festive", layer_body_png: "", layer_pallu_png: "", layer_border_png: "" };
    await apiPost("/sarees", payload, hdr(token));
    setMsg("Saree added.");
    refresh().catch(() => {});
  }
  async function addBlouse() {
    const payload = { name: "New Blouse", price: 799, primary_color: "#7c3aed", tags: "match", template_png: "" };
    await apiPost("/blouses", payload, hdr(token));
    setMsg("Blouse added.");
    refresh().catch(() => {});
  }
  async function addAccessory() {
    const payload = { name: "New Accessory", price: 299, primary_color: "#0ea5e9", tags: "sparkle", image_png: "" };
    await apiPost("/accessories", payload, hdr(token));
    setMsg("Accessory added.");
    refresh().catch(() => {});
  }

  async function del(kind: "sarees" | "blouses" | "accessories", id: number) {
    await apiDelete(`/${kind}/${id}`, hdr(token));
    refresh().catch(() => {});
  }

  async function toggleFlag(k: string, enabled: boolean) {
    await apiPost(`/admin/uxflags/${k}`, { enabled }, hdr(token));
    refresh().catch(() => {});
  }

  async function uploadLayer(kind: "body" | "pallu" | "border", file: File) {
    if (!selectedSareeId) return;
    const path = await uploadFile(`/upload/saree-layer?kind=${kind}`, token, file);
    const field = kind === "body" ? "layer_body_png" : kind === "pallu" ? "layer_pallu_png" : "layer_border_png";
    await apiPut(`/sarees/${selectedSareeId}`, { [field]: path }, hdr(token) as any);
    setMsg(`Uploaded ${kind} layer.`);
    refresh().catch(() => {});
  }

  async function uploadBlouse(file: File, id: number) {
    const path = await uploadFile("/upload/blouse-template", token, file);
    await apiPut(`/blouses/${id}`, { template_png: path }, hdr(token) as any);
    setMsg("Uploaded blouse template.");
    refresh().catch(() => {});
  }

  async function uploadAccessory(file: File, id: number) {
    const path = await uploadFile("/upload/accessory", token, file);
    await apiPut(`/accessories/${id}`, { image_png: path }, hdr(token) as any);
    setMsg("Uploaded accessory image.");
    refresh().catch(() => {});
  }

  async function createFestival() {
    await apiPost("/admin/festivals", festivalForm, hdr(token));
    setMsg("Festival theme added.");
    refresh().catch(() => {});
  }

  return (
    <div className="max-w-7xl mx-auto px-3 md:px-6 py-6 space-y-6">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-2xl font-extrabold">Admin Panel</div>
        <div className="mt-2 text-sm opacity-70">Add products + upload layer PNGs + toggle magic UX flags.</div>
        <div className="mt-4 flex flex-wrap gap-2 items-center">
          <input className="input input-bordered input-sm w-64" value={token} onChange={(e) => setToken(e.target.value)} placeholder="ADMIN_TOKEN" />
          <button className="btn btn-sm btn-primary" onClick={saveToken}>Save</button>
          {msg ? <span className="text-sm opacity-70">{msg}</span> : null}
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-4 items-start">
        <div className="glass rounded-2xl border border-base-300 p-4">
          <div className="flex items-center justify-between">
            <div className="font-bold">Sarees</div>
            <button className="btn btn-sm btn-primary" onClick={addSaree}>Add</button>
          </div>
          <div className="mt-3 space-y-2 max-h-[55vh] overflow-auto pr-1">
            {sarees.map((s) => (
              <div key={s.id} className="rounded-2xl border border-base-300 bg-base-100 p-3">
                <div className="font-semibold">{s.name}</div>
                <div className="text-xs opacity-70">₹{s.price}</div>
                <div className="mt-2 flex gap-2">
                  <button className="btn btn-xs" onClick={() => setSelectedSareeId(s.id)}>Select</button>
                  <button className="btn btn-xs btn-ghost" onClick={() => del("sarees", s.id)}>Delete</button>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="glass rounded-2xl border border-base-300 p-4">
          <div className="flex items-center justify-between">
            <div className="font-bold">Blouses</div>
            <button className="btn btn-sm btn-primary" onClick={addBlouse}>Add</button>
          </div>
          <div className="mt-3 space-y-2 max-h-[55vh] overflow-auto pr-1">
            {blouses.map((b) => (
              <div key={b.id} className="rounded-2xl border border-base-300 bg-base-100 p-3">
                <div className="font-semibold">{b.name}</div>
                <div className="text-xs opacity-70">₹{b.price}</div>
                <div className="mt-2 flex gap-2">
                  <label className="btn btn-xs">
                    Upload
                    <input type="file" className="hidden" accept="image/*" onChange={(e) => e.target.files?.[0] ? uploadBlouse(e.target.files[0], b.id).catch((er) => setMsg(er.message)) : null} />
                  </label>
                  <button className="btn btn-xs btn-ghost" onClick={() => del("blouses", b.id)}>Delete</button>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="glass rounded-2xl border border-base-300 p-4">
          <div className="flex items-center justify-between">
            <div className="font-bold">Accessories</div>
            <button className="btn btn-sm btn-primary" onClick={addAccessory}>Add</button>
          </div>
          <div className="mt-3 space-y-2 max-h-[55vh] overflow-auto pr-1">
            {accessories.map((a) => (
              <div key={a.id} className="rounded-2xl border border-base-300 bg-base-100 p-3">
                <div className="font-semibold">{a.name}</div>
                <div className="text-xs opacity-70">₹{a.price}</div>
                <div className="mt-2 flex gap-2">
                  <label className="btn btn-xs">
                    Upload
                    <input type="file" className="hidden" accept="image/*" onChange={(e) => e.target.files?.[0] ? uploadAccessory(e.target.files[0], a.id).catch((er) => setMsg(er.message)) : null} />
                  </label>
                  <button className="btn btn-xs btn-ghost" onClick={() => del("accessories", a.id)}>Delete</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="glass rounded-2xl border border-base-300 p-4">
        <div className="font-bold">Saree Layer Upload</div>
        <div className="mt-2 text-sm opacity-70">Select a saree, then upload body/pallu/border PNG layers.</div>
        <div className="mt-3 flex flex-wrap gap-2 items-center">
          <div className="badge badge-primary">Selected: {selectedSareeId || "none"}</div>
          <label className="btn btn-sm">
            Body PNG
            <input type="file" className="hidden" accept="image/*" onChange={(e) => e.target.files?.[0] ? uploadLayer("body", e.target.files[0]).catch((er) => setMsg(er.message)) : null} />
          </label>
          <label className="btn btn-sm">
            Pallu PNG
            <input type="file" className="hidden" accept="image/*" onChange={(e) => e.target.files?.[0] ? uploadLayer("pallu", e.target.files[0]).catch((er) => setMsg(er.message)) : null} />
          </label>
          <label className="btn btn-sm">
            Border PNG
            <input type="file" className="hidden" accept="image/*" onChange={(e) => e.target.files?.[0] ? uploadLayer("border", e.target.files[0]).catch((er) => setMsg(er.message)) : null} />
          </label>
        </div>
      </div>

      <div className="glass rounded-2xl border border-base-300 p-4">
        <div className="font-bold">Magic UX ON/OFF</div>
        <div className="mt-3 grid sm:grid-cols-2 lg:grid-cols-4 gap-2">
          {flags.map((f) => (
            <button key={f.key} className={`btn btn-sm ${f.enabled ? "btn-primary" : "btn-ghost"}`} onClick={() => toggleFlag(f.key, !f.enabled)}>
              {f.key}: {f.enabled ? "ON" : "OFF"}
            </button>
          ))}
          {!flags.length ? <div className="opacity-70 text-sm">Enter admin token to load flags.</div> : null}
        </div>
      </div>

      <div className="glass rounded-2xl border border-base-300 p-4">
        <div className="font-bold">Festival Themes</div>
        <div className="mt-3 grid md:grid-cols-5 gap-2">
          <input className="input input-bordered input-sm" value={festivalForm.name} onChange={(e) => setFestivalForm({ ...festivalForm, name: e.target.value })} placeholder="Name" />
          <input className="input input-bordered input-sm" value={festivalForm.start_date} onChange={(e) => setFestivalForm({ ...festivalForm, start_date: e.target.value })} placeholder="Start" />
          <input className="input input-bordered input-sm" value={festivalForm.end_date} onChange={(e) => setFestivalForm({ ...festivalForm, end_date: e.target.value })} placeholder="End" />
          <input className="input input-bordered input-sm" value={festivalForm.theme_color} onChange={(e) => setFestivalForm({ ...festivalForm, theme_color: e.target.value })} placeholder="#color" />
          <button className="btn btn-sm btn-primary" onClick={() => createFestival().catch((er) => setMsg(er.message))}>Add</button>
        </div>
        <div className="mt-2">
          <input className="input input-bordered input-sm w-full" value={festivalForm.banner_text} onChange={(e) => setFestivalForm({ ...festivalForm, banner_text: e.target.value })} placeholder="Banner text" />
        </div>
        <div className="mt-4 grid sm:grid-cols-2 lg:grid-cols-3 gap-2">
          {festivals.map((f) => (
            <div key={f.id} className="rounded-2xl border border-base-300 bg-base-100 p-3">
              <div className="font-semibold">{f.name}</div>
              <div className="text-xs opacity-70">{f.start_date} → {f.end_date}</div>
              <div className="mt-2 badge badge-primary">{f.theme_color}</div>
            </div>
          ))}
          {!festivals.length ? <div className="opacity-70 text-sm">No festivals yet.</div> : null}
        </div>
      </div>
    </div>
  );
}
