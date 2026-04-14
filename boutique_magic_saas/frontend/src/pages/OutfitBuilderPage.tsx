import { useEffect, useState } from "react";
import OutfitCanvas from "../components/OutfitCanvas";
import { useCatalogStore } from "../store/useCatalogStore";
import { useTryOnStore } from "../store/useTryOnStore";
import TailorJinn from "../components/TailorJinn";

export default function OutfitBuilderPage() {
  const load = useCatalogStore((s) => s.load);
  const sarees = useCatalogStore((s) => s.sarees);
  const blouses = useCatalogStore((s) => s.blouses);
  const accessories = useCatalogStore((s) => s.accessories);

  const saree = useTryOnStore((s) => s.selectedSaree);
  const blouse = useTryOnStore((s) => s.selectedBlouse);
  const selectedAccessories = useTryOnStore((s) => s.selectedAccessories);
  const setSaree = useTryOnStore((s) => s.setSaree);
  const setBlouse = useTryOnStore((s) => s.setBlouse);
  const toggleAccessory = useTryOnStore((s) => s.toggleAccessory);

  const [jinnKey, setJinnKey] = useState("builder");

  useEffect(() => {
    load().catch(() => {});
  }, [load]);

  return (
    <div className="max-w-7xl mx-auto px-3 md:px-6 py-6 space-y-6">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-2xl font-extrabold">Outfit Builder</div>
        <div className="mt-2 text-sm opacity-70">Drag layers: saree, blouse, accessories (composition).</div>
      </div>

      <div className="grid lg:grid-cols-[1fr_360px] gap-4 items-start">
        <OutfitCanvas saree={saree} blouse={blouse} accessories={selectedAccessories} />
        <div className="glass rounded-2xl border border-base-300 p-4 space-y-4">
          <div>
            <div className="font-bold">Saree</div>
            <div className="mt-2 grid grid-cols-2 gap-2">
              {sarees.slice(0, 10).map((s) => (
                <button
                  key={s.id}
                  className={`btn btn-sm ${saree?.id === s.id ? "btn-primary" : "btn-ghost"}`}
                  onClick={() => {
                    setSaree(s);
                    setJinnKey(`b-saree-${s.id}`);
                  }}
                >
                  {s.name.slice(0, 10)}
                </button>
              ))}
            </div>
          </div>
          <div>
            <div className="font-bold">Blouse</div>
            <div className="mt-2 grid grid-cols-2 gap-2">
              {blouses.slice(0, 10).map((b) => (
                <button
                  key={b.id}
                  className={`btn btn-sm ${blouse?.id === b.id ? "btn-secondary" : "btn-ghost"}`}
                  onClick={() => {
                    setBlouse(b);
                    setJinnKey(`b-blouse-${b.id}`);
                  }}
                >
                  {b.name.slice(0, 10)}
                </button>
              ))}
            </div>
          </div>
          <div>
            <div className="font-bold">Accessories</div>
            <div className="mt-2 grid grid-cols-2 gap-2">
              {accessories.slice(0, 10).map((a) => (
                <button
                  key={a.id}
                  className={`btn btn-sm ${selectedAccessories.some((x) => x.id === a.id) ? "btn-accent" : "btn-ghost"}`}
                  onClick={() => {
                    toggleAccessory(a);
                    setJinnKey(`b-acc-${a.id}`);
                  }}
                >
                  {a.name.slice(0, 10)}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      <TailorJinn eventKey={jinnKey} />
    </div>
  );
}

