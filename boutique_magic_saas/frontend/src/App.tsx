import { AnimatePresence, motion } from "framer-motion";
import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import Navbar from "./components/Navbar";
import BottomNav from "./components/BottomNav";
import HomePage from "./pages/HomePage";
import TryOnStudioPage from "./pages/TryOnStudioPage";
import OutfitBuilderPage from "./pages/OutfitBuilderPage";
import FestivalThemesPage from "./pages/FestivalThemesPage";
import MagicMirrorPage from "./pages/MagicMirrorPage";
import SavedLooksPage from "./pages/SavedLooksPage";
import AdminPage from "./pages/AdminPage";
import MannequinPage from "./pages/MannequinPage";
import DrapingGuidePage from "./pages/DrapingGuidePage";
import { useEffect } from "react";
import { useUxStore } from "./store/useUxStore";
import { useCatalogStore } from "./store/useCatalogStore";
import { useAppStore } from "./store/useAppStore";

export default function App() {
  const location = useLocation();
  const loadUx = useUxStore((s) => s.load);
  const loadCatalog = useCatalogStore((s) => s.load);
  const magicColor = useAppStore((s) => s.magicColor);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", "magic_light");
    document.documentElement.style.setProperty("--magic-color", magicColor);
    loadUx().catch(() => {});
    loadCatalog().catch(() => {});
  }, [loadUx, loadCatalog, magicColor]);
  return (
    <div className="min-h-screen bg-base-200 text-base-content">
      <Navbar />
      <div className="max-w-7xl mx-auto px-3 md:px-6 py-5">
        <AnimatePresence mode="wait">
          <motion.div
            key={location.pathname}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
          >
            <Routes location={location}>
              <Route path="/" element={<HomePage />} />
              <Route path="/tryon-studio" element={<TryOnStudioPage />} />
              <Route path="/outfit-builder" element={<OutfitBuilderPage />} />
              <Route path="/festival-themes" element={<FestivalThemesPage />} />
              <Route path="/magic-mirror" element={<MagicMirrorPage />} />
              <Route path="/mannequin-3d" element={<MannequinPage />} />
              <Route path="/draping-guide" element={<DrapingGuidePage />} />
              <Route path="/saved-looks" element={<SavedLooksPage />} />
              <Route path="/admin" element={<AdminPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </motion.div>
        </AnimatePresence>
      </div>
      <BottomNav />
    </div>
  );
}
