import { useEffect, useMemo, useRef, useState } from "react";
import { apiGet, apiPost } from "../api/client";
import { useAppStore } from "../store/useAppStore";
import { useTryOnStore } from "../store/useTryOnStore";
import { toPng } from "html-to-image";

type SavedLook = {
  id: number;
  user_name: string;
  saree_id: number | null;
  blouse_id: number | null;
  accessories_json: string;
  image_card_png: string;
  created_at: string;
};

export default function SavedLooksPage() {
  const userName = useAppStore((s) => s.userName);
  const saree = useTryOnStore((s) => s.selectedSaree);
  const blouse = useTryOnStore((s) => s.selectedBlouse);
  const accessories = useTryOnStore((s) => s.selectedAccessories);
  const [looks, setLooks] = useState<SavedLook[]>([]);
  const cardRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    apiGet<{ ok: true; items: SavedLook[] }>("/gallery/looks")
      .then((r) => setLooks(r.items || []))
      .catch(() => {});
  }, []);

  const total = useMemo(() => {
    return (saree?.price || 0) + (blouse?.price || 0) + accessories.reduce((s, a) => s + (a.price || 0), 0);
  }, [saree, blouse, accessories]);

  async function saveCard() {
    if (!cardRef.current) return;
    const dataUrl = await toPng(cardRef.current, { cacheBust: true, pixelRatio: 2 });
    const payload = {
      user_name: userName,
      saree_id: saree?.id || null,
      blouse_id: blouse?.id || null,
      accessories_json: JSON.stringify(accessories.map((a) => a.id)),
      image_card_png: dataUrl
    };
    const res = await apiPost<{ ok: true; item: SavedLook }>("/gallery/save", payload);
    setLooks([res.item, ...looks]);
  }

  async function share() {
    const res = await apiPost<{ ok: true; whatsapp_url: string }>("/look/share", {
      user_name: userName,
      look_name: saree?.name || "My Look",
      price: `₹${total}`
    });
    window.open(res.whatsapp_url, "_blank");
  }

  return (
    <div className="max-w-7xl mx-auto px-3 md:px-6 py-6 space-y-6">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-2xl font-extrabold">My Saved Looks</div>
        <div className="mt-2 text-sm opacity-70">Export outfit card + share to WhatsApp.</div>
      </div>

      <div className="grid lg:grid-cols-[1fr_360px] gap-4 items-start">
        <div className="rounded-2xl border border-base-300 bg-base-100 p-5">
          <div className="font-bold">Outfit Card Creator</div>
          <div className="mt-4 rounded-2xl border border-base-300 bg-base-200 p-4" ref={cardRef}>
            <div className="text-xs opacity-70">Boutique Magic</div>
            <div className="mt-1 text-xl font-extrabold">{saree?.name || "Select a saree"}</div>
            <div className="mt-2 text-sm opacity-70">By {userName}</div>
            <div className="mt-3 grid grid-cols-2 gap-3 text-sm">
              <div className="rounded-xl bg-base-100 p-3 border border-base-300">
                <div className="text-xs opacity-70">Saree</div>
                <div className="font-semibold">{saree?.name || "—"}</div>
              </div>
              <div className="rounded-xl bg-base-100 p-3 border border-base-300">
                <div className="text-xs opacity-70">Blouse</div>
                <div className="font-semibold">{blouse?.name || "—"}</div>
              </div>
            </div>
            <div className="mt-3 rounded-xl bg-base-100 p-3 border border-base-300">
              <div className="text-xs opacity-70">Total</div>
              <div className="text-2xl font-extrabold" style={{ color: "var(--magic-color)" }}>
                ₹{total}
              </div>
            </div>
            <div className="mt-3 text-xs opacity-70">{new Date().toLocaleDateString()}</div>
          </div>

          <div className="mt-4 flex gap-2">
            <button className="btn btn-primary" onClick={saveCard}>
              Save
            </button>
            <button className="btn" onClick={share}>
              Share to WhatsApp
            </button>
          </div>
        </div>

        <div className="glass rounded-2xl border border-base-300 p-4">
          <div className="font-bold">History</div>
          <div className="mt-3 space-y-3 max-h-[65vh] overflow-auto pr-1">
            {looks.map((l) => (
              <div key={l.id} className="rounded-2xl border border-base-300 bg-base-100 p-4">
                <div className="text-xs opacity-70">{l.user_name}</div>
                <div className="mt-1 font-bold">Look #{l.id}</div>
                <div className="mt-2 text-xs opacity-70">{l.created_at}</div>
              </div>
            ))}
            {!looks.length ? <div className="opacity-70 text-sm">No saved looks yet.</div> : null}
          </div>
        </div>
      </div>
    </div>
  );
}

