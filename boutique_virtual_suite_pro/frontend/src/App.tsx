import { Navigate, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import MoodboardPage from "./pages/MoodboardPage";
import TrylistPage from "./pages/TrylistPage";
import StyleTestPage from "./pages/StyleTestPage";
import ResultsPage from "./pages/ResultsPage";
import ProfilePage from "./pages/ProfilePage";
import SettingsPage from "./pages/SettingsPage";
import FavoritesPage from "./pages/FavoritesPage";
import DesignerSareePage from "./pages/designer/DesignerSareePage";
import DesignerBlousePage from "./pages/designer/DesignerBlousePage";
import DesignerAccessoriesPage from "./pages/designer/DesignerAccessoriesPage";
import DesignerJewelryPage from "./pages/designer/DesignerJewelryPage";
import FinalPreviewPage from "./pages/FinalPreviewPage";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/moodboard" element={<MoodboardPage />} />
        <Route path="/trylist" element={<TrylistPage />} />
        <Route path="/favorites" element={<FavoritesPage />} />
        <Route path="/designer-flow/saree" element={<DesignerSareePage />} />
        <Route path="/designer-flow/blouse" element={<DesignerBlousePage />} />
        <Route path="/designer-flow/accessories" element={<DesignerAccessoriesPage />} />
        <Route path="/designer-flow/jewelry" element={<DesignerJewelryPage />} />
        <Route path="/final-preview" element={<FinalPreviewPage />} />
        <Route path="/style-test" element={<StyleTestPage />} />
        <Route path="/results" element={<ResultsPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/settings" element={<SettingsPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}
