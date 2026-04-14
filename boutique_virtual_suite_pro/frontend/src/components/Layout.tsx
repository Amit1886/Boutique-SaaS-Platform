import React, { useEffect } from "react";
import Sidebar from "./Sidebar";
import BottomNav from "./BottomNav";
import TrylistDrawer from "./TrylistDrawer";
import TopBar from "./TopBar";
import Toasts from "./Toasts";
import { I18nProvider } from "../i18n/i18n";
import { useSettingsStore } from "../stores/settingsStore";
import { useMoodStore } from "../stores/moodStore";
import { useDesignerStore } from "../stores/designerStore";
import { useAuthStore } from "../stores/authStore";
import { useFavoritesStore } from "../stores/favoritesStore";

export default function Layout({ children }: { children: React.ReactNode }) {
  const theme = useSettingsStore((s) => s.theme);
  const moodColor = useMoodStore((s) => s.themeColor);
  const hydrateDesigner = useDesignerStore((s) => s.hydrateFromServer);
  const loadFavs = useFavoritesStore((s) => s.load);
  const token = useAuthStore((s) => s.token);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  useEffect(() => {
    document.documentElement.style.setProperty("--bvp-primary", moodColor || "#db2777");
  }, [moodColor]);

  useEffect(() => {
    if (token) hydrateDesigner().catch(() => {});
  }, [token, hydrateDesigner]);

  useEffect(() => {
    if (token) loadFavs().catch(() => {});
  }, [token, loadFavs]);

  return (
    <I18nProvider>
      <div className="min-h-screen bg-base-200 text-base-content">
        <TopBar />
        <Toasts />
        <div className="max-w-7xl mx-auto px-3 md:px-6 py-5 grid md:grid-cols-[260px_1fr] gap-5">
          <div className="hidden md:block">
            <Sidebar />
          </div>
          <div className="min-h-[70vh]">{children}</div>
        </div>
        <TrylistDrawer />
        <BottomNav />
      </div>
    </I18nProvider>
  );
}
